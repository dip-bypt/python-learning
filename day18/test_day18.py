import os
from pathlib import Path

from day18.day18 import load_documents, similarity_search_local


def test_load_documents(tmp_path, monkeypatch):
    d = tmp_path / "texts"
    d.mkdir()
    f1 = d / "a.txt"
    f2 = d / "b.txt"
    f1.write_text("This is about AI and machine learning.")
    f2.write_text("This is about cooking and recipes.")

    docs = load_documents(d)
    assert len(docs) == 2
    names = {doc.metadata['source'] for doc in docs}
    assert names == {"a.txt", "b.txt"}


def test_similarity_search_local():
    class D:
        def __init__(self, text, name):
            self.page_content = text
            self.metadata = {"source": name}

    docs = [D("AI machine learning", "a.txt"), D("Cooking recipes", "b.txt")]
    results = similarity_search_local(docs, "Which file talks about AI?", k=1)
    assert len(results) == 1
    assert results[0].metadata['source'] == "a.txt"
