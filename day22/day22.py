import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException

# Optional heavy deps -- tolerate absence so module is importable.
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain.chains import RetrievalQA
except Exception:
    PyPDFLoader = None
    FAISS = None
    OpenAIEmbeddings = None
    ChatOpenAI = None
    RetrievalQA = None

# Load .env: prefer a .env next to this module, then the repository root, then default lookup.
try:
    from dotenv import load_dotenv

    this_dir = Path(__file__).resolve().parent
    local_env = this_dir / ".env"
    repo_env = this_dir.parents[1] / ".env"

    if local_env.is_file():
        load_dotenv(local_env)
        print(f"Loaded environment from {local_env}")
    elif repo_env.is_file():
        load_dotenv(repo_env)
        print(f"Loaded environment from {repo_env}")
    else:
        # fall back to default behavior (look for .env in cwd or use already-set env vars)
        try:
            load_dotenv()
        except Exception:
            pass
except Exception:
    # dotenv is optional for runtime; env may be set externally
    pass

# If an OpenRouter key is present but libraries expect OPENAI_API_KEY, copy it across.
# This avoids provider client errors that require OPENAI_API_KEY to be set.
if not os.environ.get("OPENAI_API_KEY") and os.environ.get("OPENROUTER_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENROUTER_API_KEY")

# ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_DIR / "qa_logs.txt"

app = FastAPI(title="Day22 LangChain Q&A")

# Module-level state (kept simple for the demo)
vector_store: Optional[object] = None
qa_chain: Optional[object] = None


def log_to_file(question: str, answer: str) -> None:
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "answer": answer,
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF and build embeddings + FAISS store.

    The endpoint validates that optional ML dependencies and an API key
    are present and returns clear HTTP errors if not.
    """
    global vector_store, qa_chain

    # Check optional deps
    if PyPDFLoader is None or FAISS is None or OpenAIEmbeddings is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Missing optional dependencies: install langchain_community, "
                "langchain_openai, and faiss to use /upload_pdf"
            ),
        )

    # Require an API key (OpenAI or OpenRouter) to avoid provider runtime errors
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail=(
                "OPENAI_API_KEY (or OPENROUTER_API_KEY) is not set. "
                "Set it in the environment before calling /upload_pdf."
            ),
        )

    # Save uploaded file temporarily
    temp_path = Path(f"temp_{Path(file.filename).name}")
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {e}")

    try:
        temp_path.write_bytes(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write temp file: {e}")

    # Load documents
    try:
        loader = PyPDFLoader(str(temp_path))
        docs = loader.load()
    except Exception as e:
        # keep temp file for debugging if loader fails
        err = f"Failed to load PDF with PyPDFLoader: {e}"
        # write to an error log for debugging
        try:
            (LOG_DIR / "error.log").open("a", encoding="utf-8").write(f"{datetime.now()}: {err}\n")
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=err)

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # Try to pass the API key explicitly if the provider requires it at construction time.
        try:
            embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
        except TypeError:
            try:
                embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
            except TypeError:
                # Fallback to default constructor which may read from env
                embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        vector_store = FAISS.from_documents(docs, embeddings)

        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
        except TypeError:
            try:
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
            except TypeError:
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
    except Exception as e:
        err = f"Failed to create embeddings/vector store: {e}. Check your provider config and API key."
        # log for debugging
        try:
            (LOG_DIR / "error.log").open("a", encoding="utf-8").write(f"{datetime.now()}: {err}\n")
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=err)

    # cleanup
    try:
        temp_path.unlink()
    except Exception:
        pass

    return {"message": f"PDF '{file.filename}' uploaded."}


@app.post("/ask")
async def ask_question(background_tasks: BackgroundTasks, question: str = Form(...)):
    global qa_chain
    if qa_chain is None:
        return {"error": "No PDF uploaded yet. Please upload a PDF first."}
    # chain may be synchronous depending on provider; run in sync
    try:
        answer = qa_chain.run(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA error: {e}")

    background_tasks.add_task(log_to_file, question, answer)
    return {"question": question, "answer": answer}


@app.get("/logs")
async def get_logs():
    if not LOG_PATH.exists():
        return {"logs": []}

    logs = []
    with LOG_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            try:
                logs.append(json.loads(s))
            except Exception:
                logs.append({"raw": s})

    # return last 10 entries
    return {"logs": logs[-10:]} 
