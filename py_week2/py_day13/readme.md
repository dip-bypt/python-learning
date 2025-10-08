# Day 13: Deploy Local ML API with FastAPI & ngrok

## Overview
This project demonstrates how to deploy a sentiment analysis API using FastAPI, enable CORS for frontend use, and expose your local API to the internet using ngrok. The API uses a Hugging Face model for sentiment analysis and is ready for testing with curl, Postman, or any frontend client.

---

## Learning Topics
- **Deploy Local ML API**
- **Run FastAPI with uvicorn**
- **Enable CORS for frontend use**

---

## Practical Task
- Deploy a sentiment analysis API locally
- Test the API using curl & Postman

---

## How to Run

### 1. Install Requirements
Make sure you have Python 3.12+ and install dependencies:

```bash
pip install fastapi uvicorn transformers
```

### 2. Start the FastAPI Server

```bash
python -m uvicorn py_day13.main:API --reload --host 0.0.0.0 --port 8000
```

- The API will be available at: `http://localhost:8000/`
- Api status check endpoint: `http://localhost:8000/`

### 3. Enable Public Access with ngrok

1. **Sign up for ngrok:**
   - Go to [ngrok signup](https://dashboard.ngrok.com/signup) and create a free account.
   - After signup, get your auth token from [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken).

2. **Add your auth token locally:**
   ```bash
   ngrok config add-authtoken <your-token-here>
   ```

3. **Expose your local server:**
   ```bash
   ngrok http 8000
   ```
   - You will get a public URL like `https://abcd1234.ngrok-free.app`.

---

## API Endpoints

### 1. Check Api Status
- **GET /** 
- Returns a simple status message to verify the API is running.
- Example:
  ```json
  {"message": "🚀 Sentiment Analysis API is running!"}
  ```

### 2. Sentiment Analysis
- **POST /analyze**
- Request body (JSON):
  ```json
  { "text": "I love learning FastAPI!" }
  ```
- Response (JSON):
  ```json
  {
    "text": "I love learning FastAPI!",
    "sentiment": "POS",
    "confidence": 0.998
  }
  ```

---

## Example: Test with curl

```bash
curl --location 'https://noniodized-untamely-aimee.ngrok-free.dev/analyze' \
--header 'Content-Type: application/json' \
--data '{"text": "I love learning FastAPI!"}'
```

---

## Notes
- CORS is enabled for all origins, so you can connect from any frontend.
- The API is ready for use with tools like Postman, curl, or your own web app.
- The `/` endpoint is useful for browser-based checks.

---

## Credits
- Model: [finiteautomata/bertweet-base-sentiment-analysis](https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis)
- FastAPI: https://fastapi.tiangolo.com/
- ngrok: https://ngrok.com/

