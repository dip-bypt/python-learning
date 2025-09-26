from fastapi import FastAPI

from py_week1.py_day4.user_model import UserModel

API = FastAPI()

def encrypt(text, key):
    """Encrypts a string by shifting each character's Unicode code by 'key'."""
    encrypted = ""
    for char in text:
        encrypted += chr(ord(char) + key)  # shift char by key
    return encrypted

@API.get('/hello') # GET request to /hello endpoint
def hello():
    return {'message': 'Hello, BYPT Fast Api!'} # Return a JSON response

@API.post('/login') # POST request to /login endpoint
def login_user(login_data: UserModel):
    encrypted_password = encrypt(login_data.password, 3)
    return {'email': login_data.email, 'encryptedPassword': encrypted_password}