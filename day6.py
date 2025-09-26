#!/usr/bin/env python3
"""
Day 6: SQLite + FastAPI - To-Do API

This script demonstrates integrating SQLite database with FastAPI using SQLModel ORM.
It builds a simple To-Do API with table creation, row insertion, and database-backed endpoints.

Key Features:
- SQLModel ORM: For defining models, creating tables, and interacting with SQLite.
- Table Creation: Automatic table setup on startup.
- Row Insertion: Adding tasks via POST endpoint.
- FastAPI Integration: Endpoints for creating and listing tasks with proper validation.
- SQLite Basics: Uses sqlite3 under the hood via SQLAlchemy.
- Response Models: Typed responses for consistency and automatic Swagger documentation.
- Status Codes: Proper HTTP codes (201 Created, 200 OK).

Endpoints:
- POST /task: Creates a new task from JSON {title, description?, done?}.
- GET /tasks: Retrieves all tasks from the database.
"""

from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

# SQLModel model for Task data (defines the database table)
class Task(SQLModel, table=True):
    """
    SQLModel model for task data.

    Represents a to-do item with id (auto-generated), title, optional description, and done status.
    Used for database table creation and Pydantic validation in requests/responses.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    done: bool = False

# SQLite database engine (creates todo.db file in current directory)
engine = create_engine("sqlite:///./todo.db", echo=True)  # echo=True for SQL logging

def create_db_and_tables():
    """
    Creates the database tables based on SQLModel definitions.
    Called on application startup.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency to provide a database session for each request.
    Yields a Session instance, automatically closed after use.
    """
    with Session(engine) as session:
        yield session

# Create the FastAPI application instance
# This instance will be used by Uvicorn to run the server
app = FastAPI(
    title="To-Do API",
    description="A simple FastAPI example demonstrating SQLite integration with SQLModel ORM for Day 6.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """
    Event handler for application startup.
    Initializes the database and creates tables if they don't exist.
    """
    create_db_and_tables()

@app.post("/task", response_model=Task, status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    """
    POST endpoint to create a new task.

    Accepts JSON with {title, description?, done?}, validates via SQLModel/Pydantic,
    inserts into SQLite database, and returns the created task with generated id.

    Args:
        task (Task): The task data from the request body.
        session (Session): Database session dependency.

    Returns:
        Task: The created task data including auto-generated id.
    """
    session.add(task)
    session.commit()
    session.refresh(task)  # Refresh to get the auto-generated id
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks(session: Session = Depends(get_session)):
    """
    GET endpoint to retrieve all tasks.

    Queries the SQLite database for all tasks and returns them as a list.

    Args:
        session (Session): Database session dependency.

    Returns:
        List[Task]: List of all tasks in the database.
    """
    tasks = session.exec(select(Task)).all()
    return tasks
