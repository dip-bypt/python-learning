
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI()

# In-memory user storage (dictionary)
users = {}

# Data model for user
class User(BaseModel):
    name: str
    age: int

# POST /user: Add a user
@app.post("/user")
async def create_user(user: User):
    """
    Accepts JSON {name, age} and stores the user in memory.
    If user with same name exists, returns an error.
    """
    if user.name in users:
        raise HTTPException(status_code=400, detail="User already exists.")
    users[user.name] = user.dict()
    return {"message": f"User {user.name} added.", "user": user}

# GET /user/{name}: Get user info
@app.get("/user/{name}")
async def get_user(name: str):
    """
    Returns user info if exists, else error message.
    """
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found.")
    return users[name]

# (Optional) Example hello route for testing
@app.get("/hello")
async def hello():
    return {"message": "Hello, FastAPI!"}
