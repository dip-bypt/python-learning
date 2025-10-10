# Day 16 — Summarization + Keyword Extraction Chain

This folder contains a small LangChain example that:

- Summarizes input text (3-4 sentences)
- Extracts the top 5 keywords from the summary

Usage

1. Set your OpenRouter API key in the environment (or create `day16/.env`):

```bash
export OPENROUTER_API_KEY="sk-...your_key..."
# or copy day16/.env.example to day16/.env and edit it
```

2. Run the script:

```bash
python3 day16/day16.py
```

Testing

- A unit test is provided in `day16/test_day16.py`. It uses a mock LLM callable to
  test `process_text` without requiring a real API key or network access.

Run tests with:

```bash
pip install pytest
pytest day16/test_day16.py -q
```

Test coverage

To run the tests and see a coverage report for the `day16` package, install coverage tools and run:

```bash
pip install pytest pytest-cov coverage
pytest --cov=day16 --cov-report=term-missing day16/test_day16.py -q
# or a full coverage run and report:
coverage run -m pytest && coverage report -m
```

Notes

- The code reads `OPENROUTER_API_KEY` (or `OPENAI_API_KEY`) from the environment and sets
  `OPENAI_BASE_URL` to `https://openrouter.ai/api/v1` for LangChain compatibility.
- For local development you can create a `.env` file and the script will load it
  if `python-dotenv` is installed.
