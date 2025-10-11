import io
import pytest
from fastapi.testclient import TestClient
from py_day17.main import app

# Helper to create a minimal PDF in memory
def create_pdf(content="Hello PDF!"):
    from reportlab.pdfgen import canvas
    pdf_bytes = io.BytesIO()
    c = canvas.Canvas(pdf_bytes)
    c.drawString(100, 750, content)
    c.save()
    pdf_bytes.seek(0)
    return pdf_bytes

client = TestClient(app)

def test_summarize_pdf_valid():
    pdf_file = create_pdf("This is a test PDF for summarization.")
    response = client.post(
        "/summarize-pdf",
        files={"file": ("test.pdf", pdf_file, "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)
    assert len(data["summary"]) > 0

def test_summarize_pdf_invalid_file():
    fake_file = io.BytesIO(b"not a pdf")
    response = client.post(
        "/summarize-pdf",
        files={"file": ("test.txt", fake_file, "text/plain")}
    )
    # Should raise error or return 422/400
    assert response.status_code in (400, 422, 500)

def test_summarize_pdf_empty_pdf():
    empty_pdf = create_pdf("")
    response = client.post(
        "/summarize-pdf",
        files={"file": ("empty.pdf", empty_pdf, "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)

def test_summarize_pdf_missing_file():
    response = client.post("/summarize-pdf", files={})
    assert response.status_code == 422
