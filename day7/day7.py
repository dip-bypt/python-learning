"""
Day 7: Mini CRUD API - Book Manager with FastAPI + SQLite

This script creates a FastAPI app for managing books with SQLite storage.
Endpoints:
- GET /books: List all books
- POST /books: Add a new book
- DELETE /books/{id}: Delete a book by ID

Uses Python's built-in sqlite3 module for database operations.
"""

import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Database setup
DB_NAME = "day7/books.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# FastAPI app
app = FastAPI()

# Pydantic model for book input
class BookIn(BaseModel):
    title: str
    author: str

# Pydantic model for book output
class BookOut(BaseModel):
    id: int
    title: str
    author: str

@app.post("/books", response_model=BookOut, status_code=201)
def add_book(book: BookIn):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
    book_id = c.lastrowid
    conn.commit()
    conn.close()
    return {"id": book_id, "title": book.title, "author": book.author}

@app.get("/books", response_model=List[BookOut])
def list_books():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, author FROM books")
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "author": row[2]} for row in rows]

@app.delete("/books/{id}", status_code=200)
def delete_book(id: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (id,))
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    conn.commit()
    conn.close()
    return {"message": f"Book with id {id} deleted"}
