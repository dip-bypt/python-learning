# Day 22 — Async FastAPI & Background Tasks

## Overview
This small sample FastAPI project demonstrates using async endpoints together with BackgroundTasks to perform non-blocking work (saving API logs to disk).

Project layout (relevant files):
- `main.py` — FastAPI application with async endpoints and a background task that appends log entries to a file.
- `test_main.py` — pytest-based tests that exercise the endpoints and validate logging behavior.
- `logs/api_logs.txt` — the runtime log file (the app creates the `logs` directory automatically).

Day: Day 22
Comprehensive Learning Topics:
- Async FastAPI & Background Tasks
- Async endpoints
- BackgroundTasks usage

Detailed Practical Task:
- Task: Add a background task to save API logs to file

## What the app does
`main.py` exposes several async endpoints and uses FastAPI's `BackgroundTasks` to save log entries to a file without delaying the HTTP response.

Key behaviors:
- On startup the app ensures the `py_day22/logs` directory exists.
- Each endpoint schedules `save_log_to_file(endpoint, message)` as a background task.
- `save_log_to_file` writes timestamped entries to `py_day22/logs/api_logs.txt`.

Endpoints
- `GET /` — root; returns a small JSON message and logs: "Root endpoint called".
- `GET /status` — returns `{"status": "ok", "message": ...}` and logs a status message.
- `GET /greet/{name}` — returns a personalized greeting and logs the name that was greeted.
- `POST /process` — simulates starting a background processing task and logs the action.

Log format (one line per entry):
```
[YYYY-MM-DD HH:MM:SS] /endpoint: Log message
```

## Tests
Tests live in `py_day22/test_main.py` and are written with `pytest` and FastAPI's `TestClient`.

What the tests cover:
- `test_root_logs_and_response` — verifies GET `/` returns the expected JSON and that the background log contains "Root endpoint called".
- `test_status_logs_and_response` — verifies GET `/status` returns `status: ok` and that the log file contains the status message.
- `test_greet_logs_and_response` — calls `GET /greet/Alice`, checks the greeting response and verifies the log contains `Greeted user: Alice` and the `/greet/Alice` path.
- `test_process_post_logs_and_response` — calls `POST /process` and checks the JSON response and log entry.
- `test_save_log_to_file_direct` — calls the helper function directly to ensure it writes to the (monkeypatched) log file.

Testing approach details:
- The tests import `main.py` by file path and use pytest's `monkeypatch` fixture to redirect `main.LOG_FILE` and `main.LOG_DIR` to a temporary path. This prevents altering repository logs and makes tests hermetic.
- Because the app uses `BackgroundTasks` (which writes to the log after the response), tests include a short polling loop to wait briefly for the log file to be created and populated.

## How to run locally
1. Install dependencies (from the repository root):

```bash
python -m pip install -r requirement.txt
```

2. Run the FastAPI app using Uvicorn (from the repository root):

```bash
uvicorn py_day22.main:app --reload --port 8000
```

This serves the app at http://127.0.0.1:8000. Try the endpoints with curl or a browser.

3. Run tests:

```bash
pytest -q
```

Notes and debugging tips
- Tests monkeypatch `LOG_FILE` at runtime. If you run the app and tests simultaneously they operate on different locations (tests use a tmp path).
- If you don't see log entries, confirm the `py_day22/logs` directory exists and is writable by the process running the server.
- If your environment is slow (CI), increase the short timeout used by tests to read the log file.

Next steps / improvements
- Add async tests that use `httpx.AsyncClient` for more explicit async coverage.
- Add CI (GitHub Actions) to run pytest automatically on push/PR.
- Extend logging to rotate logs or use structured JSON logs for easier parsing.

---
Generated: README for Day 22 — Async FastAPI & Background Tasks

