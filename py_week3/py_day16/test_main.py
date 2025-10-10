import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure the app can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Sequential Chain API" in response.json()["message"]

def test_analyze_text_basic():
    data = {"text": "Python is a popular programming language for AI and data science."}
    response = client.post("/analyze", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "original_text" in result
    assert "summary" in result
    assert "keywords" in result
    assert isinstance(result["keywords"], list)
    assert len(result["keywords"]) >= 1

def test_analyze_text_empty():
    data = {"text": ""}
    response = client.post("/analyze", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["original_text"] == ""
    assert isinstance(result["summary"], str)
    assert isinstance(result["keywords"], list)

def test_analyze_text_long():
    long_text = "Python is a versatile language. " * 50
    data = {"text": long_text}
    response = client.post("/analyze", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["original_text"] == long_text
    assert isinstance(result["summary"], str)
    assert isinstance(result["keywords"], list)

