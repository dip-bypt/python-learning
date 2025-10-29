# 🧠 Text Analysis API (Week 4 Learning Project)

This project demonstrates the use of **FastAPI**, **LangChain**, and **Docker** to build a **Text Analysis API** capable of performing various NLP-based text processing tasks.  
It is part of the **Week 4 - Python AI Learning** workflow.

---

## 📚 Learning Objectives
- Understand **FastAPI** structure and API development.
- Use **LangChain** for text processing.
- Containerize the application using **Docker**.
- Run and test APIs using **Postman**.
- Implement modular code and maintain best practices for production-ready Python services.

---

## 🏗️ Project Structure

```
py_week4/
│
├── main.py                # Entry point for FastAPI application
├── requirements.txt       # Project dependencies
├── Dockerfile             # Docker container configuration
├── README.md              # Project documentation
└── .venv/                 # Virtual environment (optional, local only)
```

---

## 🚀 Setup & Run (Locally)

### 1️⃣ Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Mac/Linux
.venv\Scripts\activate   # On Windows
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run FastAPI App
```bash
uvicorn main:app --reload
```
Then open the app at:  
👉 **http://127.0.0.1:8000**

---

## 🧪 Testing the API (Postman / Browser)

### Endpoints
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/` | Returns welcome message |
| `POST` | `/analyze` | Analyze text for sentiment, word count, and more |

### Example Request
**POST** → `/analyze`
```json
{
  "text": "LangChain makes text analysis simpler!"
}
```

### Example Response
```json
{
  "word_count": 5,
  "sentiment": "positive",
  "language": "en",
  "analysis_summary": "The text expresses a positive tone and enthusiasm."
}
```

---

## 🧩 Running Tests

### Run all test cases
```bash
pytest -v
```
If you have a `tests/` directory, make sure it includes unit tests like:
```python
def test_text_analysis():
    response = client.post("/analyze", json={"text": "I love Python!"})
    assert response.status_code == 200
    assert "sentiment" in response.json()
```

---

## 🐳 Docker Setup

### 1️⃣ Build Docker Image
```bash
docker build -t text-analysis-api .
```

### 2️⃣ Run Docker Container
```bash
docker run -p 8000:8000 text-analysis-api
```

Now open: 👉 **http://localhost:8000**

You should see logs similar to:
```
Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## 🧠 Understanding `main.py`

The main logic is implemented in `main.py`:
- Initializes **FastAPI** app.
- Defines routes for text analysis.
- Uses LangChain logic for sentiment and linguistic processing.

Example snippet:
```python
@app.post("/analyze")
def analyze_text(request: TextRequest):
    result = process_text(request.text)
    return {"analysis": result}
```

---

## 🧩 Docker Debugging Tips
If you get an error like:
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```
Make sure Docker is running and restart it if needed.

---

## ✅ Summary
| Feature | Description |
|----------|-------------|
| Framework | FastAPI |
| NLP Engine | LangChain |
| Deployment | Docker |
| Testing | pytest |
| API Testing | Postman |
| Port | 8000 |

---

## 💡 Author & Learning Context
**Author:** Mohit Rajpurohit  
**Session:** Python AI Learning - Week 4  
**Focus:** Docker + FastAPI + LangChain fundamentals  
**Instructor Context:** Internal learning module under AI Projects

---

## 🧾 License
This project is created for educational purposes and can be freely used for personal learning or experimentation.
