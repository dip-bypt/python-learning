import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

def load_documents(data_dir):
    docs = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            path = os.path.join(data_dir, filename)
            loader = TextLoader(path)
            file_docs = loader.load()
            print(f"📄 Loaded {filename} with {len(file_docs)} document(s)")
            docs.extend(file_docs)
    print(f"\n✅ Total documents loaded: {len(docs)}")
    return docs

def split_documents(docs, chunk_size=400, chunk_overlap=50):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)
    print(f"📚 After splitting: {len(chunks)} chunks ready for embedding.")
    return chunks

def create_vector_store(docs, embeddings):
    db = FAISS.from_documents(docs, embeddings)
    print("\n🧠 FAISS vector store created successfully!")
    return db

def perform_queries(db, queries, k=2):
    results_per_query = []
    for query in queries:
        print("\n🔍 Query:", query)
        results = db.similarity_search(query, k=k)
        for i, res in enumerate(results, start=1):
            print(f"\nResult {i}:")
            print("Content:", res.page_content[:200].replace("\n", " "), "...")
            print("Metadata:", res.metadata)
        print("-" * 80)
        results_per_query.append(results)
    return results_per_query

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    data_dir = "py_day18/data"
    docs = load_documents(data_dir)
    docs = split_documents(docs, chunk_size=400, chunk_overlap=50)
    db = create_vector_store(docs, embeddings)
    queries = [
        "Which file talks about AI?",
        "Which document explains web development?",
        "Tell me which file mentions data science or machine learning."
    ]
    perform_queries(db, queries, k=2)
