"""
Day 9 - NLP Tasks with Hugging Face

Tasks:
1. Summarization (with chunking to avoid OOM)
2. Translation (English → French)
3. Question Answering
"""

from transformers import pipeline
import wikipedia

# -----------------------------
# Config
# -----------------------------
TOPIC = "Artificial intelligence"   # <-- Change to any Wikipedia topic


# -----------------------------
# 1. Summarization (with chunking)
# -----------------------------
print("=== Summarization Task ===")

try:
    # Fetch Wikipedia article dynamically
    page = wikipedia.page(TOPIC)
    text = page.content
    print(f"Fetched topic: {TOPIC}")
    print(f"Article length: {len(text)} characters\n")

    # Show first 500 characters
    print("Original Wikipedia Text (first 500 chars):\n")
    print(text[:500], "\n")

    # Load summarizer
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # ---- CHUNKING ----
    max_chunk = 1000  # characters per chunk
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]

    print(f"Splitting into {len(chunks)} chunks...\n")

    partial_summaries = []
    for idx, chunk in enumerate(chunks[:5]):  # limit to 5 chunks to keep runtime reasonable
        print(f" Summarizing chunk {idx+1}/{len(chunks)}...")
        summary = summarizer(chunk, max_length=120, min_length=50, do_sample=False)
        partial_summaries.append(summary[0]['summary_text'])

    # Combine partial summaries
    final_summary_text = " ".join(partial_summaries)

    print("\nSummarization Result:\n")
    print(final_summary_text, "\n")

except Exception as e:
    print("Error in summarization:", e)


# -----------------------------
# 2. Translation
# -----------------------------
print("=== Translation Task ===")

try:
    translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
    translation = translator("Artificial intelligence is transforming the world.", max_length=50)
    print("Translation Result (English → French):\n")
    print(translation[0]['translation_text'], "\n")

except Exception as e:
    print("Error in translation:", e)


# -----------------------------
# 3. Question Answering
# -----------------------------
print("=== Question Answering Task ===")

try:
    qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

    # Use the first chunk as context
    context = chunks[0] if len(text) > 0 else "Artificial intelligence is a branch of computer science."

    question = "What are some applications of AI?"

    answer = qa(question=question, context=context)
    print(f"Q: {question}")
    print("Answer:", answer['answer'], "\n")

except Exception as e:
    print("Error in Q&A:", e)
