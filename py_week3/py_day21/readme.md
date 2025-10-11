# Day 21: LangChain Document Q&A API

## Comprehensive Learning Topics

- **Project:** LangChain Document Q&A API
- **Key Concepts:**
  - Upload PDF → store embeddings
  - Ask question → get context-based answer
  - Serve via FastAPI

## Project Overview

This project demonstrates a FastAPI-based API for document Q&A using LangChain. Users can upload a PDF, which is processed and stored as embeddings in a FAISS vector store. The API then allows users to ask questions about the uploaded document and receive context-aware answers powered by an LLM.

## Features

1. **Upload PDF:**  
   - Endpoint: `/upload_pdf`  
   - Accepts a PDF file, extracts and chunks its content, creates embeddings, and stores them in a FAISS vector store.

2. **Ask Question:**  
   - Endpoint: `/ask`  
   - Accepts a question and returns an answer based on the uploaded PDF using a conversational retrieval chain.

3. **Serve via FastAPI:**  
   - The API is built with FastAPI and provides endpoints for PDF upload, Q&A, and a root health check.

## Code Structure

- **main.py:**  
  - Implements the FastAPI app, PDF upload, embedding storage, and Q&A endpoints.
  - Uses LangChain's PyPDFLoader, OpenAIEmbeddings, FAISS, and ConversationalRetrievalChain.
  - Maintains conversational memory for context-aware answers.

- **test_main.py:**  
  - Uses `pytest` and FastAPI's `TestClient` for automated endpoint testing.
  - Tests include:
    - Root endpoint health check.
    - Asking a question before uploading a PDF (should return an error).
    - Uploading a PDF and then asking a question (should return a relevant answer).

## Example Usage

### 1. Install dependencies

```bash
pip install -r requirement.txt
```

### 2. Run the FastAPI server

```bash
uvicorn py_day21.main:app --reload
```

### 3. Upload a PDF

Use a tool like Postman or `curl`:

```bash
curl -F "file=@yourfile.pdf" http://127.0.0.1:8000/upload_pdf
```

### 4. Ask a question

```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question": "What is the capital of France?"}'
```

### 5. Root endpoint

```bash
curl http://127.0.0.1:8000/
```

## How to Run Test Cases

1. Make sure you have `pytest` installed:

   ```bash
   pip install pytest
   ```

2. Run the tests:

   ```bash
   pytest py_day21/test_main.py
   ```

All tests should pass, confirming the API's endpoints and logic are working as expected.

## Learning Outcomes

- Build a document Q&A API using LangChain and FastAPI.
- Store and retrieve document embeddings for semantic search.
- Integrate conversational memory for context-aware answers.
- Write and run automated tests for API endpoints.

---

