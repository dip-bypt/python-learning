import os
from typing import List
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
from collections import Counter


# Lightweight SimpleDocument for local fallback
class SimpleDocument:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata


# Module-level state used by ask_question when no args are provided
documents: List[SimpleDocument] = []
vector_store = None


# -------------------------------
# Load PDF and Split into Chunks
# -------------------------------
def load_pdf_documents(pdf_path: str) -> List[SimpleDocument]:
    """Load PDF using PyPDF2 and return as SimpleDocuments"""
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            docs.append(SimpleDocument(text, {"page": i + 1}))
    return docs


def split_documents(documents: List[SimpleDocument]) -> List[SimpleDocument]:
    """Split long documents into smaller 300-character chunks."""
    chunks = []
    for d in documents:
        text = d.page_content
        for i in range(0, len(text), 300):
            chunk = text[i:i + 300]
            chunks.append(SimpleDocument(chunk, d.metadata))
    return chunks


def build_vector_store_local(docs: List[SimpleDocument]):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [d.page_content for d in docs]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    # Use cosine similarity (via IndexFlatIP)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))

    return (index, embeddings, texts, model)


# Backwards-compatible alias used by older tests
build_vector_store = build_vector_store_local


def query_vector_store_local(query: str, store, k=2):
    index, embeddings, texts, model = store
    q_vec = model.encode([query], normalize_embeddings=True)
    D, I = index.search(np.array(q_vec).astype("float32"), k)
    results = [texts[i] for i in I[0]]
    return results


def ask_question(question: str, store=None, documents=None):
    print(f"\n❓ Question: {question}")
    # fallback to module-level state if parameters are not provided
    if store is None:
        store = globals().get('vector_store', None)
    if documents is None:
        documents = globals().get('documents', [])

    if store is not None:
        try:
            results = query_vector_store_local(question, store, k=2)
            answer = "\n---\n".join(results)
            print(f"💬 Answer (from embeddings):\n{answer[:400]}...\n")
            return answer
        except Exception as e:
            print("⚠️ Error using FAISS store:", e)

    # fallback
    if documents:
        results = similarity_search_local(documents, question, k=2)
        ans = "\n---\n".join([r.page_content[:400] for r in results])
        print(f"💬 Local Answer (excerpt):\n{ans}\n")
        return ans


def similarity_search_local(documents: List[SimpleDocument], query: str, k: int = 3):
    """Simple TF-IDF based similarity (dependency-free)"""
    import math
    import re
    from collections import Counter

    def tokenize(text: str):
        return re.findall(r"\w+", text.lower())

    docs_tokens = [tokenize(d.page_content) for d in documents]
    df = {}
    for toks in docs_tokens:
        for t in set(toks):
            df[t] = df.get(t, 0) + 1

    N = len(documents)
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
    for (vec, norm), doc in zip(doc_vecs, documents):
        dot = 0.0
        for term, w in q_vec.items():
            dot += w * vec.get(term, 0.0)
        sim = dot / (norm * q_norm)
        scores.append((sim, doc))

    scores.sort(key=lambda x: x[0], reverse=True)
    return [d for s, d in scores[:k]]



# -------------------------------
# Main Program
# -------------------------------
def main():
    pdf_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError("sample.pdf not found! Place it in the same folder.")

    print(f"📘 Loading PDF: {pdf_path}")
    # populate module-level documents so ask_question can use them later
    global documents, vector_store
    documents = load_pdf_documents(pdf_path)
    docs = split_documents(documents)
    print(f"✅ Split PDF into {len(docs)} text chunks.")

    print("🔍 Creating embeddings and building FAISS index (offline)...")
    # Use the (possibly monkeypatched) build_vector_store API so tests can
    # replace it easily.
    vector_store = build_vector_store(docs)
    # store in module-level variable for ask_question fallback
    globals()['vector_store'] = vector_store
    globals()['documents'] = documents

    import sys
    print("\n🚀 Mini PDF Q&A Bot Ready! Type your question below.")
    # If stdin is not a TTY (for example while running pytest), skip the interactive loop
    if not sys.stdin.isatty():
        print("Interactive mode skipped (non-TTY stdin).")
        return

    while True:
        q = input("\nAsk: ").strip()
        if q.lower() in ["exit", "quit"]:
            break
        ask_question(q, vector_store, docs)


if __name__ == "__main__":
    main()
