# Day 7: Mini CRUD API - Book Manager with FastAPI + SQLite

## Overview
This project implements a mini CRUD API for managing books using FastAPI and SQLite with SQLModel ORM. It supports listing all books (GET /books), adding new books (POST /books), and deleting books by ID (DELETE /books/{id}). The API uses SQLite for persistent storage in a `books.db` file. SQLModel handles ORM and validation, with automatic Swagger documentation for testing.

## Files Included
- `day7.py`: The main FastAPI application script with Book model, database setup, and CRUD endpoints.
- `day7_README.md`: This comprehensive guide with setup, usage, testing (Swagger & Postman), and explanations.

## Prerequisites
- Python 3.7 or higher installed (check with `python --version`).
- Install required libraries: Run `pip install sqlmodel uvicorn[standard]` (includes SQLAlchemy, Pydantic, FastAPI). If using a virtual environment (e.g., `ai-env`), install within it. Dependencies are shared with previous days.
- Basic knowledge of FastAPI, JSON, HTTP methods, databases, and tools like curl, Swagger, or Postman.
- Postman (optional, for GUI testing): Download from https://www.postman.com/downloads/ if needed.

## Step-by-Step Guide

### 1. Setup
- Ensure you're in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning/python-learning`.
- Verify `day7.py` is present.
- Install dependencies if not already done: `pip install sqlmodel uvicorn[standard]`.
- The SQLite database file `books.db` will be created automatically on first run.

### 2. Running the Script
- Open a terminal and navigate to the directory.
- Start the server: `uvicorn day7:app --reload`.
- Server runs on `http://127.0.0.1:8000`. Logs confirm startup and table creation (due to `echo=True`).

### 3. Testing the Endpoints
Use curl for command-line testing or Postman/Swagger for GUI. Initially, GET /books returns an empty list `[]`.

- **GET /books** (List all books):
  - Curl: `curl "http://127.0.0.1:8000/books"`.
  - Expected: 200 OK, JSON array of books, e.g., `[{"id": 1, "title": "1984", "author": "George Orwell"}]`.
  - Postman: GET request to `http://127.0.0.1:8000/books`.

- **POST /books** (Add a book):
  - Curl: `curl -X POST "http://127.0.0.1:8000/books" -H "Content-Type: application/json" -d '{"title": "1984", "author": "George Orwell"}'`.
  - Expected: 201 Created, JSON `{"id": 1, "title": "1984", "author": "George Orwell"}`.
  - Test validation: Missing title returns 422 Unprocessable Entity.
  - Postman: POST to `http://127.0.0.1:8000/books`, Body > raw > JSON with `{"title": "Test Book", "author": "Test Author"}`.

- **DELETE /books/{id}** (Delete a book by ID):
  - Curl: `curl -X DELETE "http://127.0.0.1:8000/books/1"`.
  - Expected: 204 No Content on success; 404 Not Found if ID doesn't exist.
  - Postman: DELETE to `http://127.0.0.1:8000/books/1` (replace 1 with actual ID from POST).

Add multiple books, list them, then delete one and list again to verify.

### 4. Accessing Swagger UI & ReDoc
- Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.
  - GET /books: Click "Try it out", execute to see list.
  - POST /books: Enter JSON in schema, execute to add.
  - DELETE /books/{id}: Enter ID, execute to delete.
- ReDoc at `http://127.0.0.1:8000/redoc` for readable docs.
- Book model appears as schema for validation and auto-generated docs.

### 5. Testing with Postman
- Create a new collection "Book Manager API".
- Add requests:
  - GET `http://127.0.0.1:8000/books` (no body).
  - POST `http://127.0.0.1:8000/books` (Headers: Content-Type application/json; Body: raw JSON `{"title": "Fahrenheit 451", "author": "Ray Bradbury"}`).
  - DELETE `http://127.0.0.1:8000/books/{{book_id}}` (use variable for ID from POST response).
- Run collection to test full CRUD flow.
- Check response codes, bodies, and headers for correctness.

### 6. Code Explanation
- **SQLModel Model**: `Book` class defines table with `id` (primary key), `title` (str), `author` (str).
- **Database Setup**: `create_engine` for SQLite, `create_db_and_tables` on startup.
- **Session Dependency**: `get_session` provides DB session per request.
- **Endpoints**:
  - GET: Queries all books with `select(Book).all()`.
  - POST: Adds and commits new book, refreshes for ID.
  - DELETE: Fetches by ID with `session.get`, deletes if found, raises 404 otherwise.
- **Validation & Responses**: SQLModel/Pydantic ensures typed inputs/outputs; status codes for CRUD.

### 7. Customization
- Add fields to Book (e.g., `isbn: str`, `year: int`).
- Implement PUT /books/{id} for updates.
- Add query params to GET (e.g., ?author=Orwell to filter).
- Seed initial data in `on_startup`.
- Switch to PostgreSQL by updating engine URL.

### 8. Troubleshooting
- Import errors: Verify `pip install sqlmodel`.
- Database issues: Check `books.db` created; delete to reset.
- Validation errors: Ensure JSON has required fields (422 response).
- 404 on DELETE: Confirm ID exists (use GET first).
- Server issues: Port 8000 free? Restart with `--reload`.
- Swagger/Postman: Refresh page/app; check console for errors.
- No output from curl: Server running? Check logs.

## Learning Outcomes
- Built a full CRUD API (Create, Read, Delete) with FastAPI + SQLite.
- Used SQLModel for ORM, validation, and table management.
- Tested with Swagger UI and Postman for end-to-end verification.

## Next Steps
- Add authentication (e.g., JWT).
- Implement full CRUD (add PUT).
- Deploy to Heroku/Vercel with PostgreSQL.
- Explore advanced features like pagination or relationships.
