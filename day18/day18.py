import os
from pathlib import Path
from typing import List

# Set base path immediately so it's available even if dotenv isn't installed
base = os.path.dirname(__file__)

# --------------------------
# Load .env if exists
# --------------------------
try:
    from dotenv import load_dotenv
    env_path = os.path.join(base, ".env")
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
except Exception:
    pass


# --------------------------
# Lightweight Document fallback
# --------------------------
class SimpleDocument:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata


def load_documents(folder: str) -> List[SimpleDocument]:
    p = Path(folder)
    docs: List[SimpleDocument] = []
    for file_path in p.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(SimpleDocument(page_content=text, metadata={"source": file_path.name}))
    return docs


def similarity_search_local(documents: List[SimpleDocument], query: str, k: int = 3) -> List[SimpleDocument]:
    """A tiny local similarity heuristic: count overlap of query tokens in each document."""
    q_tokens = [t.lower() for t in query.split()]
    scores = []
    for d in documents:
        text = d.page_content.lower()
        score = sum(text.count(tok) for tok in q_tokens)
        scores.append((score, d))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [d for s, d in scores[:k]]


def main():
    # Load text files
    folder = Path(base) / "texts"
    documents = load_documents(folder)

    if not documents:
        raise FileNotFoundError("No text files found in 'texts/' folder.")

    # Ensure API key is set
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        print("⚠️ No API key found. Using local fallback for demo purposes.")
        print("\nDemo similarity search result:\n")
        for doc in documents:
            print(f"- {doc.metadata['source']}")
        # Also show a local similarity sample
        query = "Which file talks about AI?"
        results = similarity_search_local(documents, query)
        print(f"\nTop matching files for query: {query}")
        for res in results:
            print(f"- {res.metadata['source']}")
        raise SystemExit(0)

    # If we have a key, try to use LangChain + FAISS; if imports fail, fall back to local search
    os.environ["OPENAI_API_KEY"] = key
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    try:
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.docstore.document import Document as LC_Document
    except Exception:
        print("langchain or FAISS not available; running local similarity search instead.")
        query = "Which file talks about AI?"
        results = similarity_search_local(documents, query)
        print(f"\nTop matching files for query: {query}")
        for res in results:
            print(f"- {res.metadata['source']}")
        return

    # Build embeddings and FAISS index (wrapped so failures fall back gracefully)
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        # Convert SimpleDocument -> LangChain Document so FAISS gets the attributes it expects
        lc_docs = [LC_Document(page_content=d.page_content, metadata=d.metadata) for d in documents]
        faiss_index = FAISS.from_documents(lc_docs, embeddings)
        query = "Which file talks about AI?"
        results = faiss_index.similarity_search(query, k=3)
        print("\nTop matching files for query:", query)
        for res in results:
            print(f"- {res.metadata['source']}")
    except Exception as e:
        print("Failed to build FAISS index or fetch embeddings; falling back to local similarity.")
        print("Error:", e)
        query = "Which file talks about AI?"
        results = similarity_search_local(documents, query)
        print(f"\nTop matching files for query: {query}")
        for res in results:
            print(f"- {res.metadata['source']}")


if __name__ == "__main__":
    main()
