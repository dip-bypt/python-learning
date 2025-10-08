"""
Day 10 - Expose Hugging Face Sentiment Model with FastAPI

Concepts:
 - Accept JSON input
 - Run Hugging Face pipeline inference
 - Return label + score as JSON

Task:
 - Create POST /analyze → returns label + score
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# -----------------------------
# Initialize FastAPI app
# -----------------------------
API = FastAPI(title="Day 10 - Sentiment Analysis API")

# -----------------------------
# Load Hugging Face Sentiment Pipeline
# -----------------------------
sentiment_model = pipeline("sentiment-analysis")

# -----------------------------
# Define Request Schema
# -----------------------------
class TextRequest(BaseModel):
    text: str

# -----------------------------
# Define Root Route (Health Check)
# -----------------------------
@API.get("/")
def root():
    return {"message": "🚀 Sentiment Analysis API is running!"}

# -----------------------------
# Define Sentiment Analysis API
# -----------------------------
@API.post("/analyze")
def analyze_text(req: TextRequest):
    result = sentiment_model(req.text)
    label = result[0]["label"]
    score = result[0]["score"]
    return {"text": req.text, "sentiment": label, "confidence": score}

