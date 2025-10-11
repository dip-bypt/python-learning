# Day 19 — LangChain Q&A FastAPI

This example exposes a small FastAPI endpoint which runs a LangChain LLMChain
to answer questions about an input text.

Endpoint
- POST /qa
  - Request JSON: { "text": "...", "question": "..." }
  - Response JSON: { "answer": "..." }

Running locally

1. Set your API key in `day19/.env` or the environment:

```
OPENROUTER_API_KEY=your_key_here
```

2. Install runtime deps (LangChain + FastAPI + Uvicorn):

```bash
python -m pip install fastapi uvicorn langchain langchain-openai python-dotenv
```

3. Start the server:

```bash
cd day19
uvicorn day19:app --reload
```

Tests

Tests mock the LangChain chain so they are fast and don't require an API key.

```bash
pytest day19/test_day19.py -q
```

Coverage

```bash
pytest --cov=day19 --cov-report=term-missing day19/test_day19.py
```
