# Day 19: LangChain + FastAPI Conversational Q&A API

## Comprehensive Learning Topics

- **LangChain + FastAPI:** Integrate LLM-powered Q&A with a modern web API.
- **API Endpoint for Q&A:** Accept user questions and return LLM-generated answers.
- **Session Memory:** Maintain conversational context using session IDs.

---

## Project Overview

This project demonstrates how to:
- Build a FastAPI service that exposes a `/qa` endpoint for question answering.
- Use LangChain’s memory features to support multi-turn conversations with session memory.
- Leverage OpenAI’s GPT-3.5-turbo for generating answers.

---

## Detailed Practical Task

- **Task:**  
  Build an API endpoint:  
  - **POST /qa** → returns an answer from the LLM based on the input question (and session memory).

---

## How It Works

- **POST /qa**  
  - Request:  
    ```json
    {
      "question": "What is the capital of France?",
      "session_id": "user123"
    }
    ```
    - `question` (str): The user’s question (required).
    - `session_id` (str): Session identifier for conversation memory (optional, defaults to `"default"`).

  - Response:  
    ```json
    {
      "question": "What is the capital of France?",
      "answer": "The capital of France is Paris.",
      "session_id": "user123"
    }
    ```

- **GET /**  
  - Returns a health/status message.

- **Session Memory:**  
  - Each session_id keeps its own conversation history, so follow-up questions can reference previous context.

---

## Example Usage

### 1. Install Requirements

```bash
pip install fastapi uvicorn langchain-core langchain-openai python-dotenv
```

### 2. Set Up Environment

- Place your OpenAI API key in a `.env` file as `OPENAI_API_KEY=sk-...`

### 3. Run the API

```bash
uvicorn py_day19.main:app --reload
```

### 4. Example Request

```bash
curl -X POST 'http://127.0.0.1:8000/qa' \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the capital of France?", "session_id": "demo"}'
```

---

## Test Coverage

Automated tests in `test_main.py` verify:

- **Root Endpoint:** Returns a status message.
- **Basic Q&A:** Answers are returned for valid questions.
- **Session Memory:** Follow-up questions in the same session use conversation history.
- **Session Isolation:** Different sessions do not share memory.
- **Validation:** Missing question returns a 422 error; missing session_id defaults to `"default"`.

Run tests with:
```bash
pytest py_day19/test_main.py
```

---

## Learning Recap

- **LangChain + FastAPI:** Seamless integration for LLM-powered APIs.
- **Session-based Memory:** Maintain context for multi-turn conversations.
- **Robust API Design:** Input validation and clear error handling.

---

## Practical Task

> **Task:**  
> Build and test a POST /qa endpoint that returns an LLM-generated answer from input text, supporting conversational memory.

---

## Console Conversational Q&A Mode

You can also interact with the Q&A system directly from the terminal for conversational retrieval:

```bash
python py_day19/main.py
```

- The console will prompt you for questions in a loop.
- Type your question and press Enter to get an answer from the LLM.
- The session maintains conversational memory, so you can ask follow-up questions.
- Type `quit`, `exit`, or `bye` to end the session.

Example:
```
🧠 Conversational Q&A Mode (Modern API)
Type 'quit' to end.

You: My name is Alice.
AI: Nice to meet you, Alice! How can I assist you today?
You: What is my name?
AI: Your name is Alice.
You: quit
👋 Conversation ended. Goodbye!
```

This mode demonstrates conversational retrieval and memory directly in the terminal, without needing to use the API endpoints.
