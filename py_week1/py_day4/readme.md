# FastAPI Basics & Practice (py_day4)

## Session Overview
This session covers the fundamentals of FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Topics Covered
- **What is FastAPI**: Introduction to FastAPI and its advantages.
- **Install & Run Uvicorn**: Setting up the ASGI server (Uvicorn) to run FastAPI apps.
- **Create @app.get() and @app.post() Routes**: Building GET and POST endpoints.
- **Swagger UI & ReDoc Usage**: Using FastAPI's built-in interactive API docs.

---

## Tasks Completed

### 1. Build a Hello API
- **GET /hello**: Returns a welcome message.
- **POST /echo**: (Not implemented in code, see below for implemented POST)
- **POST /login**: Accepts user credentials, returns email and an encrypted password.

---

## Code Review

### main.py
- Defines a FastAPI app instance as `API`.
- Implements a simple string encryption function.
- **GET /hello**: Returns `{ "message": "Hello, BYPT Fast Api!" }`.
- **POST /login**: Accepts a JSON body with `email` and `password`, returns the email and an encrypted version of the password (using a basic character shift).

### user_model.py
- Defines a Pydantic model `UserModel` with `email` and `password` fields for request validation.

---

## How to Run
1. **Install dependencies** (in your virtual environment):
   ```bash
   pip install fastapi uvicorn
   ```
2. **Run the API server**:
   ```bash
   uvicorn py_week1.py_day4.main:API --reload
   ```
   OR
   ```bash
    py_week1/ai-env/bin/python -m uvicorn py_week1.py_day4.main:API --reload
    ```
3. **Access API docs**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Example Requests

### GET /hello
```
GET http://127.0.0.1:8000/hello
Response: { "message": "Hello, BYPT Fast Api!" }
```

### POST /login
```
POST http://127.0.0.1:8000/login
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "mypassword"
}
Response: {
  "email": "user@example.com",
  "encryptedPassword": "pbssdvvzrug"  // password shifted by 3 chars
}
```

---

## Notes
- The `/echo` endpoint described in the task is not implemented in the current code. The POST endpoint available is `/login`.
- The password encryption is a simple character shift for demonstration and **not secure for real applications**.

---

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

