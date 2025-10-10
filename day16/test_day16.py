import pytest
from day16.day16 import process_text


def mock_llm(input_text):
    # Return deterministic, test-friendly response
    return {
        "summary": "This is a short summary of the input.",
        "keywords": "keyword1, keyword2, keyword3, keyword4, keyword5"
    }


def test_process_text_with_mock():
    input_text = "Some long text about AI and programming."
    out = process_text(input_text, llm_callable=mock_llm)
    assert "summary" in out
    assert "keywords" in out
    assert out["summary"].startswith("This is a short summary")
    assert "keyword1" in out["keywords"]
