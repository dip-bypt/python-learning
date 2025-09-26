# Day 4: FastAPI Basics

## Overview
This project introduces FastAPI, a modern, fast web framework for building APIs with Python 3.7+. FastAPI leverages async/await syntax for high-performance, non-blocking I/O operations, making it ideal for concurrent requests. It automatically generates interactive API documentation via Swagger UI and ReDoc, and uses type hints with Pydantic for data validation. The task builds a simple "Hello API" with two endpoints: a GET route for a greeting and a POST route that echoes JSON input.

## Files Included
- `day4.py`: The main FastAPI application script containing the API endpoints.
- `day4_README.md`: This comprehensive guide with setup, usage, and explanations.

## Prerequisites
- Python 3.7 or higher installed on your system (check with `python --version`).
- Install required libraries: Run `pip install fastapi uvicorn[standard]` in your terminal. This installs FastAPI and Uvicorn (an ASGI server for running the app). If using a virtual environment (recommended, e.g., activate `ai-env` if present), install within it.
- Basic knowledge of Python and HTTP requests (GET/POST).

## Step-by-Step Guide

### 1. Setup
- Ensure you are in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning/python-learning`.
- Verify `day4.py` is present in the directory.
- If not already done, install dependencies: Open a terminal and run:
  ```
  pip install fastapi uvicorn[standard]
  ```
  - Expected output: Successful installation messages for fastapi, uvicorn, and dependencies like starlette and pydantic.

### 2. Running the Script
- Open a terminal in VSCode or your system terminal.
- Navigate to the project directory (if not already there).
- Start the server with Uvicorn in reload mode (auto-restarts on code changes):
  ```
  uvicorn day4:app --reload
  ```
  - Expected output: Server starts on `http://127.0.0.1:8000` (or `http://localhost:8000`). You'll see logs like "INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)".
- The app is now live! Do not close the terminal; keep it running to test endpoints.

### 3. Testing the Endpoints
- **GET /hello**:
  - Open a browser and visit: `http://127.0.0.1:8000/hello`.
  - Or use curl in a new terminal: `curl http://127.0.0.1:8000/hello`.
  - Expected output: `"Hello, FastAPI!"` (plain text).
- **POST /echo**:
  - Use curl to send JSON: `curl -X POST "http://127.0.0.1:8000/echo" -H "Content-Type: application/json" -d '{"message": "Hello, World!", "number": 42}'`.
  - Expected output: The same JSON echoed back, e.g., `{"message": "Hello, World!", "number": 42}`.
- Test with different JSON payloads to verify echoing.

### 4. Accessing Swagger UI & ReDoc
- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` in your browser. This interactive interface allows you to:
  - View all endpoints (/hello and /echo).
  - See request/response schemas.
  - Test endpoints directly: Click "Try it out" for /hello (no input needed) or /echo (enter JSON in the request body).
  - Expand sections for detailed descriptions and examples.
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc` for a cleaner, documentation-focused view of the API.
- These are auto-generated from your FastAPI code—no extra setup required!

### 5. Code Explanation
- **Imports**: `from fastapi import FastAPI, Request` – FastAPI for the app, Request for handling POST body.
- **App Creation**: `app = FastAPI(...)` – Initializes the FastAPI instance with metadata for docs.
- **GET /hello Endpoint**: Simple async function returning a string. Demonstrates basic routing.
- **POST /echo Endpoint**: Async function parsing JSON from the request and returning it. Shows body handling.
- **Async Usage**: Functions are `async` to support FastAPI's async capabilities, even if not strictly needed here for simplicity.
- **Why Async?**: FastAPI uses async for non-blocking operations, improving performance under load (e.g., multiple concurrent requests).

### 6. Customization
- **Add More Endpoints**: In `day4.py`, add new routes like `@app.get("/info")` returning app details.
- **Change Responses**: Modify return values, e.g., make /hello return JSON: `return {"greeting": "Hello, FastAPI!"}`.
- **Add Validation**: For /echo, use Pydantic models for strict JSON schemas (e.g., require specific fields).
- **Change Port/Host**: Run with `uvicorn day4:app --reload --host 0.0.0.0 --port 8080` for different binding.

### 7. Troubleshooting
- **Import Errors**: Ensure FastAPI/Uvicorn are installed (`pip list` to check). If issues, try `pip install --upgrade fastapi uvicorn`.
- **Server Won't Start**: Check for port conflicts (e.g., if 8000 is in use, change port). Error: "Address already in use" – kill other processes or use a different port.
- **Endpoint Errors**: For POST, ensure JSON is valid (e.g., no trailing commas). Check terminal logs for FastAPI errors.
- **Browser Issues**: Clear cache or use incognito. For POST, use tools like Postman instead of browser.
- **Async Warnings**: If using older Python, ensure 3.7+. No issues expected here.
- **General**: Stop the server with CTRL+C, make changes, and restart.

## Learning Outcomes
- Understood FastAPI's async nature for high-performance APIs.
- Learned to create and run APIs with Uvicorn.
- Practiced defining GET and POST routes with proper handling.
- Explored automatic documentation via Swagger UI and ReDoc for testing and sharing APIs.

## Next Steps
- Experiment with more endpoints, query parameters, or path variables (e.g., `@app.get("/hello/{name}")`).
- Integrate databases or authentication in future days.
- Build on this for full CRUD APIs or deploy to cloud services.
