import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

API = FastAPI()

class Task(BaseModel):
    title: str
    description: str | None = None

def init_db():
    conn = sqlite3.connect("todo.db")   # creates file if not exists
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # run when API starts

@API.post("/task")
async def add_task(task: Task):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (task.title, task.description)
    )
    conn.commit()
    conn.close()
    return {"message": "Task added successfully"}

@API.get("/tasks")
async def list_tasks():
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, description FROM tasks")
    rows = cur.fetchall()
    conn.close()

    # convert rows → dicts
    tasks = [{"id": row[0], "title": row[1], "description": row[2]} for row in rows]
    return {"tasks": tasks}
