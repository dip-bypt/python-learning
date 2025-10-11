# Day 21 — Document upload + FAISS Q&A API

This example provides a FastAPI app with two endpoints:

- POST /upload-pdf/ — upload a PDF, build embeddings and FAISS index (stored locally)
- POST /qa/ — ask a question (JSON body: {"question": "..."})

Behavior
- If embeddings/FAISS creation fails (client or key issues), the app stores
  plain text chunks and uses a lightweight TF-IDF fallback for QA instead of failing.

Tests

```bash
pytest day21/test_day21.py -q
```

Coverage

```bash
pytest --cov=day21 --cov-report=term-missing day21/test_day21.py
```
