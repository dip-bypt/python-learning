## Week 3 — LangChain Fundamentals (Day 16)

This folder demonstrates a compact example of Prompt Templates and Sequential Chains using LangChain concepts. The practical task implemented here chains two steps:

- Input text → Summarize (2 concise sentences)
- Summary → Extract Keywords (returns 5 keywords as a comma-separated list)

The code shows both a console example and a FastAPI service that exposes the chain via an `/analyze` endpoint.

### Comprehensive Learning Topics

- Prompt Templates & Sequential Chains
- Dynamic placeholders in templates (e.g., `{text}`, `{summary}`)
- Combining multiple chains (composition of prompt → LLM → prompt → LLM)

### Files of interest

- `main.py` — Implements two prompt templates and composes them with an OpenAI LLM. Provides:
	- Console example (runs when executed directly)
	- FastAPI app exposing `/analyze` and `/` endpoints
- `test_main.py` — Tests the FastAPI endpoints using `TestClient`:
	- GET `/` should return a JSON message containing "Day 16 - Sequential Chain API"
	- POST `/analyze` with JSON {"text": <string>} should return:
		- `original_text`: same as input
		- `summary`: a string
		- `keywords`: a list (parsed from the LLM CSV output)

### Contract (inputs / outputs)

- Input: JSON {"text": "..."}
- Output: JSON {
	"original_text": string,
	"summary": string,
	"keywords": [string, ...]
}

Errors / edge cases handled by tests

- Empty text — service returns an empty `original_text` and still returns `summary` and `keywords` (strings/lists). Tests expect types, not specific LLM content.
- Long text — service should accept long inputs and return summary/keywords (test ensures response structure and types).

### Prerequisites

- Python 3.10+ (project used Python 3.12 artifacts in cache, but 3.10+ is recommended)
- An OpenAI API key set in the environment as `OPENAI_API_KEY` (the code uses `python-dotenv` to load `.env`)
- Required packages (example):

```bash
pip install fastapi uvicorn python-dotenv pytest requests langchain-core langchain-openai
```

Note: package names may vary depending on your LangChain/LLM client choices; the repository imports `langchain_core` and `langchain_openai`.

### How to run (console)

Run the example directly to see console output (it will invoke the chains and print summary + keywords):

```bash
python py_day16/main.py
```

### How to run (API)

Start the FastAPI server with uvicorn :

```bash
uvicorn py_day16.main:app --reload
```

Then:
- GET http://127.0.0.1:8000/ — health/description
- POST http://127.0.0.1:8000/analyze with JSON body {"text": "..."}

Example request payload:

```json
{ "text": "Python is a versatile language used for web, data science and automation." }
```

**Example curl request:**
```bash
curl --location 'http://127.0.0.1:8000/analyze' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Manually reading all reviews is impossible, so the company wants to understand what customers like and dislike about the product. "
}'
```

Example (expected shape) response:

```json
{
	"original_text": "Python is a versatile language used for web, data science and automation.",
	"summary": "Python is a versatile language used across web development, data science and automation. Its simplicity and libraries make it a popular choice.",
	"keywords": ["Python", "web development", "data science", "automation", "libraries"]
}
```

### Tests

Run the tests

```bash
pytest py_day16/test_main.py
```

The included tests verify:
- the root endpoint returns the expected message string
- `/analyze` returns the expected JSON shape for normal, empty and long inputs

### Notes, assumptions and next steps

- The LLM output is not deterministic. Tests only assert structure and basic invariants (types & presence). If you want deterministic unit tests, mock the LLM client or inject a fake responder.
- Consider adding input validation (reject non-string text), rate limiting, and better error handling for LLM timeouts.
- Small improvements: parse and normalise keyword casing, trim empty tokens, and add an examples section in the README showing actual console outputs when using a fixed mock LLM.

Requirements coverage:
- Review `main.py`: Done — behavior and endpoints documented.
- Review `test_main.py`: Done — test expectations included.
- Include learning details (Prompt Templates, Sequential Chains, dynamic placeholders): Done.

If you want, I can run the test suite and/or start the FastAPI server here and report the outputs (I will need a valid `OPENAI_API_KEY` in the environment or we can mock the LLM for tests).
