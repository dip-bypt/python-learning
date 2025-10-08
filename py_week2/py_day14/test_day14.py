import importlib.util
import os
import pytest
from fastapi.testclient import TestClient

spec = importlib.util.spec_from_file_location("app", os.path.join(os.path.dirname(__file__), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
API = app_module.API


def test_root():
    client = TestClient(API)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "available_routes" in data
    assert "/sentiment" in data["available_routes"]
    assert "/summary" in data["available_routes"]

def test_sentiment():
    client = TestClient(API)
    data = {"text": "I love learning FastAPI!"}
    response = client.post("/sentiment", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "sentiment" in result
    assert "confidence" in result

def test_summary():
    client = TestClient(API)
    data = {"text": "FastAPI is a modern, fast web framework for building APIs with Python."}
    response = client.post("/summary", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "summary" in result
