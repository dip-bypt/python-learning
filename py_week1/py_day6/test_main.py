import unittest
import os
import sqlite3
from fastapi.testclient import TestClient
from py_week1.py_day6.main import API, init_db

test_db = "test_todo.db"

def setup_test_db():
    # Use a separate DB for testing
    if os.path.exists(test_db):
        os.remove(test_db)
    conn = sqlite3.connect(test_db)
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

class TestPyDay6(unittest.TestCase):
    def setUp(self):
        setup_test_db()
        # Patch the DB path in the API to use the test DB
        self._orig_connect = sqlite3.connect
        sqlite3.connect = lambda path=None: self._orig_connect(test_db)
        self.client = TestClient(API)

    def tearDown(self):
        sqlite3.connect = self._orig_connect
        if os.path.exists(test_db):
            os.remove(test_db)

    def test_add_task(self):
        data = {"title": "Test Task", "description": "Test Desc"}
        response = self.client.post("/task", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Task added successfully", response.text)

    def test_list_tasks(self):
        # Add two tasks
        self.client.post("/task", json={"title": "Task1", "description": "Desc1"})
        self.client.post("/task", json={"title": "Task2"})
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 200)
        tasks = response.json()["tasks"]
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["title"], "Task1")
        self.assertEqual(tasks[1]["title"], "Task2")

    def test_add_task_title_only(self):
        data = {"title": "Title Only"}
        response = self.client.post("/task", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Task added successfully", response.text)
        # Check it appears in GET /tasks
        response = self.client.get("/tasks")
        tasks = response.json()["tasks"]
        self.assertTrue(any(t["title"] == "Title Only" for t in tasks))

if __name__ == "__main__":
    unittest.main()

