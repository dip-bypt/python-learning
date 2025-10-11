import os
from fastapi.testclient import TestClient
import day21.day21 as mod


def make_dummy_pdf(tmp_path, name="doc.pdf"):
    p = tmp_path / name
    p.write_text("This is a test PDF about AI and testing.")
    return p


def test_upload_and_qa_with_fallback(monkeypatch, tmp_path):
    # Simulate uploading a PDF but make embeddings fail so fallback is used
    dummy = make_dummy_pdf(tmp_path)

    # Monkeypatch PyPDFLoader to return simple objects
    class D:
        def __init__(self, text):
            self.page_content = text

    monkeypatch.setattr(mod, "PyPDFLoader", lambda path: type("L", (), {"load": lambda self: [D("AI content here")]})())

    # Force FAISS.from_documents to raise so we go to fallback
    def fake_from_documents(*args, **kwargs):
        raise RuntimeError("fake embedding failure")

    monkeypatch.setattr(mod, "FAISS", type("F", (), {"from_documents": staticmethod(fake_from_documents)}))

    client = TestClient(mod.app)
    with open(dummy, "rb") as f:
        resp = client.post("/upload-pdf/", files={"file": (dummy.name, f, "application/pdf")})
    assert resp.status_code == 200
    assert "fallback" in resp.json()["message"].lower()

    # Now ask a question; should use local fallback
    resp2 = client.post("/qa/", json={"question": "What is AI?"})
    assert resp2.status_code == 200
    assert "AI" in resp2.json()["answer"] or len(resp2.json()["answer"]) > 0


def test_upload_and_qa_with_mocked_faiss(monkeypatch, tmp_path):
    # Simulate a successful FAISS and QA chain
    dummy = make_dummy_pdf(tmp_path)

    class D:
        def __init__(self, text):
            self.page_content = text

    monkeypatch.setattr(mod, "PyPDFLoader", lambda path: type("L", (), {"load": lambda self: [D("AI content here")]})())

    # Mock embeddings and FAISS
    class FakeVS:
        def as_retriever(self, search_kwargs=None):
            return None

    def fake_from_documents(*args, **kwargs):
        return FakeVS()

    monkeypatch.setattr(mod, "FAISS", type("F", (), {"from_documents": staticmethod(fake_from_documents),
                                                       "load_local": staticmethod(lambda p, e: FakeVS())}))

    # Mock OpenAIEmbeddings to a dummy callable (not used directly)
    monkeypatch.setattr(mod, "OpenAIEmbeddings", lambda model: None)

    # Mock RetrievalQA.from_chain_type to return an object with run()
    class FakeQA:
        def __init__(self):
            pass

        def run(self, q):
            return "MOCK_ANSWER"

    monkeypatch.setattr(mod, "RetrievalQA", type("R", (), {"from_chain_type": staticmethod(lambda **kw: FakeQA())}))

    client = TestClient(mod.app)
    with open(dummy, "rb") as f:
        resp = client.post("/upload-pdf/", files={"file": (dummy.name, f, "application/pdf")})
    assert resp.status_code == 200
    assert "uploaded" in resp.json()["message"].lower()

    resp2 = client.post("/qa/", json={"question": "What is AI?"})
    assert resp2.status_code == 200
    assert resp2.json()["answer"] == "MOCK_ANSWER"
