"""
Day 6: FastAPI + SQLite To-Do API

This script creates a FastAPI app with SQLite integration for a simple To-Do list.
- POST /task: Add a new task to the database
- GET /tasks: List all tasks

Uses Python's built-in sqlite3 module for database operations.
"""

import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Database setup
DB_NAME = "day6/todo.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# FastAPI app
app = FastAPI()

# Pydantic model for task input
class TaskIn(BaseModel):
    description: str

# Pydantic model for task output
class TaskOut(BaseModel):
    id: int
    description: str

@app.post("/task", response_model=TaskOut, status_code=201)
def add_task(task: TaskIn):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (description) VALUES (?)", (task.description,))
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return {"id": task_id, "description": task.description}

@app.get("/tasks", response_model=List[TaskOut])
def list_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, description FROM tasks")
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "description": row[1]} for row in rows]
