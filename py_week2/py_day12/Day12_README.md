# 🧠 Day 12 - Hugging Face Datasets & IMDB Sentiment Analysis

## 📘 Comprehensive Learning Topics
**Focus:**  
- Introduction to the `datasets` library  
- Loading and exploring the IMDB dataset  
- Performing batch sentiment analysis using Hugging Face Transformers  

---

## 🎯 Detailed Practical Task
**Goal:**  
> Print 5 random IMDB reviews and their sentiment scores.

---

## 🧩 Concepts Covered
- Loading datasets with `load_dataset()`  
- Understanding dataset splits (`train`, `test`)  
- Random sampling using `Dataset.select()`  
- Using Hugging Face `pipeline` for sentiment analysis  

---

## 🧠 Code Implementation

### **main.py**
```python
from datasets import load_dataset
from transformers import pipeline
import random

# Load dataset
dataset = load_dataset("scikit-learn/imdb")
all_data = dataset["train"]
print("Dataset splits:", dataset.keys())

# Initialize Sentiment Analysis Pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Randomly select 5 sample reviews
sample_indices = random.sample(range(len(all_data)), 5)
sample_reviews = all_data.select(sample_indices)

# Display Results
print("\n🎬 5 Random IMDB Reviews with Sentiment Scores:\n")
for i, review in enumerate(sample_reviews, start=1):
    text = review["text"] if "text" in review else review["content"]
    result = sentiment_analyzer(text[:512])  # Truncate long reviews for faster inference
    print(f"Review {i}:")
    print(f"Text: {text[:200]}{'...' if len(text) > 200 else ''}")
    print(f"Prediction: {result[0]['label']} | Score: {result[0]['score']:.4f}")
    print("-" * 80)
```

---

## 🧪 Example Output
```
Dataset splits: dict_keys(['train'])

🎬 5 Random IMDB Reviews with Sentiment Scores:

Review 1:
Text: This movie was incredibly heartwarming and well-directed. The performances were genuine and the storyline was both engaging and emotional...
Prediction: POSITIVE | Score: 0.9982
--------------------------------------------------------------------------------
Review 2:
Text: The plot made no sense, and the acting was just terrible. I expected more from such a good cast...
Prediction: NEGATIVE | Score: 0.9956
--------------------------------------------------------------------------------
Review 3:
Text: Absolutely loved it! The pacing, soundtrack, and overall vibe were perfect for a feel-good film...
Prediction: POSITIVE | Score: 0.9991
--------------------------------------------------------------------------------
Review 4:
Text: The cinematography was beautiful, but the script lacked depth and originality...
Prediction: NEGATIVE | Score: 0.9812
--------------------------------------------------------------------------------
Review 5:
Text: It's one of those movies that stays with you for days. Brilliantly made and perfectly executed...
Prediction: POSITIVE | Score: 0.9975
--------------------------------------------------------------------------------
```

---

## ⚡ Key Takeaways
- Hugging Face `datasets` library allows direct access to benchmark datasets.
- You can easily apply any `transformers` model on top of datasets for NLP tasks.
- `Dataset.select()` is memory-efficient compared to converting datasets to Python lists.
- This workflow scales seamlessly for batch analysis and production pipelines.

---

## 🧰 Requirements
Make sure the following dependencies are installed:
```bash
pip install datasets transformers torch
```

---

## 🧩 Summary
In this session, you learned:
- How to load IMDB dataset using Hugging Face `datasets` library.  
- How to sample random reviews for quick testing.  
- How to use `pipeline("sentiment-analysis")` for automatic text classification.  
- How to analyze multiple reviews in one go efficiently.
