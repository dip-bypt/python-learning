from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Create FastAPI instance
app = FastAPI()

# In-memory item storage (dictionary)
users: Dict[str, dict] = {}

# Pydantic model for User
class User(BaseModel):
    name: str
    age: int

# Response model (to ensure consistent output)
class UserResponse(BaseModel):
    name: str
    age: int

# POST /user → create user
@app.post("/user", response_model=UserResponse, status_code=201)
async def create_user(user: User):
    if user.name in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.name] = {"name": user.name, "age": user.age}
    return users[user.name]

# GET /user/{name} → fetch user by name
@app.get("/user/{name}", response_model=UserResponse)
async def get_user(name: str):
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[name]

