import unittest
from fastapi.testclient import TestClient
from py_week1.py_day5.main import API, users_db

class TestPyDay5(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(API)
        users_db.clear()  # Ensure a clean DB for each test

    def test_create_user_success(self):
        data = {"email": "a@b.com", "name": "Alice", "age": 25}
        response = self.client.post("/user", json=data)
        self.assertEqual(response.status_code, 201)
        resp_json = response.json()
        self.assertTrue(resp_json["success"])
        self.assertEqual(resp_json["user"]["email"], "a@b.com")
        self.assertEqual(resp_json["user"]["name"], "Alice")
        self.assertEqual(resp_json["user"]["age"], 25)

    def test_create_user_duplicate_email(self):
        data = {"email": "a@b.com", "name": "Alice", "age": 25}
        self.client.post("/user", json=data)
        response = self.client.post("/user", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already registered", response.text)

    def test_get_user_success(self):
        data = {"email": "a@b.com", "name": "Alice", "age": 25}
        self.client.post("/user", json=data)
        response = self.client.get("/user/a@b.com")
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertTrue(resp_json["success"])
        self.assertEqual(resp_json["user"]["email"], "a@b.com")

    def test_get_user_not_found(self):
        response = self.client.get("/user/unknown@b.com")
        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.text)

if __name__ == "__main__":
    unittest.main()

