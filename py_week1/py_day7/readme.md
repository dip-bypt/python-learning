# Mini CRUD API Project: Book Manager (py_day7)

## Session Overview
This session focused on building a complete CRUD API using FastAPI and SQLite, covering:
- **FastAPI for API development**
- **SQLite for persistent storage**
- **CRUD operations (Create, Read, Delete)**
- **Testing with Swagger UI and Postman**

---

## Project: Book Manager API

### Endpoints Implemented
- **GET /books**: List all books in the database.
- **POST /books**: Add a new book (title, author, year).
- **DELETE /books/{id}**: Delete a book by its ID.

### Database
- All book records are stored in a local SQLite database (`books.db`).
- The table `books` is created automatically if it does not exist.

---

## Code Review: `main.py`
- **Book Model**: Pydantic model with `title`, `author`, and `year` fields.
- **Database Initialization**: On startup, creates the `books` table if needed.
- **GET /books**: Fetches all books and returns them as a list of dictionaries.
- **POST /books**: Inserts a new book and returns a success message with the new book's ID.
- **DELETE /books/{book_id}**: Deletes a book by ID, returns a message or 404 if not found.

---

## How to Run
1. **Install dependencies** (in your virtual environment):
   ```bash
   pip install fastapi uvicorn
   ```
2. **Run the API server**:
   ```bash
   uvicorn py_week1.py_day7.main:API --reload
   ```
   OR
   ```bash
    py_week1/ai-env/bin/python -m uvicorn py_week1.py_day7.main:API --reload
    ```
3. **Access API docs**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Example Requests

### Add a Book
```
POST http://127.0.0.1:8000/books
Content-Type: application/json
{
  "title": "The Pragmatic Programmer",
  "author": "Andrew Hunt",
  "year": 1999
}
Response: { "message": "Book added successfully", "id": 1 }
```

### List All Books
```
GET http://127.0.0.1:8000/books
Response: {
  "books": [
    { "id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "year": 1999 },
    ...
  ]
}
```

### Delete a Book
```
DELETE http://127.0.0.1:8000/books/1
Response: { "message": "Book with ID 1 deleted successfully" }
```

---

## Notes
- The database file `books.db` is created in the project directory.
- All data persists between server restarts.
- Test the API using Swagger UI or Postman for interactive exploration.

---

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [sqlite3 Python Docs](https://docs.python.org/3/library/sqlite3.html)

