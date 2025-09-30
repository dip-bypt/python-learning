# py_week2/py_day8/main.py

"""
Day 8 - Hugging Face Intro
Task:
 - Use pipeline('sentiment-analysis')
 - Test 3 custom sentences & print results

Concepts Covered:
 - Hugging Face transformers library
 - Using pretrained pipelines
 - Basic Sentiment Analysis
"""

from transformers import pipeline
from fastapi import FastAPI
from pydantic import BaseModel

# -----------------------------
# Create a sentiment analysis pipeline
# -----------------------------
sentiment_analyzer = pipeline("sentiment-analysis")

# -----------------------------
# Custom sentences to analyze
# -----------------------------
sentences = [
    "I love learning FastAPI and Python!",
    "This project is so difficult and frustrating.",
    "The weather today is okay, nothing special."
]

# -----------------------------
# Analyze each sentence
# -----------------------------
for sentence in sentences:
    result = sentiment_analyzer(sentence)  # Run model on text
    # Result is a list with one dict: [{'label': 'POSITIVE', 'score': 0.99}]
    label = result[0]['label']
    score = result[0]['score']
    print(f"Sentence: {sentence}")
    print(f" → Sentiment: {label} (confidence: {score:.2f})\n")

class Sentence(BaseModel):
    text: str


API = FastAPI()

@API.post(
    "/predict")
def predict_sentiment(sentence: Sentence):
    result = sentiment_analyzer(sentence.text)
    label = result[0]['label']
    score = result[0]['score']
    return {"text": sentence.text, "sentiment": label, "confidence": score}
