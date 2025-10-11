import os
import tempfile
import textwrap

from day17.day17 import process_pdf


def test_process_pdf_with_mock(tmp_path):
    # create a small dummy PDF by writing plain text and relying on the
    # PyPDFLoader not to be invoked because we pass a mock llm_callable.
    pdf_file = tmp_path / "dummy.pdf"
    pdf_file.write_text("This is a dummy PDF content for testing.")

    def mock_llm_callable(path):
        assert str(path) == str(pdf_file)
        return "MOCK_SUMMARY"

    summary = process_pdf(str(pdf_file), llm_callable=mock_llm_callable)
    assert summary == "MOCK_SUMMARY"


def test_process_pdf_missing_file():
    missing = "nonexistent.pdf"
    try:
        process_pdf(missing, llm_callable=lambda p: "x")
    except FileNotFoundError as e:
        assert "PDF file not found" in str(e)
    else:
        raise AssertionError("Expected FileNotFoundError")
