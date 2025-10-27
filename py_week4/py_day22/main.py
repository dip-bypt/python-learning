# py_week4/py_day22/main.py

from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
import os

app = FastAPI(title="Async FastAPI with Background Tasks")

LOG_DIR = "py_day22/logs"
LOG_FILE = f"{LOG_DIR}/api_logs.txt"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def save_log_to_file(endpoint: str, message: str):
    """Background task to save logs asynchronously."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {endpoint}: {message}\n"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)


# ---------- Async Routes ---------- #

@app.get("/")
async def root(background_tasks: BackgroundTasks):
    background_tasks.add_task(save_log_to_file, "/", "Root endpoint called")
    return {"message": "Async FastAPI API running 🚀"}


@app.get("/status")
async def get_status(background_tasks: BackgroundTasks):
    """Simple async endpoint that logs status checks."""
    message = "Status endpoint called successfully."
    background_tasks.add_task(save_log_to_file, "/status", message)
    return {"status": "ok", "message": message}


@app.get("/greet/{name}")
async def greet_user(name: str, background_tasks: BackgroundTasks):
    """Async greeting endpoint that logs each call."""
    message = f"Greeted user: {name}"
    background_tasks.add_task(save_log_to_file, f"/greet/{name}", message)
    return {"message": f"Hello, {name}!"}


@app.post("/process")
async def process_data(background_tasks: BackgroundTasks):
    """Simulate async processing and log it."""
    message = "Data processing initiated."
    background_tasks.add_task(save_log_to_file, "/process", message)
    return {"task": "processing", "status": "started"}
