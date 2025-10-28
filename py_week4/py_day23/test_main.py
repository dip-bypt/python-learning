from fastapi.testclient import TestClient
from main import app, API_KEY, API_KEY_NAME

client = TestClient(app)

def test_root_endpoint():
    """Test if root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_qa_with_valid_api_key():
    """Test QA endpoint with valid API key"""
    response = client.get(
        "/qa",
        params={"question": "Hello"},
        headers={API_KEY_NAME: API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Hello"
    assert data["answer"] == "olleH"

def test_qa_with_invalid_api_key():
    """Test QA endpoint with invalid API key"""
    response = client.get(
        "/qa",
        params={"question": "Hello"},
        headers={API_KEY_NAME: "wrong-key"}
    )
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized - Invalid API Key"

def test_qa_without_api_key():
    """Test QA endpoint without API key"""
    response = client.get("/qa", params={"question": "Hello"})
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized - Invalid API Key"
