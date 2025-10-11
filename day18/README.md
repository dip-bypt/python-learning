# Day 18 — Simple Similarity Search (FAISS fallback)

This lesson demonstrates how to load plain text files and perform a simple
similarity search. The code prefers a LangChain + FAISS production path when
an API key and packages are available, and otherwise runs a local lightweight
similarity heuristic for demo purposes.

Files
- `day18.py` — main implementation (functions: `load_documents`, `similarity_search_local`, `main`).
- `test_day18.py` — unit tests for loading documents and local similarity.

Run

```bash
python day18/day18.py
```

Tests

```bash
pytest day18/test_day18.py -q
```

Coverage

```bash
pytest --cov=day18 --cov-report=term-missing day18/test_day18.py
```

Notes

- The script will exit early with a demo listing if no `OPENROUTER_API_KEY` or
  `OPENAI_API_KEY` is present. To run the FAISS path, set an API key and
  install `langchain` and FAISS.
