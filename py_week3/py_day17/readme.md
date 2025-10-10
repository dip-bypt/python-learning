# Day 17: PDF Document Summarization with LangChain

## Comprehensive Learning Topics

- **Document Loaders:** Using LangChain’s PyPDFLoader to process PDF and TXT files.
- **PDF Summarization:** Simple summarization of documents using LLMs.
- **Practical Task:** Summarize a 2-page PDF document via API or script.

---

## Project Overview

This project demonstrates how to:
- Load and process PDF documents using LangChain’s PyPDFLoader.
- Summarize the content of each page using an LLM (OpenAI).
- Expose the summarization as a FastAPI endpoint.
- Run and test the summarization pipeline both via API and console.

---

## How It Works

- **API Endpoint:**  
  `POST /summarize-pdf`  
  Upload a PDF file and receive a summary of its contents (one summary per page, combined).

- **Console Demo:**  
  Run `main.py` directly to summarize the first two pages of `sample.pdf` (if present).

---

## Example Usage

### 1. Install Requirements

```bash
pip install fastapi uvicorn langchain-core langchain-openai langchain-community python-dotenv reportlab
```

### 2. Set Up Environment

- Place your OpenAI API key in a `.env` file as `OPENAI_API_KEY=sk-...`
- (Optional) Add a sample PDF as `py_day17/sample.pdf` for console demo.

### 3. Run the API

```bash
uvicorn py_day17.main:app --reload
```

### 4. Example API Request

```bash
curl --location 'http://127.0.0.1:8000/summarize-pdf' \
  --form 'file=@sample.pdf;type=application/pdf'
```

**Response:**
```json
{
  "summary": "Page 1 summary...\nPage 2 summary..."
}
```

---

## Test Coverage

Automated tests are provided in `test_main.py` using FastAPI’s TestClient and in-memory PDF generation:

- **Valid PDF:** Ensures a summary is returned for a real PDF.
- **Invalid File:** Uploading a non-PDF returns a clear error.
- **Empty PDF:** Handles empty PDFs gracefully.
- **Missing File:** Returns a validation error if no file is uploaded.

Run tests with:
```bash
pytest py_day17/test_main.py
```

---

## Learning Recap

- **Document Loaders:** Efficiently load and parse PDFs for downstream LLM tasks.
- **Error Handling:** Robust API design for file validation and user feedback.
- **LangChain Pipelines:** Compose prompt templates and LLMs for document summarization.

---

## Practical Task

> **Task:** Summarize a 2-page PDF document  
> Try the API or run the script to see concise summaries generated for your PDF files.

---

