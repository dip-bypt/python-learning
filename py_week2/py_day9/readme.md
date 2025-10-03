# Day 9 - Hugging Face NLP Tasks

## Assessment Overview

**Topics Covered:**
- Using Hugging Face pipelines for different NLP tasks: Summarization, Translation, and Question Answering.
- Loading models from the Hugging Face model hub.

**Task:**
- Load the "facebook/bart-large-cnn" model.
- Summarize a Wikipedia article in 2 sentences.

---

## Code Overview

### main.py
- Fetches a Wikipedia article (default: "Artificial intelligence").
- Uses the Hugging Face summarization pipeline (`facebook/bart-large-cnn`) to summarize the article.
- Handles long articles by chunking the text.
- Prints the original and summarized text.

### pipeline_api.py
- Implements a FastAPI app with three endpoints:
  - `/summarize`: Summarizes a Wikipedia article by topic.
  - `/translate`: Translates English text to French.
  - `/qa`: Answers a question based on a Wikipedia article.
- Loads and reuses Hugging Face pipelines for summarization, translation, and question answering.

---

## How to Run

### 1. Install Requirements

```bash
pip install transformers fastapi wikipedia uvicorn
```

### 2. Run the Script

To summarize a Wikipedia article from the command line:

```bash
python main.py
```

### 3. Run the API

Start the FastAPI server:

```bash
uvicorn pipeline_api:API --reload
```

- Access the interactive docs at: http://127.0.0.1:8000/docs

---

## Example API Usage

- **Summarize:**  
  `POST /summarize`  
  Body: `{ "topic": "Artificial intelligence" }`

- **Translate:**  
  `POST /translate`  
  Body: `{ "text": "Hello, how are you?" }`

- **Question Answering:**  
  `POST /qa`  
  Body: `{ "question": "What is AI?", "topic": "Artificial intelligence" }`

---

## Notes
- The summarization pipeline uses chunking to handle long Wikipedia articles.
- All models are loaded from the Hugging Face model hub.
- The API is ready for extension to other NLP tasks as needed.

