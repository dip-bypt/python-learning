"""
Day 8: Sentiment Analysis with Hugging Face Transformers

This script demonstrates how to use Hugging Face's `transformers` library
to perform sentiment analysis on custom sentences using a pre-trained pipeline.

Steps:
1. Load the sentiment-analysis pipeline.
2. Analyze a list of sentences.
3. Print the sentiment label and confidence score for each sentence.
"""

from transformers import pipeline

# Step 1: Load the pre-trained sentiment analysis pipeline
# This downloads and loads a model that can classify text as POSITIVE or NEGATIVE.
sentiment_pipeline = pipeline("sentiment-analysis")

# Step 2: Define custom sentences to analyze
sentences = [
    "I really love learning AI with Python!",
    "This is the worst movie I have ever seen.",
    "The food was okay, not too bad but not great either."
]

# Step 3: Analyze each sentence and print the results
for sentence in sentences:
    result = sentiment_pipeline(sentence)
    label = result[0]['label']        # Sentiment label: POSITIVE or NEGATIVE
    score = result[0]['score']        # Confidence score (0 to 1)
    print(f"Sentence: {sentence}")
    print(f"Sentiment: {label}, Confidence: {score:.2f}")
    print("-" * 50)
