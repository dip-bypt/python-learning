from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_analyze_text():
    response = client.post("/analyze", json={"text": "Hello world. This is a test."})
    data = response.json()
    assert response.status_code == 200
    assert data["word_count"] == 6
    assert data["sentence_count"] == 2
    assert "avg_word_length" in data


def test_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 200
    assert "error" in response.json()
