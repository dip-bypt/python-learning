import os
from pathlib import Path
import day20.day20 as mod


def test_ask_question_local(monkeypatch, tmp_path):
    # Create a dummy sample.pdf (as a text file) in a temp folder
    sample = tmp_path / "sample.pdf"
    sample.write_text("This document mentions AI and machine learning.")

    # Monkeypatch os.path to make the module load the temp sample
    monkeypatch.setattr(mod, "__file__", str(tmp_path / "day20.py"))

    # Monkeypatch load_pdf_documents to read our sample
    def fake_load(pdf_path):
        return [mod.SimpleDocument("AI content here", {"source": "sample.pdf"})]

    monkeypatch.setattr(mod, "load_pdf_documents", fake_load)

    # Ensure no vector store is built (force local fallback)
    monkeypatch.setattr(mod, "build_vector_store", lambda docs: None)

    mod.main()
    # Now ask a question - should use local fallback
    ans = mod.ask_question("Which file talks about AI?")
    assert "AI content" in ans
