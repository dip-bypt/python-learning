# Day 18: Embeddings & Vector Stores with FAISS

## Comprehensive Learning Topics
- **Embeddings & Vector Stores:** How to represent text as vectors for semantic search.
- **Sentence Embeddings:** Using OpenAI to embed text documents.
- **FAISS for Similarity Search:** Efficiently store and query document vectors.

---

## Project Overview
This project demonstrates how to:
- Load multiple text files as documents.
- Split documents into manageable chunks for embedding.
- Generate embeddings for each chunk using OpenAI.
- Store all embeddings in a FAISS vector store for fast similarity search.
- Query the vector store to find the most relevant documents for a given question.

---

## Detailed Practical Task
- **Task:** Store 10 text files in FAISS and answer queries such as: “Which file talks about AI?”

---

## How It Works
- **Document Loading:** All `.txt` files in `py_day18/data/` are loaded as documents.
- **Splitting:** Each document is split into smaller chunks for better embedding and retrieval.
- **Embedding:** Each chunk is embedded using OpenAI sentence embeddings (API key required).
- **Vector Store:** All embeddings are stored in a FAISS index for efficient similarity search.
- **Querying:** You can query the store with natural language questions to retrieve the most relevant document chunks.

---

## Example Usage

### 1. Install Requirements
```bash
pip install fastapi langchain-core langchain-openai langchain-community python-dotenv faiss-cpu
```

### 2. Set Up Environment
- Place your OpenAI API key in a `.env` file as `OPENAI_API_KEY=sk-...`
- Add your `.txt` files to the `py_day18/data/` directory (10 sample files are included).

### 3. Run the Script
```bash
python py_day18/main.py
```

### 4. Example Output
```
📄 Loaded file1_ai.txt with 1 document(s)
... (other files loaded)
✅ Total documents loaded: 10
📚 After splitting: 10 chunks ready for embedding.
🧠 FAISS vector store created successfully!

🔍 Query: Which file talks about AI?
Result 1:
Content: ...
Metadata: ...
```

---

## Test Coverage
Automated tests are provided in `test_main.py`:
- **Document Loading:** Verifies all text files are loaded correctly.
- **Splitting:** Checks that documents are split into non-empty chunks.
- **Vector Store & Query:** Uses a dummy embedding to test FAISS integration and query results structure.
- **Error Handling:** Tests for missing or empty data directories.

Run tests with:
```bash
pytest py_day18/test_main.py
```

---

## Learning Recap
- **Embeddings:** Transforming text into high-dimensional vectors for semantic comparison.
- **FAISS:** Using Facebook AI Similarity Search for fast vector-based document retrieval.
- **LangChain Integration:** Modular pipeline for loading, splitting, embedding, storing, and querying documents.

---

## Practical Task
> **Task:** Store 10 text files in FAISS and query: “Which file talks about AI?”
> 
> Try running the script and experiment with your own queries for semantic search over your document collection.

