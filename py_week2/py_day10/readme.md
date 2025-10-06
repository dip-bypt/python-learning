# Day 10: Expose Hugging Face Model with FastAPI

## Overview
This project demonstrates how to expose a Hugging Face sentiment analysis model as a web API using FastAPI. The API accepts JSON input, runs inference using a pre-trained sentiment model, and returns the sentiment label and confidence score.

## Features
- FastAPI web server
- Hugging Face Transformers pipeline for sentiment analysis
- POST endpoint `/analyze` that accepts text and returns sentiment results

## How It Works
- The API loads a Hugging Face sentiment analysis pipeline at startup.
- Users send a POST request to `/analyze` with a JSON body containing a `text` field.
- The API returns the sentiment label (e.g., POSITIVE/NEGATIVE) and a confidence score.

## API Endpoints
### Health Check
- **GET /**
  - Returns a message indicating the API is running.

### Sentiment Analysis
- **POST /analyze**
  - **Request Body:**
    ```json
    { "text": "I love learning FastAPI!" }
    ```
  - **Response:**
    ```json
    {
      "text": "I love learning FastAPI!",
      "sentiment": "POSITIVE",
      "confidence": 0.999
    }
    ```

## Running the API
1. Install dependencies:
   ```bash
   pip install fastapi transformers uvicorn
   ```
2. Start the server:
   ```bash
   uvicorn main:API --reload
   ```
3. Access the API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Notes
- The model is loaded at startup for efficient inference.
- Handles errors gracefully and returns error messages in JSON format.

---
**Session Task Recap:**
- Expose Hugging Face model with FastAPI
- Accept JSON input for text
- Run inference & return JSON
- Create Sentiment API: POST /analyze → returns label + score

