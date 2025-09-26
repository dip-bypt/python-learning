#!/usr/bin/env python3
"""
Day 5: Pydantic Models + Query/Path Params - User API

This script demonstrates data validation with Pydantic models, path parameters, query parameters,
response models, and HTTP status codes in FastAPI. It builds a simple user management API.

Key Features:
- Pydantic Models: For validating request and response data (e.g., User model with name and age).
- Path Parameters: Dynamic URL parts like /user/{name} for retrieving specific users.
- Query Parameters: Optional URL parameters like ?details=full for additional options.
- Response Models: Typed responses for consistency and automatic Swagger documentation.
- Status Codes: Proper HTTP codes (201 Created, 200 OK, 404 Not Found, 409 Conflict).
- Async Support: Functions are async for FastAPI's non-blocking capabilities.

Endpoints:
- POST /user: Creates a new user from JSON {name, age}.
- GET /user/{name}: Retrieves user info by name, with optional query param for details.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, validator
from typing import Optional

# Pydantic model for User data validation
class User(BaseModel):
    """
    Pydantic model for user data.

    Validates name as a non-empty string and age as a positive integer.
    Used for request bodies (POST) and response schemas.
    """
    name: str
    age: int

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name must not be empty')
        return v

    @validator('age')
    def age_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Age must be a positive integer')
        return v

# Create the FastAPI application instance
# This instance will be used by Uvicorn to run the server
app = FastAPI(
    title="User API",
    description="A simple FastAPI example demonstrating Pydantic models, path/query params, and status codes for Day 5.",
    version="1.0.0"
)

# In-memory storage for users (dict with name as key)
users: dict[str, dict] = {}

@app.post("/user", response_model=User, status_code=201)
async def create_user(user: User):
    """
    POST endpoint to create a new user.

    Accepts JSON with {name, age}, validates via Pydantic, and stores the user.
    Returns 409 if user already exists, 201 on success.

    Args:
        user (User): The user data from the request body.

    Returns:
        User: The created user data.

    Raises:
        HTTPException: 409 if user already exists.
    """
    if user.name in users:
        raise HTTPException(status_code=409, detail="User already exists")
    users[user.name] = user.dict()
    return user

@app.get("/user/{name}", response_model=User)
async def get_user(name: str, details: Optional[str] = Query(None, description="Optional query param: 'full' for complete info")):
    """
    GET endpoint to retrieve a user by name.

    Uses path parameter for name, optional query parameter for details.
    Returns 404 if user not found.

    Args:
        name (str): The user's name from the URL path.
        details (Optional[str]): Query param for additional details (e.g., 'full').

    Returns:
        User: The user data if found.

    Raises:
        HTTPException: 404 if user not found.
    """
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = users[name]
    # Example of query param usage: if details == 'full', could add extra fields, but here just return user
    return User(**user_data)
