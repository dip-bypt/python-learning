# Day 6: SQLite + FastAPI - To-Do API

## Overview
This project demonstrates integrating SQLite database with FastAPI using SQLModel ORM. It creates a to-do list API with table creation, row insertion, and database-backed endpoints. The API allows adding tasks via POST /task and listing all tasks via GET /tasks. Uses SQLModel for ORM (object-relational mapping) with Pydantic validation, built on SQLAlchemy and sqlite3.

## Files Included
- `day6.py`: The main FastAPI application script with To-Do API endpoints, SQLModel Task model, and SQLite database integration.
- `day6_README.md`: This comprehensive guide with setup, usage, and explanations.

## Prerequisites
- Python 3.7 or higher installed (check with `python --version`).
- Install required libraries: Run `pip install sqlmodel uvicorn[standard]` (includes SQLAlchemy, Pydantic, and FastAPI dependencies). If using a virtual environment (e.g., activate `ai-env`), install within it.
- Basic knowledge of FastAPI, JSON, HTTP methods, and databases.

## Step-by-Step Guide

### 1. Setup
- Ensure you're in the project directory: `/Users/bypti703/Documents/GENERAL_DETAILS/Python_Learning/python-learning`.
- Verify `day6.py` is present.
- Install dependencies if not done: `pip install sqlmodel uvicorn[standard]`.
- The SQLite database file `todo.db` will be created automatically in the current directory on first run.

### 2. Running the Script
- Open a terminal and navigate to the directory.
- Start the server: `uvicorn day6:app --reload`.
- Server runs on `http://127.0.0.1:8000`. Logs confirm startup and table creation (due to echo=True).

### 3. Testing the Endpoints
- **POST /task**:
  - Curl: `curl -X POST "http://127.0.0.1:8000/task" -H "Content-Type: application/json" -d '{"title": "Buy groceries", "description": "Milk and bread"}'`.
  - Expected: 201 Created, JSON `{"id": 1, "title": "Buy groceries", "description": "Milk and bread", "done": false}`.
  - Test validation: Missing title returns 422 Unprocessable Entity.
  - Add more tasks to see multiple entries.
- **GET /tasks**:
  - Curl: `curl "http://127.0.0.1:8000/tasks"`.
  - Expected: 200 OK, JSON array of tasks, e.g., `[{"id": 1, "title": "Buy groceries", "description": "Milk and bread", "done": false}]`.
  - Initially empty if no tasks added.

### 4. Accessing Swagger UI & ReDoc
- Visit `http://127.0.0.1:8000/docs`.
- POST /task: Expand, click "Try it out", enter JSON in schema field (e.g., {"title": "Test task"}), execute.
- GET /tasks: Expand, click "Try it out", execute to see list.
- ReDoc at `/redoc` for alternative docs view.
- Task model appears as schema for validation and docs.

### 5. Code Explanation
- **SQLModel Model**: `Task` class defines table with id (primary key), title (required), description (optional), done (boolean default false).
- **Database Setup**: `create_engine` for SQLite, `create_db_and_tables` on startup.
- **Session Dependency**: `get_session` provides DB session per request.
- **Endpoints**: POST inserts new task, GET queries all tasks.
- **ORM Basics**: SQLModel handles table creation, inserts, and selects automatically.

### 6. Customization
- Add fields to Task (e.g., priority: int).
- Implement PUT /task/{id} for updates, DELETE /task/{id} for deletion.
- Add query params to GET (e.g., ?done=true to filter completed tasks).
- Replace SQLite with PostgreSQL by changing engine URL.
- Add authentication or more complex logic.

### 7. Troubleshooting
- Import errors: Ensure sqlmodel is installed (`pip install sqlmodel`).
- Database issues: Check `todo.db` file created; delete to reset.
- Validation errors: Check JSON matches schema (422 response).
- Server issues: Ensure port 8000 free, deps installed.
- Swagger: Refresh if schemas don't load; check console for errors.

## Learning Outcomes
- Integrated SQLite with FastAPI using SQLModel ORM.
- Created tables and inserted rows via API endpoints.
- Used Pydantic for validation in DB models.

## Next Steps
- Add more CRUD operations (update, delete).
- Explore advanced SQLModel features like relationships.
- Deploy to production with a real database.
