import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

# LangChain imports
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="LangChain Document Q&A API", version="1.0")

# Embeddings
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY")
)

# LLM
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0.2
)

# Memory (simplest approach, no deprecated imports)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Global FAISS vectorstore
vector_store = None

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF, extract text, create embeddings, store in FAISS.
    """
    global vector_store

    # Save uploaded PDF temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    doc_chunks = splitter.split_documents(docs)

    # Create FAISS vectorstore
    vector_store = FAISS.from_documents(doc_chunks, embeddings)

    # Remove temp file
    os.remove(file_path)

    return {"message": f"PDF '{file.filename}' uploaded and embeddings stored successfully!", "chunks": len(doc_chunks)}

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question based on uploaded PDF.
    """
    global vector_store
    if vector_store is None:
        return {"error": "No PDF uploaded yet. Please upload a PDF first."}

    # Create conversational retrieval chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )

    # Get answer
    result = qa_chain.invoke({"question": request.question})
    return {
        "question": request.question,
        "answer": result["answer"]
    }

@app.get("/")
async def root():
    return {"message": "LangChain Document Q&A API running 🚀"}

