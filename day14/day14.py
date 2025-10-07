# Day 14: Project Wrap-Up & Best Practices
# ----------------------------------------
# Use this file to summarize your final project, document key concepts, and note best practices.
# Add clear comments to explain your code and help future readers understand your workflow.
# ----------------------------------------
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI(title="Text Analysis API", description="2-in-1 Sentiment + Summarization API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model for API requests
class TextRequest(BaseModel):
    text: str

# Load NLP pipelines
sentiment_analyzer = pipeline("sentiment-analysis")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Root route
@app.get("/")
def home():
    return {"message": "Welcome to the Text Analysis API"}

# 1️⃣ Sentiment Analysis Endpoint
@app.post("/sentiment")
def analyze_sentiment(request: TextRequest):
    """
    POST /sentiment
    Input: {"text": "I love Python!"}
    Output: {"label": "POSITIVE", "score": 0.999}
    """
    result = sentiment_analyzer(request.text)[0]
    return {"label": result["label"], "score": round(result["score"], 3)}

# 2️⃣ Text Summarization Endpoint
@app.post("/summary")
def summarize_text(request: TextRequest):
    """
    POST /summary
    Input: {"text": "Long paragraph text..."}
    Output: {"summary": "Short 2-line summary."}
    """
    summary = summarizer(
        request.text,
        max_length=60,  # control summary size
        min_length=25,
        do_sample=False
    )[0]["summary_text"]

    return {"summary": summary}
