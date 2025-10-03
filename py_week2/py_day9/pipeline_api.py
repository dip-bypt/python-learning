"""
Day 9 - NLP Tasks with Hugging Face + FastAPI

Features:
1. Summarization (with chunking)
2. Translation (English → French)
3. Question Answering

API Endpoints:
- POST /summarize
- POST /translate
- POST /qa
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import wikipedia

# -----------------------------
# FastAPI App
# -----------------------------
API = FastAPI(title="NLP Tasks API")

# -----------------------------
# Input Schemas
# -----------------------------
class SummarizeRequest(BaseModel):
    topic: str

class TranslateRequest(BaseModel):
    text: str

class QARequest(BaseModel):
    question: str
    topic: str


# -----------------------------
# Load Pipelines (once at startup)
# -----------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


# -----------------------------
# Functions
# -----------------------------
def summarize_wiki(topic: str) -> str:
    """Summarize a Wikipedia article into ~2 sentences with chunking"""
    page = wikipedia.page(topic)
    text = page.content

    max_chunk = 1000
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]

    partial_summaries = []
    for chunk in chunks[:5]:  # limit chunks for performance
        summary = summarizer(chunk, max_length=120, min_length=50, do_sample=False)
        partial_summaries.append(summary[0]['summary_text'])

    return " ".join(partial_summaries)


def translate_text(text: str) -> str:
    """Translate English → French"""
    result = translator(text, max_length=50)
    return result[0]['translation_text']


def qa_task(question: str, topic: str) -> str:
    """Answer a question using Wikipedia article as context"""
    page = wikipedia.page(topic)
    text = page.content

    context = text[:1000]  # take only first 1000 chars
    answer = qa_pipeline(question=question, context=context)
    return answer['answer']


# -----------------------------
# API Routes
# -----------------------------
@API.post("/summarize")
def summarize_api(req: SummarizeRequest):
    try:
        summary = summarize_wiki(req.topic)
        return {"topic": req.topic, "summary": summary}
    except Exception as e:
        return {"error": str(e)}


@API.post("/translate")
def translate_api(req: TranslateRequest):
    try:
        translation = translate_text(req.text)
        return {"original": req.text, "translation": translation}
    except Exception as e:
        return {"error": str(e)}


@API.post("/qa")
def qa_api(req: QARequest):
    try:
        answer = qa_task(req.question, req.topic)
        return {"topic": req.topic, "question": req.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
