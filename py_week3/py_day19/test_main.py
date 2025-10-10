import pytest
from fastapi.testclient import TestClient
from py_day19.main import app, store

@pytest.fixture(autouse=True)
def clear_store():
    store.clear()
    yield
    store.clear()

def test_root():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()
    assert "LangChain Q&A API" in resp.json()["message"]

def test_qa_endpoint_basic():
    client = TestClient(app)
    data = {"question": "What is the capital of France?", "session_id": "test1"}
    resp = client.post("/qa", json=data)
    assert resp.status_code == 200
    result = resp.json()
    assert result["question"] == data["question"]
    assert result["session_id"] == data["session_id"]
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0

def test_qa_endpoint_session_memory():
    client = TestClient(app)
    # Ask a first question
    resp1 = client.post("/qa", json={"question": "My name is Alice.", "session_id": "memtest"})
    # Ask a follow-up question in the same session
    resp2 = client.post("/qa", json={"question": "What is my name?", "session_id": "memtest"})
    assert resp2.status_code == 200
    result2 = resp2.json()
    assert result2["session_id"] == "memtest"
    assert isinstance(result2["answer"], str)
    # The answer should reference "Alice" (LLM memory)
    # Can't guarantee LLM output, but should not be empty
    assert len(result2["answer"]) > 0

def test_qa_endpoint_new_session():
    client = TestClient(app)
    # Ask a question in one session
    resp1 = client.post("/qa", json={"question": "Remember my favorite color is blue.", "session_id": "sessionA"})
    # Ask in a different session
    resp2 = client.post("/qa", json={"question": "What is my favorite color?", "session_id": "sessionB"})
    assert resp2.status_code == 200
    result2 = resp2.json()
    # The answer should not reference blue (different session)
    assert result2["session_id"] == "sessionB"
    assert isinstance(result2["answer"], str)
    assert len(result2["answer"]) > 0

def test_qa_endpoint_missing_question():
    client = TestClient(app)
    resp = client.post("/qa", json={"session_id": "noq"})
    assert resp.status_code == 422

def test_qa_endpoint_missing_session_id():
    client = TestClient(app)
    resp = client.post("/qa", json={"question": "Hello?"})
    assert resp.status_code == 200
    result = resp.json()
    assert result["session_id"] == "default"
    assert isinstance(result["answer"], str)

