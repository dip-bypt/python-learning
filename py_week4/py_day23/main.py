from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse

app = FastAPI(title="Day 23 - Auth & Security (API Key Check)")

# --- Configuration ---
API_KEY = "my-secret-key"  # You can store this in .env or secure config
API_KEY_NAME = "x-api-key"  # Header name for API Key

# --- Dependency for API key verification ---
async def verify_api_key(request: Request):
    api_key = request.headers.get(API_KEY_NAME)
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return True

# --- Routes ---
@app.get("/")
async def root():
    return {"message": "Welcome to Day 23 - API Key Auth Demo!"}

@app.get("/qa")
async def qa_endpoint(question: str, authorized: bool = Depends(verify_api_key)):
    """
    Simple Q&A endpoint protected by API Key.
    For demo, just reverses the question text.
    """
    return {"question": question, "answer": question[::-1]}

# --- Custom Exception Handler for 401 ---
@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(status_code=401, content={"error": "Unauthorized - Invalid API Key"})
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

