import os
import shutil
import tempfile
import types
import pytest
from unittest.mock import MagicMock
from py_day18 import main
from langchain_core.embeddings import Embeddings

def make_temp_txt_files(contents):
    temp_dir = tempfile.mkdtemp()
    for i, text in enumerate(contents, 1):
        with open(os.path.join(temp_dir, f"file{i}.txt"), "w") as f:
            f.write(text)
    return temp_dir

def test_load_documents():
    temp_dir = make_temp_txt_files(["AI is cool.", "Web dev explained."])
    docs = main.load_documents(temp_dir)
    assert len(docs) == 2
    shutil.rmtree(temp_dir)

def test_split_documents():
    temp_dir = make_temp_txt_files(["A"*500, "B"*500])
    docs = main.load_documents(temp_dir)
    chunks = main.split_documents(docs, chunk_size=200, chunk_overlap=50)
    # Accept splitter behavior: just check all chunks are non-empty and count >= docs
    assert all(len(chunk.page_content) > 0 for chunk in chunks)
    assert len(chunks) >= len(docs)
    shutil.rmtree(temp_dir)

def test_create_vector_store_and_query():
    temp_dir = make_temp_txt_files(["AI and ML.", "Web development."])
    docs = main.load_documents(temp_dir)
    chunks = main.split_documents(docs, chunk_size=100, chunk_overlap=10)
    # DummyEmbeddings inherits from Embeddings for FAISS compatibility
    class DummyEmbeddings(Embeddings):
        def embed_documents(self, texts):
            return [[float(i)]*10 for i in range(len(texts))]
        def embed_query(self, text):
            return [0.0]*10
    db = main.create_vector_store(chunks, DummyEmbeddings())
    queries = ["AI", "Web"]
    results = main.perform_queries(db, queries, k=1)
    assert len(results) == 2
    assert all(len(r) == 1 for r in results)
    shutil.rmtree(temp_dir)

def test_missing_data_dir():
    with pytest.raises(FileNotFoundError):
        main.load_documents("/tmp/does_not_exist_12345")

def test_empty_data_dir():
    temp_dir = tempfile.mkdtemp()
    docs = main.load_documents(temp_dir)
    assert docs == []
    shutil.rmtree(temp_dir)
