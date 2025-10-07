from datasets import load_dataset
from transformers import pipeline
import random

# Load dataset
dataset = load_dataset("scikit-learn/imdb")
all_data = dataset["train"]

# Initialize pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Randomly select 5 indices
sample_indices = random.sample(range(len(all_data)), 5)
sample_reviews = all_data.select(sample_indices)

print("\n🎬 5 Random IMDB Reviews with Sentiment Scores:\n")
for i, review in enumerate(sample_reviews, start=1):
    text = review["review"]
    result = sentiment_analyzer(text[:512])
    print(f"Review {i}:")
    print(f"Text: {text[:200]}{'...' if len(text) > 200 else ''}")
    print(f"Prediction: {result[0]['label']} | Score: {result[0]['score']:.4f}")
    print("-" * 80)
