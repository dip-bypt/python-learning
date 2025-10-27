import sys
import types
import importlib
import importlib.util
import os
try:
    # import TestClient lazily inside tests to avoid requiring FastAPI at collection time
    from fastapi.testclient import TestClient  # type: ignore
except Exception:
    TestClient = None


def _inject_fake_langchain_modules():
    # langchain_community.document_loaders.PyPDFLoader
    m1 = types.ModuleType("langchain_community.document_loaders")

    class FakeLoader:
        def __init__(self, path):
            self.path = path

        def load(self):
            from types import SimpleNamespace

            return [SimpleNamespace(page_content="Hello world", metadata={"source": "fake"})]

    m1.PyPDFLoader = FakeLoader
    sys.modules["langchain_community.document_loaders"] = m1

    # langchain_community.vectorstores.FAISS
    m2 = types.ModuleType("langchain_community.vectorstores")

    class FakeVectorStore:
        def __init__(self):
            pass

        def as_retriever(self, search_kwargs=None):
            return "retriever"

    # expose a FAISS container with from_documents
    m2.FAISS = types.SimpleNamespace(from_documents=lambda docs, embeddings: FakeVectorStore())
    sys.modules["langchain_community.vectorstores"] = m2

    # langchain_openai (OpenAIEmbeddings, ChatOpenAI)
    m3 = types.ModuleType("langchain_openai")
    m3.OpenAIEmbeddings = lambda model=None: "fake-embeddings"
    m3.ChatOpenAI = lambda model=None, temperature=None: "fake-llm"
    sys.modules["langchain_openai"] = m3

    # langchain.chains.RetrievalQA
    m4 = types.ModuleType("langchain.chains")

    class FakeRetrievalQA:
        @staticmethod
        def from_chain_type(llm=None, retriever=None, chain_type=None):

            class Chain:
                def run(self, q):
                    return f"FAKE ANSWER to: {q}"

            return Chain()

    m4.RetrievalQA = FakeRetrievalQA
    sys.modules["langchain.chains"] = m4


def test_upload_and_ask_endpoints(tmp_path, monkeypatch):
    # Inject fake modules before importing the app so top-level imports succeed
    _inject_fake_langchain_modules()

    # Now import the FastAPI app
    # load module by file path because day22 is not a package in the test env
    module_path = os.path.join(os.path.dirname(__file__), "day22.py")
    spec = importlib.util.spec_from_file_location("day22", module_path)
    app_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_mod)
    # import TestClient lazily
    if TestClient is None:
        from fastapi.testclient import TestClient as _TC
        client = _TC(app_mod.app)
    else:
        client = TestClient(app_mod.app)

    # Prepare a fake PDF file upload
    files = {"file": ("test.pdf", b"%PDF-1.4 fake pdf content", "application/pdf")}
    resp = client.post("/upload_pdf", files=files)
    assert resp.status_code == 200
    assert "uploaded" in resp.json().get("message", "").lower()

    # Ask a question (the app uses the fake RetrievalQA.chain.run)
    resp2 = client.post("/ask", data={"question": "What is this?"})
    assert resp2.status_code == 200
    data = resp2.json()
    assert "answer" in data
    assert "FAKE ANSWER" in data["answer"]


def test_ask_without_upload(monkeypatch):
    # Import app (no uploads done)
    # Ensure modules available for import
    _inject_fake_langchain_modules()
    module_path = os.path.join(os.path.dirname(__file__), "day22.py")
    spec = importlib.util.spec_from_file_location("day22", module_path)
    app_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_mod)
    if TestClient is None:
        from fastapi.testclient import TestClient as _TC
        client = _TC(app_mod.app)
    else:
        client = TestClient(app_mod.app)

    resp = client.post("/ask", data={"question": "Will fail"})
    assert resp.status_code == 200
    assert resp.json().get("error") is not None
