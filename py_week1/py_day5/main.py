from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

API = FastAPI()


class User(BaseModel):  # Define a User model
    email: str
    name: str | None = None
    age: int | None = None


users_db = {}  # In-memory database to store users


@API.post('/user', status_code=status.HTTP_201_CREATED)  # 201 is the status code for "Created".
async def create_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    users_db[user.email] = user
    return {
        "status": status.HTTP_200_OK,
        "success": True,
        "message": "User created successfully",
        "user": user
    }


@API.get('/user/{email}', response_model=User)
async def get_user(email: str):
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
