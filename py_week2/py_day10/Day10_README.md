
# Day 10 - FastAPI + Hugging Face Integration

## Overview
On **Day 10**, the focus was on exposing **Hugging Face models via FastAPI** and creating APIs for NLP and Speech tasks. This included:

1. **Sentiment Analysis API** – accepts JSON input and returns sentiment labels and confidence scores.
2. **Text-to-Speech (TTS) API** – converts text to speech using ESPnet pre-trained models and returns playable audio files.

The exercises combined **API design, Hugging Face inference pipelines, and FastAPI deployment**.

## Learning Topics

- **FastAPI Basics**: Creating APIs (`GET` and `POST` endpoints), accepting JSON input via `Pydantic` models, returning JSON responses, serving static/audio files with `FileResponse`.
- **Hugging Face Model Integration**: Using `transformers` pipelines for NLP tasks, loading pre-trained models, running inference, handling outputs (labels + scores).
- **ESPnet TTS**: Using pre-trained ESPnet models for text-to-speech, generating audio waveforms (`wav`) from text, saving and managing output files, exposing TTS via FastAPI for direct audio playback.
- **Additional Concepts**: File handling in Python (`os`, `uuid`), returning file URLs for web consumption, error handling in API endpoints.

## Tasks

### 1. Sentiment Analysis API
**Objective:** Create a simple sentiment analysis service.

- **Endpoint:** `POST /analyze`  
- **Input:** JSON with `text`  
- **Output:** JSON with `text`, `sentiment` (predicted label), `confidence` (score rounded to 3 decimals)

**Example Request:**
```json
{
  "text": "I love learning FastAPI!"
}
```
**Example Response:**
```json
{
  "text": "I love learning FastAPI!",
  "sentiment": "POSITIVE",
  "confidence": 0.998
}
```

**Key File:** `main.py`  
**Implementation Highlights:** Uses `transformers.pipeline("sentiment-analysis")`, FastAPI POST endpoint returns JSON results, includes a health check at `/`.

### 2. Extra Activity – Text-to-Speech API
**Objective:** Convert text to speech using ESPnet and serve audio via API.

- **Endpoint 1:** `POST /tts` – generate audio from text  
- **Endpoint 2:** `GET /tts-file/{file_name}` – serve the audio file

**Workflow:**  
1. User sends text via `/tts`.  
2. API generates a WAV file in `outputs/`.  
3. API returns a **playable file URL** (`/tts-file/{file_name}`) for immediate playback.

**Example Request to `/tts`:**
```json
{
  "text": "Hello, this is ESPnet speaking."
}
```
**Example Response:**
```json
{
  "message": "Text successfully converted to speech",
  "file_name": "b0e0f191.wav",
  "file_url": "http://0.0.0.0:8000/tts-file/b0e0f191.wav"
}
```

**Key File:** `Text2Speech.py`  
**Implementation Highlights:** Uses ESPnet `Text2Speech.from_pretrained()` for high-quality TTS, saves audio as WAV files (`PCM_16`), generates unique file names using `uuid`, serves audio with `FileResponse` for browser playback.

## R&D and Learnings

1. **FastAPI + File Serving**: Initially returning local file paths caused "Not Found" errors in the browser. Solved by creating `/tts-file/{file_name}` endpoint and returning a URL in `/tts`.
2. **Model Integration**: Explored Hugging Face `transformers.pipeline` for sentiment analysis and ESPnet pre-trained TTS models. Learned to check GPU availability using `torch.cuda.is_available()`.
3. **Output Management**: Created an `outputs/` directory dynamically, used `uuid` to avoid filename collisions, enabled direct playback from FastAPI without manual downloading.
4. **API Usability**: Added clear JSON responses for both success and error cases, created a health check (`GET /`) for Sentiment API.

## Folder Structure (Day 10)
```
py_week2/
│
├─ py_day10/
│  ├─ main.py               # Sentiment Analysis API
│  ├─ Text2Speech.py        # Text-to-Speech API
│  ├─ outputs/              # Generated WAV files
│  └─ README.md             # This file
```

## How to Run

1. **Install dependencies**:
```bash
pip install fastapi uvicorn transformers espnet soundfile torch
```
2. **Run Sentiment API**:
```bash
uvicorn py_day10.main:API --reload --host 0.0.0.0 --port 8000
```
3. **Run TTS API**:
```bash
uvicorn py_day10.Text2Speech:API --reload --host 0.0.0.0 --port 8000
```
4. **Test Endpoints**:
- Sentiment API: `POST /analyze`  
- TTS API: `POST /tts` → returns file URL  
- TTS playback: `GET /tts-file/{file_name}`

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)  
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)  
- [ESPnet2 Documentation](https://espnet.github.io/espnet/)  
- [Serving Files in FastAPI](https://fastapi.tiangolo.com/advanced/static-files/)
