import unittest
import os
import sqlite3
from fastapi.testclient import TestClient
from py_week1.py_day7.main import API, init_db

test_db = "test_books.db"

def setup_test_db():
    if os.path.exists(test_db):
        os.remove(test_db)
    conn = sqlite3.connect(test_db)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class TestPyDay7(unittest.TestCase):
    def setUp(self):
        setup_test_db()
        self._orig_connect = sqlite3.connect
        sqlite3.connect = lambda path=None: self._orig_connect(test_db)
        self.client = TestClient(API)

    def tearDown(self):
        sqlite3.connect = self._orig_connect
        if os.path.exists(test_db):
            os.remove(test_db)

    def test_add_book(self):
        data = {"title": "Book1", "author": "Author1", "year": 2020}
        response = self.client.post("/books", json=data)
        self.assertEqual(response.status_code, 200)
        # Check it appears in GET /books
        response = self.client.get("/books")
        books = response.json()["books"]
        self.assertTrue(any(b["title"] == "Book1" for b in books))

    def test_list_books(self):
        self.client.post("/books", json={"title": "Book1", "author": "Author1", "year": 2020})
        self.client.post("/books", json={"title": "Book2", "author": "Author2", "year": 2021})
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        books = response.json()["books"]
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Book1")
        self.assertEqual(books[1]["title"], "Book2")

    def test_add_book_missing_field(self):
        data = {"title": "Book3", "author": "Author3"}  # Missing year
        response = self.client.post("/books", json=data)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

if __name__ == "__main__":
    unittest.main()

