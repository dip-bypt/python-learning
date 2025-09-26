import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

API = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    year: int


def init_db():
    conn = sqlite3.connect("books.db")  # Connect to SQLite database (creates file if not exists)
    cur = conn.cursor() # Create a cursor object to execute SQL commands. Return a cursor for the connection.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """) # Create the books table if it doesn't exist. Executes an SQL statement.
    conn.commit() # Commit any pending transaction to the database.
    conn.close() # Close the database connection.

init_db()


@API.get("/books")
async def get_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, author, year FROM books")
    rows = cur.fetchall()
    conn.close()

    books = [{"id": r[0], "title": r[1], "author": r[2], "year": r[3]} for r in rows]
    return {"books": books}


@API.post("/books")
async def add_book(book: Book):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        (book.title, book.author, book.year)
    )
    conn.commit()
    book_id = cur.lastrowid
    conn.close()

    return {"message": "Book added successfully", "id": book_id}


@API.delete("/books/{book_id}")
async def delete_book(book_id: int):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": f"Book with ID {book_id} deleted successfully"}
