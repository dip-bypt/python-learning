#!/usr/bin/env python3
"""
Day 7: Mini CRUD API - Book Manager with FastAPI + SQLite

This script demonstrates a mini CRUD API for managing books using FastAPI and SQLite with SQLModel ORM.
It includes endpoints for listing books (GET), adding books (POST), and deleting books by ID (DELETE).

Key Features:
- SQLModel ORM: For defining the Book model, creating tables, and performing CRUD operations.
- SQLite Database: Persistent storage in books.db file.
- FastAPI Endpoints: Typed requests/responses with automatic Swagger documentation.
- Path Parameters: For DELETE /books/{id}.
- HTTP Status Codes: 201 for creation, 200 for retrieval, 404 for not found, 204 for deletion.
- Validation: Pydantic-based via SQLModel for title and author.

Endpoints:
- GET /books: Retrieves all books from the database.
- POST /books: Creates a new book from JSON {title, author}.
- DELETE /books/{id}: Deletes a book by its ID.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List

# SQLModel model for Book data (defines the database table)
class Book(SQLModel, table=True):
    """
    SQLModel model for book data.

    Represents a book with id (auto-generated), title, and author.
    Used for database table creation and Pydantic validation in requests/responses.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str

# SQLite database engine (creates books.db file in current directory)
engine = create_engine("sqlite:///./books.db", echo=True)  # echo=True for SQL logging

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
    title="Book Manager API",
    description="A mini CRUD API for managing books with FastAPI and SQLite using SQLModel ORM for Day 7.",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    """
    Event handler for application startup.
    Initializes the database and creates tables if they don't exist.
    """
    create_db_and_tables()

@app.get("/books", response_model=List[Book])
def get_books(session: Session = Depends(get_session)):
    """
    GET endpoint to retrieve all books.

    Queries the SQLite database for all books and returns them as a list.

    Args:
        session (Session): Database session dependency.

    Returns:
        List[Book]: List of all books in the database.
    """
    books = session.exec(select(Book)).all()
    return books

@app.post("/books", response_model=Book, status_code=201)
def create_book(book: Book, session: Session = Depends(get_session)):
    """
    POST endpoint to create a new book.

    Accepts JSON with {title, author}, validates via SQLModel/Pydantic,
    inserts into SQLite database, and returns the created book with generated id.

    Args:
        book (Book): The book data from the request body.
        session (Session): Database session dependency.

    Returns:
        Book: The created book data including auto-generated id.
    """
    session.add(book)
    session.commit()
    session.refresh(book)  # Refresh to get the auto-generated id
    return book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    """
    DELETE endpoint to remove a book by ID.

    Finds the book by ID, deletes it from the database if found.
    Returns 404 if book not found, 204 on successful deletion.

    Args:
        book_id (int): The ID of the book to delete from the URL path.
        session (Session): Database session dependency.

    Raises:
        HTTPException: 404 if book not found.
    """
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return None
