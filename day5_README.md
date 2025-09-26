# Day 5: Pydantic Models + Query/Path Params

## Overview
This project introduces Pydantic models for data validation, path parameters for dynamic URLs, query parameters for optional inputs, response models for typed outputs, and HTTP status codes in FastAPI. The API manages users: POST /user creates a user from validated JSON {name, age}, and GET /user/{name} retrieves user info using path params (with optional query param for details). Validation ensures name is non-empty and age is positive. In-memory storage simulates a database.

## Files Included
- `day5.py`: The main FastAPI application script with user endpoints and Pydantic models.
- `day5_README.md`: This comprehensive guide with setup, usage, and explanations.

## Prerequisites
- Python 3.7 or higher installed (check with `python --version`).
- Install required libraries: Run `pip install fastapi uvicorn[standard]` (includes Pydantic). If using a virtual environment (e.g., activate `ai-env`), install within it.
- Basic knowledge of FastAPI, JSON, and HTTP methods.

## Step-by-Step Guide

### 1. Setup
- Ensure you're in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning/python-learning`.
- Verify `day5.py` is present.
- Install dependencies if not done: `pip install fastapi uvicorn[standard]`.

### 2. Running the Script
- Open a terminal and navigate to the directory.
- Start the server: `uvicorn day5:app --reload`.
- Server runs on `http://127.0.0.1:8000`. Logs confirm startup.

### 3. Testing the Endpoints
- **POST /user**:
  - Curl: `curl -X POST "http://127.0.0.1:8000/user" -H "Content-Type: application/json" -d '{"name": "Alice", "age": 25}'`.
  - Expected: 201 Created, JSON `{"name": "Alice", "age": 25}`.
  - Test validation: Invalid age (e.g., -1) returns 422 Unprocessable Entity.
  - Duplicate name: 409 Conflict.
- **GET /user/{name}**:
  - Curl: `curl "http://127.0.0.1:8000/user/Alice"`.
  - Expected: 200 OK, user JSON.
  - Non-existent: 404 Not Found.
  - With query: `curl "http://127.0.0.1:8000/user/Alice?details=full"` (same output for now).

### 4. Accessing Swagger UI & ReDoc
- Visit `http://127.0.0.1:8000/docs`.
- POST /user: Expand, click "Try it out", enter JSON in schema field, execute.
- GET /user/{name}: Enter name in path, optional query, execute.
- ReDoc at `/redoc` for docs view.
- Models appear as schemas for validation and docs.

### 5. Code Explanation
- **Pydantic Model**: `User` class validates name (str, non-empty) and age (int >0).
- **Path Params**: `{name}` in GET route captures URL part.
- **Query Params**: `details` optional in GET (demonstrates usage).
- **Response Models**: `response_model=User` ensures typed responses.
- **Status Codes**: 201 for creation, 404 for not found, 409 for conflict.
- **Storage**: `users` dict for simplicity.

### 6. Customization
- Add fields to User (e.g., email).
- Implement query param logic (e.g., details=full adds extra data).
- Replace dict with a real DB (e.g., SQLAlchemy).
- Add more endpoints (PUT for update, DELETE).

### 7. Troubleshooting
- Validation errors: Check JSON matches schema (422 response).
- 404/409: Expected for missing/duplicate users.
- Server issues: Ensure port 8000 free, deps installed.
- Swagger: Refresh if schemas don't load.

## Learning Outcomes
- Mastered Pydantic for validation and schemas.
- Used path/query params in routes.
- Applied response models and status codes.

## Next Steps
- Integrate databases or add authentication.
- Explore advanced Pydantic features.
