# Pydantic Models, Query & Path Params (py_day5)

## Session Overview
This session focused on advanced FastAPI features for robust API development:

- **Data validation with Pydantic**: Using Pydantic models for request and response validation.
- **Query & Path Params**: Handling dynamic and query parameters in endpoints.
- **Response Models & Status Codes**: Structuring API responses and using appropriate HTTP status codes.

---

## Tasks Completed

### 1. Extend API with User Endpoints
- **POST /user**: Accepts user data (`email`, `name`, `age`) and stores it in an in-memory database.
- **GET /user/{email}**: Returns user info for the given email if the user exists.

---

## Code Review: `main.py`
- **User Model**: Defines a Pydantic `User` model with `email`, `name`, and `age` fields.
- **In-Memory DB**: Uses a Python dictionary to store user data.
- **POST /user**:
  - Accepts a JSON body matching the `User` model.
  - Returns 201 Created on success, 400 if the email is already registered.
- **GET /user/{email}**:
  - Path parameter for email.
  - Returns user info if found, 404 if not found.
  - Uses `response_model` for response validation.

---

## How to Run
1. **Install dependencies** (in your virtual environment):
   ```bash
   pip install fastapi uvicorn
   ```
2. **Run the API server**:
   ```bash
   uvicorn py_week1.py_day5.main:API --reload
   ```
   OR
   ```bash
    py_week1/ai-env/bin/python -m uvicorn py_week1.py_day5.main:API --reload
    ```
3. **Access API docs**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Example Requests

### POST /user
```
POST http://127.0.0.1:8000/user
Content-Type: application/json
{
  "email": "alice@example.com",
  "name": "Alice",
  "age": 30
}
Response: {
  "status": 200,
  "success": true,
  "message": "User created successfully",
  "user": {
    "email": "alice@example.com",
    "name": "Alice",
    "age": 30
  }
}
```

### GET /user/{email}
```
GET http://127.0.0.1:8000/user/alice@example.com
Response: {
  "status": 200,
  "success": true,
  "message": "User fetched successfully",
  "user": {
    "email": "alice@example.com",
    "name": "Alice",
    "age": 30
  }
}
```

---

## Notes
- The user data is stored in memory and will reset when the server restarts.
- Pydantic models ensure data validation for both requests and responses.
- Proper status codes and error handling are demonstrated.

---

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

