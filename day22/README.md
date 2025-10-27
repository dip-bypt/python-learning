# Day 22 — LangChain Q&A API (fast prototype)

This folder contains a small FastAPI app that demonstrates uploading a PDF, building an embedding vector store with FAISS, and answering questions with a RetrievalQA chain.

Files
- `day22.py` — FastAPI app exposing `/upload_pdf`, `/ask`, and `/logs`.
- `test_day22.py` — pytest tests that inject fake "langchain" modules so tests run without real heavy dependencies or API keys.

Notes
- The app depends on langchain_community, langchain_openai, and faiss; the tests avoid those heavy deps by monkeypatching fake modules.
- To run the app for real you must install the dependencies listed in the project `requirements.txt` and set appropriate API keys in your environment (for example `OPENAI_API_KEY` or other provider keys).

Run tests

Install dev test deps (if not already installed):

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

Run tests with coverage:

```bash
pytest day22 -q --cov=day22
```

If you want to run the FastAPI app locally:

```bash
uvicorn day22.day22:app --reload
```

The tests are intentionally lightweight and self-contained. They verify the happy path (upload + ask) and the error path (ask without upload) using fakes.
