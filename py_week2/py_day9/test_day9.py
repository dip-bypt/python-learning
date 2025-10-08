import pytest
from fastapi.testclient import TestClient
from pipeline_api import API

client = TestClient(API)

def test_summarize():
    response = client.post("/summarize", json={"topic": "Artificial intelligence"})
    assert response.status_code == 200
    result = response.json()
    assert "summary" in result
    assert isinstance(result["summary"], str)

def test_translate():
    response = client.post("/translate", json={"text": "Hello, how are you?"})
    assert response.status_code == 200
    result = response.json()
    assert "translation" in result
    assert isinstance(result["translation"], str)

def test_qa():
    response = client.post("/qa", json={"question": "What is AI?", "topic": "Artificial intelligence"})
    assert response.status_code == 200
    result = response.json()
    assert "answer" in result
    assert isinstance(result["answer"], str)

