# 🧠 Python Week 4 — Day 23
### **Topic:** Auth & Security
**Focus Areas:**
- API Key Authentication
- Rate Limiting (Conceptual Overview)

---

## 🚀 Overview

This session introduces **basic API security** using **API Key authentication** in FastAPI.  
We also discuss **rate limiting concepts**, which help protect APIs from excessive requests.

The practical task for this day focuses on securing the `/qa` endpoint using an API key validation system.

---

## 🧩 File Structure

```
py_week4/
│
├── py_day23/
│   ├── main.py           # Core FastAPI app with API Key Auth
│   ├── test_main.py      # Unit tests for endpoints & auth logic
│   └── README.md         # Documentation (this file)
│
└── requirements.txt
```

---

## 🧠 Learning Objectives

| Concept | Description |
|----------|--------------|
| **Async FastAPI Endpoints** | All endpoints are asynchronous (`async def`) for scalability. |
| **API Key Authentication** | Each request must include a valid API key in headers to access secured routes. |
| **Rate Limiting Basics** | Introduced conceptually — to prevent abuse by limiting requests per user/IP. |

---

## 💻 Code Explanation (`main.py`)

### 1. API Key Setup
```text
API_KEY = "mysecretapikey123"
API_KEY_NAME = "X-API-Key"
```

Clients must send this key in the request headers:
```
X-API-Key: mysecretapikey123
```

### 2. API Key Dependency
```text
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized - Invalid API Key")
```

Checks whether the provided key matches the server-side value.  
Returns **401 Unauthorized** for missing or invalid keys.

### 3. QA Endpoint
```text
@app.get("/qa")
async def qa_endpoint(question: str, x_api_key: str = Depends(verify_api_key)):
    return {"question": question, "answer": question[::-1]}
```

Protected route that requires a valid API key.  
Returns a reversed string as a mock answer (for testing).

### 4. Root Endpoint
```text
@app.get("/")
async def root():
    return {"message": "Welcome to the Secure FastAPI App!"}
```

Publicly accessible route for basic connectivity check.

---

## ✅ Test Coverage (`test_main.py`)

| Test | Description | Expected Result |
|------|--------------|----------------|
| `test_root_endpoint` | Checks if `/` returns welcome message | ✅ 200 OK |
| `test_qa_with_valid_api_key` | Sends valid key and gets response | ✅ 200 OK |
| `test_qa_with_invalid_api_key` | Sends invalid key | ❌ 401 Unauthorized |
| `test_qa_without_api_key` | Omits key entirely | ❌ 401 Unauthorized |

### Run Tests:
```bash
pytest py_day23/test_main.py -v
```

---

## ✅ Test Using curl or Thunder Client

✅ Valid Request
```bash
curl -X GET "http://127.0.0.1:8000/qa?question=Hello" -H "x-api-key: my-secret-key"
```
Response:
```json
{"question": "Hello", "answer": "olleH"}
```

❌ Invalid Request
```bash
curl -X GET "http://127.0.0.1:8000/qa?question=Hello"
```
Response:
```json
{"error": "Unauthorized - Invalid API Key"}
```

---

## 🧩 Rate Limiting — Conceptual Overview

Although not implemented in this day’s task, **rate limiting** is critical for scaling and security.

### Example Techniques
- **Fixed Window:** Allow N requests per minute.
- **Sliding Log / Token Bucket:** Allow burst requests within quota.
- **Redis-based Rate Limiter:** Common for distributed systems.

FastAPI libraries like:
```bash
pip install slowapi
```
can be integrated later for production-level rate limiting.

---

## 🏁 Summary

| Section | Description                                           |
|----------|-------------------------------------------------------|
| **Goal** | Implement secured API with API Key authentication     |
| **Tools Used** | FastAPI, Pytest                                       |
| **Key Concept** | Header-  based authentication                         |
| **Outcome** | `/qa` route protected using custom API key validation |

---
