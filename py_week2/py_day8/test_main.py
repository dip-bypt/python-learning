import pytest
from fastapi.testclient import TestClient
from main import API, sentiment_analyzer

# Test the sentiment_analyzer directly
@pytest.mark.parametrize("sentence,expected_label", [
    ("I love learning FastAPI and Python!", "POSITIVE"),
    ("This project is so difficult and frustrating.", "NEGATIVE"),
    ("The weather today is okay, nothing special.", None)  # Could be POSITIVE or NEGATIVE depending on model
])
def test_sentiment_analyzer(sentence, expected_label):
    result = sentiment_analyzer(sentence)
    assert isinstance(result, list)
    assert 'label' in result[0]
    assert 'score' in result[0]
    if expected_label:
        assert result[0]['label'] == expected_label

# Test the FastAPI endpoint
client = TestClient(API)

def test_predict_sentiment():
    data = {"text": "I love learning FastAPI and Python!"}
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == data["text"]
    assert result["sentiment"] == "POSITIVE"
    assert 0.0 <= result["confidence"] <= 1.0

    data = {"text": "This project is so difficult and frustrating."}
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["sentiment"] == "NEGATIVE"
    assert 0.0 <= result["confidence"] <= 1.0

    data = {"text": "The weather today is okay, nothing special."}
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "sentiment" in result
    assert 0.0 <= result["confidence"] <= 1.0

