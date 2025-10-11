import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import shutil
from pydantic import BaseModel

# Define base directory early so it's available even if dotenv fails
base = os.path.dirname(__file__)

# Load environment
try:
    from dotenv import load_dotenv
    env_path = os.path.join(base, ".env")
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
except Exception:
    pass

# Ensure API key is set
key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not key:
    raise RuntimeError("No API key found in environment")
os.environ["OPENAI_API_KEY"] = key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

# LangChain + embeddings
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_community.vectorstores import FAISS
    from langchain.chains import RetrievalQA
    from langchain.docstore.document import Document as LC_Document
except Exception as e:
    raise RuntimeError("Install langchain_community, langchain_openai, FAISS, etc.") from e

VECTOR_DIR = os.path.join(base, "vectorstore")
VECTOR_PATH = os.path.join(VECTOR_DIR, "faiss_index")
os.makedirs(VECTOR_DIR, exist_ok=True)

app = FastAPI(title="LangChain Document Q&A API")

vector_store = None
qa_chain = None
uploaded_texts = []  # fallback storage of uploaded texts when embeddings fail

# -------------------------
# Upload PDF and create embeddings
# -------------------------


class UploadResponse(BaseModel):
    message: str


@app.post("/upload-pdf/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, qa_chain

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    pdf_path = os.path.join(VECTOR_DIR, file.filename)
    try:
        with open(pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Load PDF and split
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        # Ensure every document has a metadata attribute (some loaders/tests may not set it)
        for d in documents:
            if not hasattr(d, "metadata"):
                try:
                    d.metadata = {}
                except Exception:
                    # If we can't set attribute, create a lightweight wrapper
                    class _Doc:
                        def __init__(self, content):
                            self.page_content = content
                            self.metadata = {}

                    documents = [_Doc(getattr(x, "page_content", str(x))) for x in documents]
                    break
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.split_documents(documents)

        # Convert to LangChain Document
        lc_docs = [LC_Document(page_content=d.page_content, metadata=getattr(d, "metadata", {})) for d in docs]

        # Create embeddings + FAISS (guarded)
        try:
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            vector_store = FAISS.from_documents(lc_docs, embeddings)

            # Build retrieval QA chain
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever(search_kwargs={"k":3}), chain_type="stuff")

            # Save FAISS index locally
            try:
                vector_store.save_local(VECTOR_PATH)
            except Exception:
                print("Warning: failed to save FAISS index locally")

            return {"message": f"PDF '{file.filename}' uploaded and embeddings created successfully."}
        except Exception as e:
            # Embedding/FAISS failed. Fall back to storing texts for simple local search.
            print(f"Warning: embeddings/FAISS failed: {e}")
            # Save plain text chunks for fallback QA
            try:
                uploaded_texts.clear()
                for d in lc_docs:
                    uploaded_texts.append({"text": d.page_content, "meta": getattr(d, "metadata", {})})
            except Exception:
                pass
            return {"message": f"PDF uploaded but embeddings failed; using local fallback for QA."}
    except Exception as e:
        # Clean up uploaded file on error
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to process uploaded PDF: {e}")

# -------------------------
# Ask a question
# -------------------------
class QARequest(BaseModel):
    question: str


@app.post("/qa/")
async def ask_question(request: QARequest):
    global qa_chain
    if qa_chain is None:
        # If embeddings/FAISS failed during upload, we may still have uploaded_texts
        if uploaded_texts:
            # perform a simple local similarity search
            def similarity_search_local(items, query, k=1):
                import math, re
                from collections import Counter

                def tokenize(text: str):
                    return re.findall(r"\w+", text.lower())

                docs_tokens = [tokenize(it["text"]) for it in items]
                df = {}
                for toks in docs_tokens:
                    for t in set(toks):
                        df[t] = df.get(t, 0) + 1
                N = len(items)
                idf = {t: math.log((N + 1) / (1 + df[t])) + 1 for t in df}

                doc_vecs = []
                for toks in docs_tokens:
                    tf = Counter(toks)
                    vec = {}
                    norm = 0.0
                    for term, freq in tf.items():
                        w = freq * idf.get(term, 0.0)
                        vec[term] = w
                        norm += w * w
                    norm = math.sqrt(norm) if norm > 0 else 1.0
                    doc_vecs.append((vec, norm))

                q_toks = tokenize(query)
                q_tf = Counter(q_toks)
                q_vec = {}
                q_norm = 0.0
                for term, freq in q_tf.items():
                    w = freq * idf.get(term, math.log((N + 1) / 1) + 1)
                    q_vec[term] = w
                    q_norm += w * w
                q_norm = math.sqrt(q_norm) if q_norm > 0 else 1.0

                scores = []
                for (vec, norm), item in zip(doc_vecs, items):
                    dot = 0.0
                    for term, w in q_vec.items():
                        dot += w * vec.get(term, 0.0)
                    sim = dot / (norm * q_norm)
                    scores.append((sim, item))

                scores.sort(key=lambda x: x[0], reverse=True)
                return [it for s, it in scores[:k]]

            results = similarity_search_local(uploaded_texts, request.question, k=1)
            if results:
                return {"question": request.question, "answer": results[0]["text"]}
            else:
                raise HTTPException(status_code=500, detail="No fallback results available.")
        raise HTTPException(status_code=400, detail="No PDF uploaded yet. Please upload a PDF first.")

    try:
        answer = qa_chain.run(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM/chain error: {e}")

# -------------------------
# Load FAISS index on startup (if exists)
# -------------------------
@app.on_event("startup")
def load_faiss_on_startup():
    global vector_store, qa_chain
    try:
        if os.path.isdir(VECTOR_DIR):
            # try load if saved index exists
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            try:
                vector_store = FAISS.load_local(VECTOR_PATH, embeddings)
            except Exception:
                # fallback: nothing to load
                vector_store = None
            if vector_store is not None:
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
                qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever(search_kwargs={"k":3}), chain_type="stuff")
                print("Loaded existing FAISS index on startup")
    except Exception as e:
        print(f"Warning: failed to load FAISS on startup: {e}")
