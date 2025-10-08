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
    assert "message" in response.json()

def test_analyze():
    client = TestClient(API)
    data = {"text": "I love learning FastAPI!"}
    response = client.post("/analyze", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == data["text"]
    assert "sentiment" in result
    assert 0.0 <= result["confidence"] <= 1.0
