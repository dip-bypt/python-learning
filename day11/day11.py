# FastAPI app instance for ASGI
from fastapi import FastAPI
app = FastAPI()

# Day 11: Model Performance Comparison with Hugging Face Transformers
# ---------------------------------------------------------------
# This script compares the inference performance of two sentiment analysis models
# (BERT and DistilBERT) using Hugging Face's transformers library.
# It measures how long each model takes to process 50 sample sentences and logs the results.
# ---------------------------------------------------------------
# day11_model_comparison.py

from transformers import pipeline
import time
import json

# Step 1: Prepare test data — 50 sample sentences
sentences = [
    "I love learning Python and AI!" if i % 2 == 0 else "I hate getting errors in my code."
    for i in range(50)
]

# Step 2: Initialize two sentiment analysis pipelines
bert_model = "nlptown/bert-base-multilingual-uncased-sentiment"
distilbert_model = "distilbert-base-uncased-finetuned-sst-2-english"

bert_pipeline = pipeline("sentiment-analysis", model=bert_model)
distilbert_pipeline = pipeline("sentiment-analysis", model=distilbert_model)

# Step 3: Function to measure inference time
def measure_inference_time(pipeline_func, sentences):
    start_time = time.time()
    results = [pipeline_func(sentence) for sentence in sentences]
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / len(sentences)
    return total_time, avg_time

# Step 4: Measure inference performance
bert_total, bert_avg = measure_inference_time(bert_pipeline, sentences)
distilbert_total, distilbert_avg = measure_inference_time(distilbert_pipeline, sentences)

# Step 5: Log results in a dictionary
performance_data = {
    "model_performance": [
        {
            "model": "BERT",
            "total_inference_time_sec": round(bert_total, 2),
            "average_time_per_sentence_sec": round(bert_avg, 4)
        },
        {
            "model": "DistilBERT",
            "total_inference_time_sec": round(distilbert_total, 2),
            "average_time_per_sentence_sec": round(distilbert_avg, 4)
        }
    ]
}

# Step 6: Save results into JSON file
with open("performance_log.json", "w") as f:
    json.dump(performance_data, f, indent=4)

# Step 7: Print summary results
print("\n✅ Model Performance Comparison Completed!\n")
for entry in performance_data["model_performance"]:
    print(f"Model: {entry['model']}")
    print(f"➡ Total Time: {entry['total_inference_time_sec']} sec")
    print(f"➡ Avg Time per Sentence: {entry['average_time_per_sentence_sec']} sec\n")
