# Day 17 — PDF Summarization (LangChain + OpenRouter)

This lesson shows how to summarize a PDF using LangChain and an OpenRouter-backed
LLM. The code is written to be testable without network access by allowing a
mock `llm_callable` to be injected into `process_pdf`.

Files
- `day17.py` — main implementation (function: `process_pdf(pdf_path, llm_callable=None)`).
- `test_day17.py` — pytest tests that exercise the mock path and missing-file error.

Setup

- Create a `.env` in `day17/` containing:

```
OPENROUTER_API_KEY=your_openrouter_key_here
```

or set `OPENROUTER_API_KEY` / `OPENAI_API_KEY` in your environment.

Installation

Install test dependencies (pytest) and python-dotenv if you want automatic .env loading:

```bash
python -m pip install -r requirements.txt
# or at minimum:
python -m pip install pytest python-dotenv
```

Run

To run the summarization (requires a real API key and `sample.pdf` in the folder):

```bash
python day17/day17.py
```

Tests

```bash
pytest day17/test_day17.py -q
```

Coverage

```bash
pytest --cov=day17 --cov-report=term-missing day17/test_day17.py
```

Notes

- The runtime imports heavy langchain packages only when `process_pdf` is called
  without an `llm_callable`, so tests and import-time checks stay lightweight.
- If you run the script directly, it will look for `sample.pdf` in the same folder.
