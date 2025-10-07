import time
import json
from transformers import pipeline

# -----------------------------
# Initialize Models (cached in memory)
# -----------------------------
bert_model = pipeline("sentiment-analysis", model="bert-base-uncased")
distilbert_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# -----------------------------
# Sample Sentences
# -----------------------------
sample_sentences = [
    "I love this product!",
    "This is the worst movie I've ever seen.",
    "Transformers library is amazing!",
    "I am not happy with this service.",
    "The weather today is lovely.",
    # Repeat or generate 50 sentences for testing
] * 10  # 5 sentences repeated 10 times = 50 sentences

# -----------------------------
# Function to measure inference time
# -----------------------------
def measure_inference(model, sentences, model_name):
    results = []
    for sentence in sentences:
        start_time = time.time()
        _ = model(sentence)
        end_time = time.time()
        inference_time_ms = round((end_time - start_time) * 1000, 3)
        results.append({
            "model": model_name,
            "sentence": sentence,
            "inference_time_ms": inference_time_ms
        })
    return results

# -----------------------------
# Run Benchmark
# -----------------------------
bert_results = measure_inference(bert_model, sample_sentences, "bert-base-uncased")
distilbert_results = measure_inference(distilbert_model, sample_sentences, "distilbert-base-uncased-finetuned-sst-2-english")

# -----------------------------
# Save results to JSON
# -----------------------------
all_results = bert_results + distilbert_results

with open("py_day11/day11_inference_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("✅ Inference benchmarking completed. Results saved to 'day11_inference_results.json'")
