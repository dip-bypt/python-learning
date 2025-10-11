import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from py_day21.main import app

client = TestClient(app)

def create_dummy_pdf(content="Hello World!"):
    import io
    from reportlab.pdfgen import canvas
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name)
    c.drawString(100, 750, content)
    c.save()
    temp.seek(0)
    return temp

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "LangChain Document Q&A API" in resp.json()["message"]

def test_ask_without_upload():
    resp = client.post("/ask", json={"question": "What is this?"})
    assert resp.status_code == 200
    assert "No PDF uploaded yet" in resp.json()["error"]

def test_upload_pdf_and_ask():
    temp_pdf = create_dummy_pdf("The capital of France is Paris.")
    with open(temp_pdf.name, "rb") as f:
        files = {"file": (os.path.basename(temp_pdf.name), f, "application/pdf")}
        resp = client.post("/upload_pdf", files=files)
    os.unlink(temp_pdf.name)
    assert resp.status_code == 200
    assert resp.json()["message"].endswith("uploaded and embeddings stored successfully!")
    # Now ask a question
    resp2 = client.post("/ask", json={"question": "What is the capital of France?"})
    assert resp2.status_code == 200
    assert "France" in resp2.json()["question"]
    # The answer may vary depending on LLM, so just check answer is present
    assert resp2.json()["answer"]
