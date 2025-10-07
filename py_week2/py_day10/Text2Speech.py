"""
Day 10 - Extra Activity
Text-to-Speech using ESPnet + Hugging Face Integration

Concepts:
 - Using ESPnet's pre-trained Text2Speech models
 - Generating waveform from text
 - Saving to WAV/MP3
 - Optional: Exposing via FastAPI endpoint
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import soundfile as sf
from espnet2.bin.tts_inference import Text2Speech
import torch
import uuid
import os

# -----------------------------
# Initialize Model
# -----------------------------
# You can replace the model below with any other TTS model from Hugging Face
# Examples: espnet/kan-bayashi_ljspeech_vits, espnet/kan-bayashi_jsut_tacotron2
text2speech = Text2Speech.from_pretrained(
    "espnet/kan-bayashi_ljspeech_vits",  # English female voice (high quality)
    device="cpu" if not torch.cuda.is_available() else "cuda"
)

# -----------------------------
# Base Directory for Saving Audio Files
# -----------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Core Function (Reusable)
# -----------------------------
def generate_speech_from_text(text: str) -> str:
    """Convert input text to speech and save as WAV file."""
    # Run TTS inference
    speech = text2speech(text)["wav"]

    # Unique file name
    file_id = str(uuid.uuid4())[:8]
    file_path = os.path.join(OUTPUT_DIR, f"{file_id}.wav")

    # Save WAV file
    sf.write(file_path, speech.numpy(), text2speech.fs, "PCM_16")
    return file_path

# -----------------------------
# FastAPI Setup
# -----------------------------
API = FastAPI(title="Day 10 - Text to Speech (ESPnet)")

class TTSRequest(BaseModel):
    text: str

@API.post("/tts")
def tts_api(req: TTSRequest):
    """
    Converts given text into speech and returns the accessible file URL.
    """
    try:
        # Generate the audio file
        file_path = generate_speech_from_text(req.text)
        filename = os.path.basename(file_path)

        # Construct URL pointing to /tts-file route
        file_url = f"http://0.0.0.0:8000/tts-file/{filename}"

        return {
            "message": "Text successfully converted to speech",
            "file_name": filename,
            "file_url": file_url
        }
    except Exception as e:
        return {"error": str(e)}


@API.get("/tts-file/{file_name}")
def get_tts_file(file_name: str):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav", filename=file_name)
    else:
        return {"error": "File not found"}

# -----------------------------
# Example Run (if executed directly)
# -----------------------------
if __name__ == "__main__":
    sample_text = "Welcome to the Day 10 extra activity on Text to Speech using ESPnet."
    audio_file = generate_speech_from_text(sample_text)
    print(f"✅ Audio saved successfully: {audio_file}")

