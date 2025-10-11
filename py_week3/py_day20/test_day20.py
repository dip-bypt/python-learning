import os
import pytest
from unittest.mock import patch, MagicMock
from py_day20.main import extract_text_and_tables, create_chunks, create_vector_store, create_chatbot

def setup_vector_store_and_chatbot():
    pdf_path = "py_day20/school_student_report.pdf"
    texts = extract_text_and_tables(pdf_path)
    chunks = create_chunks(texts)
    vector_store = create_vector_store(chunks)
    chatbot = create_chatbot(vector_store)
    return chatbot

def ask_chatbot(chatbot, question):
    # Simulate a conversation session
    return chatbot({"question": question})["answer"]

def test_ananya_iyer_percentage():
    chatbot = setup_vector_store_and_chatbot()
    answer = ask_chatbot(chatbot, "How much percentage did Ananya Iyer got in standard 2?")
    assert "63.96" in answer and "Ananya Iyer" in answer

def test_manav_desai_percentage():
    chatbot = setup_vector_store_and_chatbot()
    answer = ask_chatbot(chatbot, "how much percentage did Manav Desai got?")
    assert "91.96" in answer and "Manav Desai" in answer

def test_class_monitor_standard_3():
    chatbot = setup_vector_store_and_chatbot()
    answer = ask_chatbot(chatbot, "Who is the class moniter of standard 3?")
    assert "Ankit Verma" in answer and "Standard 3" in answer

def test_manav_ambiguous():
    chatbot = setup_vector_store_and_chatbot()
    answer = ask_chatbot(chatbot, "how much percentage did Manav got ?")
    assert "multiple students named Manav" in answer or "specify" in answer
    # Now disambiguate
    answer2 = ask_chatbot(chatbot, "Manav Desai!")
    assert "91.96" in answer2 and "Manav Desai" in answer2
