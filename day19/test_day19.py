from fastapi.testclient import TestClient
import day19.day19 as mod


def test_qa_endpoint_monkeypatch(monkeypatch):
    # Monkeypatch chain.run to avoid real LLM calls
    def fake_run(inputs):
        # echo back question for verification
        return f"FAKE_ANSWER: {inputs.get('question')}"

    monkeypatch.setattr(mod, "chain", type("C", (), {"run": staticmethod(fake_run)}))

    client = TestClient(mod.app)
    resp = client.post("/qa", json={"text": "some text", "question": "What is this?"})
    assert resp.status_code == 200
    assert resp.json() == {"answer": "FAKE_ANSWER: What is this?"}


def test_qa_endpoint_default_question(monkeypatch):
    # When no question is provided, default is used. Ensure chain.run receives it.
    called = {}

    def fake_run(inputs):
        called['inputs'] = inputs
        return "SUMMARY: ok"

    monkeypatch.setattr(mod, "chain", type("C", (), {"run": staticmethod(fake_run)}))
    client = TestClient(mod.app)
    resp = client.post("/qa", json={"text": "long text"})
    assert resp.status_code == 200
    assert resp.json() == {"answer": "SUMMARY: ok"}
    assert 'question' in called['inputs']
