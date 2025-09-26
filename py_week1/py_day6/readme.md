# SQLite + FastAPI To-Do API (py_day6)

## Session Overview
This session focused on integrating SQLite with FastAPI to build a persistent backend API:

- **sqlite3 basics / SQLModel ORM**: Using SQLite for lightweight, file-based databases.
- **Create table & insert rows**: Table creation and data insertion with SQL.
- **Integrate DB into FastAPI endpoints**: Connecting database logic to API routes.

---

## Tasks Completed

### 1. Build To-Do API
- **POST /task**: Add a new task to the SQLite database.
- **GET /tasks**: List all tasks from the database.

---

## Code Review: `main.py`
- **Database Initialization**: On startup, creates a `tasks` table in `todo.db` if it doesn't exist.
- **Task Model**: Uses Pydantic for request validation (`title`, optional `description`).
- **POST /task**:
  - Accepts a JSON body for a new task.
  - Inserts the task into the database.
  - Returns a success message.
- **GET /tasks**:
  - Fetches all tasks from the database.
  - Returns a list of tasks as JSON objects.

---

## How to Run
1. **Install dependencies** (in your virtual environment):
   ```bash
   pip install fastapi uvicorn
   ```
2. **Run the API server**:
   ```bash
   uvicorn py_week1.py_day6.main:API --reload
   ```
   OR
   ```bash
    py_week1/ai-env/bin/python -m uvicorn py_week1.py_day6.main:API --reload
    ```
3. **Access API docs**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Example Requests

### POST /task
```
POST http://127.0.0.1:8000/task
Content-Type: application/json
{
  "title": "Buy groceries",
  "description": "Milk, Bread, Eggs"
}
Response: { "message": "Task added successfully" }
```

### GET /tasks
```
GET http://127.0.0.1:8000/tasks
Response: {
  "tasks": [
    { "id": 1, "title": "Buy groceries", "description": "Milk, Bread, Eggs" },
    ...
  ]
}
```

---

## Notes
- The database file `todo.db` is created in the project directory.
- All data persists between server restarts.
- The code uses Python's built-in `sqlite3` module for simplicity.

---

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [sqlite3 Python Docs](https://docs.python.org/3/library/sqlite3.html)

