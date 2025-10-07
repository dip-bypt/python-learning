

# Day 12: Sentiment Analysis on IMDB Reviews with Hugging Face
# ------------------------------------------------------------
# This script demonstrates how to use Hugging Face's datasets and transformers
# libraries to perform sentiment analysis on random IMDB movie reviews.
# Each step is explained for learning purposes.
# ------------------------------------------------------------

from datasets import load_dataset
from transformers import pipeline
import random

# Step 1: Load the IMDB dataset
# The IMDB dataset contains thousands of movie reviews labeled as positive or negative.
dataset = load_dataset("imdb")
train_data = dataset["train"]

# Step 2: Select 5 random reviews from the training set
# This allows us to test the model on different reviews each time.
samples = random.sample(list(train_data), 5)

# Step 3: Load the Hugging Face sentiment analysis pipeline
# The pipeline uses a pre-trained model to predict sentiment (POSITIVE/NEGATIVE).
sentiment_pipeline = pipeline("sentiment-analysis")

# Step 4: Analyze each review and print the results
for i, sample in enumerate(samples, start=1):
    review = sample['text']
    result = sentiment_pipeline(review)[0]
    print(f"\nReview {i}:")
    print(f"Text: {review}")
    print(f"Predicted Sentiment: {result['label']} (score={result['score']:.2f})")
