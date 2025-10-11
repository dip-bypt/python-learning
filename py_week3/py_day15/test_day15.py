import pytest
from fastapi.testclient import TestClient
from py_day15.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "LangChain Polite Rewriter API" in response.json()["message"]

def test_rewrite_valid():
    data = {"sentence": "Close the door."}
    response = client.post("/rewrite", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["original_sentence"] == data["sentence"]
    assert isinstance(result["polite_version"], str)
    assert len(result["polite_version"]) > 0

def test_rewrite_empty():
    data = {"sentence": ""}
    response = client.post("/rewrite", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["original_sentence"] == ""
    assert isinstance(result["polite_version"], str)

def test_rewrite_missing_field():
    response = client.post("/rewrite", json={})
    assert response.status_code == 422

def test_rewrite_non_string():
    data = {"sentence": 123}
    response = client.post("/rewrite", json=data)
    assert response.status_code == 422

