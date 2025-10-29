from fastapi import FastAPI, Body

app = FastAPI(title="Text Analysis API", version="1.0")


@app.post("/analyze")
async def analyze_text(data: dict = Body(...)):
    """
    Analyze given text and return simple statistics.
    """
    text = data.get("text", "")
    if not text.strip():
        return {"error": "Text is empty."}

    words = text.split()
    sentences = text.split(".")
    avg_word_length = round(sum(len(w) for w in words) / len(words), 2) if words else 0

    return {
        "word_count": len(words),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "avg_word_length": avg_word_length,
    }


@app.get("/")
async def root():
    return {"message": "Text Analysis API running 🚀"}
