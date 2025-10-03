"""
Day 10: Expose Hugging Face Sentiment Model with FastAPI

This script creates a FastAPI API that exposes a Hugging Face sentiment analysis model.
- POST /analyze: Accepts JSON input {"text": "..."} and returns the sentiment label and score as JSON.

You can test this API with curl, Postman, or the Swagger UI at /docs.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Load the sentiment analysis pipeline once at startup
sentiment_pipeline = pipeline("sentiment-analysis")

app = FastAPI()

class TextIn(BaseModel):
    text: str

class SentimentOut(BaseModel):
    label: str
    score: float

@app.post("/analyze", response_model=SentimentOut)
def analyze_sentiment(input: TextIn):
    """
    Accepts JSON {"text": "..."} and returns sentiment label and score.
    """
    result = sentiment_pipeline(input.text)[0]
    return {"label": result["label"], "score": result["score"]}
