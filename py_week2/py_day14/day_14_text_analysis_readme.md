# Day 14 - Text Analysis API

## Overview
Build a unified NLP API using FastAPI and Hugging Face pipelines, exposing two endpoints:

1. **POST /sentiment** → Returns sentiment (POSITIVE/NEGATIVE) with confidence.
2. **POST /summary** → Returns a concise 2-line summary of the text.

This project consolidates NLP tasks into a single API for easy testing and deployment.

---

## Learning Topics
- FastAPI basics: routes, POST requests, request/response models.
- Hugging Face transformers pipelines.
- Sentiment analysis using `distilbert`.
- Text summarization using `facebook/bart-large-cnn`.
- Device management for CPU/GPU inference.

---

## Directory Structure
```
py_week2/
 └── py_day14/
      ├── main.py
      ├── requirements.txt
      └── README.md
```

---

## main.py
```python
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import torch

API = FastAPI(title="Day 14 - Text Analysis API")

# Device configuration
device = 0 if torch.cuda.is_available() else -1

# Hugging Face Pipelines
sentiment_analyzer = pipeline("sentiment-analysis", device=device)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

# Request model
class TextRequest(BaseModel):
    text: str

@API.get("/")
def root():
    return {
        "message": "🚀 Text Analysis API is running!",
        "available_routes": ["/sentiment", "/summary"]
    }

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:API", host="0.0.0.0", port=8000, reload=True)
```

---

## requirements.txt
```
fastapi
uvicorn
transformers
torch
pydantic
```

---

## Example Requests

### 1️⃣ Sentiment Analysis
**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/sentiment" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really love working with Python and FastAPI!"}'
```
**Response:**
```json
{
  "text": "I really love working with Python and FastAPI!",
  "sentiment": "POSITIVE",
  "confidence": 0.999
}
```

### 2️⃣ Text Summarization
**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/summary" \
     -H "Content-Type: application/json" \
     -d '{"text": "FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints. It provides automatic interactive documentation, making development faster and easier."}'
```
**Response:**
```json
{
  "text": "FastAPI is a modern, high-performance web framework for building APIs with Python...",
  "summary": "FastAPI is a Python framework that makes it easy to build fast APIs with automatic documentation."
}
```

---

## Notes
- Ensure `torch` detects the correct device (CPU/GPU) for optimal performance.
- This project combines two separate NLP pipelines into one API for simplicity.
- Can be deployed locally using `uvicorn` or on cloud platforms like Render/Heroku for external access.