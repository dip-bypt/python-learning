"""
Day 14 - Project: Text Analysis API
----------------------------------
Builds a unified FastAPI service exposing:
  1️⃣ /sentiment  → Sentiment Analysis
  2️⃣ /summary    → Text Summarization
"""

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import torch

# -----------------------------
# Initialize FastAPI App
# -----------------------------
API = FastAPI(title="Day 14 - Text Analysis API")

# -----------------------------
# Model Initialization
# -----------------------------
device = 0 if torch.cuda.is_available() else -1

sentiment_analyzer = pipeline("sentiment-analysis", device=device)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

# -----------------------------
# Input Schema
# -----------------------------
class TextRequest(BaseModel):
    text: str

# -----------------------------
# Root Route
# -----------------------------
@API.get("/")
def root():
    return {
        "message": "🚀 Text Analysis API is running!",
        "available_routes": ["/sentiment", "/summary"]
    }

# -----------------------------
# 1️⃣ Sentiment Analysis Endpoint
# -----------------------------
@API.post("/sentiment")
def analyze_sentiment(req: TextRequest):
    try:
        result = sentiment_analyzer(req.text)[0]
        return {
            "text": req.text,
            "sentiment": result['label'],
            "confidence": round(result['score'], 3)
        }
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# 2️⃣ Summarization Endpoint
# -----------------------------
@API.post("/summary")
def summarize_text(req: TextRequest):
    try:
        result = summarizer(
            req.text,
            max_length=60,
            min_length=20,
            do_sample=False
        )[0]
        return {
            "text": req.text,
            "summary": result['summary_text']
        }
    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# Run locally
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:API", host="0.0.0.0", port=8000, reload=True)
