# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# -----------------------------
# Initialize app
# -----------------------------
API = FastAPI(title="Day 13 - Sentiment Analysis Deployment")

# Enable CORS (allow frontend / any origin)
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Load Hugging Face model
# -----------------------------
sentiment_model = pipeline("sentiment-analysis")

class TextRequest(BaseModel):
    text: str

@API.post("/analyze")
def analyze_text(req: TextRequest):
    try:
        result = sentiment_model(req.text)
        label = result[0]["label"]
        score = round(result[0]["score"], 3)
        return {"text": req.text, "sentiment": label, "confidence": score}
    except Exception as e:
        return {"error": str(e)}

@API.get("/")
def root():
    return {"message": "🚀 Sentiment Analysis API is running!"}
