# Day 8: Hugging Face Transformers Intro

## Overview
This project demonstrates the basics of using Hugging Face's `transformers` library in Python. The main focus is on:
- Installing the `transformers` package
- Using pretrained pipelines for sentiment analysis
- Understanding tokenization basics

## Task
- Use the `pipeline('sentiment-analysis')` from Hugging Face
- Test the pipeline with 3 custom sentences
- Print the sentiment analysis results

## How to Run
1. Install the required package:
   ```bash
   pip install transformers
   ```
2. Run the script:
   ```bash
   python main.py
   ```

## Example Output
The script will print the sentiment analysis results for three example sentences, e.g.:
```
Sentence: I love learning FastAPI and Python!
 → Sentiment: POSITIVE (confidence: 0.99)

Sentence: This project is so difficult and frustrating.
 → Sentiment: NEGATIVE (confidence: 0.98)

Sentence: The weather today is okay, nothing special.
 → Sentiment: NEUTRAL (confidence: 0.65)
```

---
*This project is for educational purposes, demonstrating basic usage of Hugging Face pipelines in Python.*

## API Usage

This project also provides a FastAPI web API for sentiment analysis.

### Endpoint
- **POST** `/predict`

### Request Body
```
{
  "text": "Your sentence here"
}
```

### Response
```
{
  "text": "Your sentence here",
  "sentiment": "POSITIVE",  // or NEGATIVE, NEUTRAL
  "confidence": 0.98
}
```

### How to Run the API
1. Install FastAPI and Uvicorn (if not already installed):
   ```bash
   pip install fastapi uvicorn
   ```
2. Start the API server:
   ```bash
   uvicorn main:API --reload
   ```
   (Run this command from inside the `py_day8` directory.)

### Example API Call
You can test the API using `curl`:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love learning FastAPI and Python!"}'
```
