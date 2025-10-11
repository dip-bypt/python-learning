# Day 20 — PDF Q&A with FAISS (with local fallbacks)

This lesson builds a small PDF Q&A pipeline: load a PDF, split into chunks,
create embeddings and a FAISS vector store, then run a retriever+QA chain.

The implementation includes robust fallbacks so tests and demos don't require
real API keys or heavy dependencies.

Run

```bash
python day20/day20.py
```

Tests

```bash
pytest day20/test_day20.py -q
```

Coverage

```bash
pytest --cov=day20 --cov-report=term-missing day20/test_day20.py
```

Notes
- If you want the real embedding/FAISS path to run, set `OPENROUTER_API_KEY`
  or `OPENAI_API_KEY` in `day20/.env` and install the required packages.
