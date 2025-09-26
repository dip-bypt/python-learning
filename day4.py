#!/usr/bin/env python3
"""
Day 4: FastAPI Basics - Hello API

This script demonstrates the basics of FastAPI, including creating GET and POST endpoints.
FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.
It emphasizes async support for high performance and automatic OpenAPI documentation via Swagger UI and ReDoc.

Key Features:
- Async capabilities: Allows non-blocking I/O operations, improving concurrency for I/O-bound tasks.
- Automatic API documentation: Generates interactive Swagger UI (/docs) and ReDoc (/redoc) from code.
- Type validation: Uses Pydantic for request/response validation based on type hints.

Endpoints:
- GET /hello: Returns a simple greeting message.
- POST /echo: Accepts any JSON payload and echoes it back unchanged.
"""

from fastapi import FastAPI, Body
from typing import Dict, Any

# Create the FastAPI application instance
# This instance will be used by Uvicorn to run the server
app = FastAPI(
    title="Hello API",
    description="A simple FastAPI example demonstrating GET and POST endpoints for Day 4.",
    version="1.0.0"
)

@app.get("/hello")
async def hello():
    """
    GET endpoint that returns a greeting message.

    This endpoint demonstrates a basic GET request in FastAPI.
    It returns a plain string response.

    Returns:
        str: A greeting message "Hello, FastAPI!".
    """
    return "Hello, FastAPI!"

@app.post("/echo")
async def echo(data: Dict[str, Any] = Body(..., description="Any JSON payload to echo back")):
    """
    POST endpoint that echoes back the received JSON payload.

    This endpoint accepts any JSON body and returns it unchanged.
    It demonstrates handling POST requests with JSON data in FastAPI.

    Args:
        data (Dict[str, Any]): The JSON payload sent in the request body.

    Returns:
        Dict[str, Any]: The same JSON payload sent in the request body.
    """
    return data
