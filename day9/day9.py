
"""
Day 9: Summarization with Hugging Face Transformers

This script demonstrates how to use the Hugging Face `transformers` library to summarize a Wikipedia article using the "facebook/bart-large-cnn" model.

Steps:
1. Load the summarization pipeline with the specified model.
2. Fetch a Wikipedia article using the Wikipedia REST API.
3. Summarize the article in 2 sentences.
4. Print the original and summarized text.

You can change the topic by editing the Wikipedia API URL.
"""


from transformers import pipeline
import requests

# Step 1: Load the summarization pipeline using facebook/bart-large-cnn
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Step 2: Try to fetch a Wikipedia article (change 'FastAPI' to any topic)
wiki_url = "https://en.wikipedia.org/api/rest_v1/page/summary/FastAPI"
fallback_article = (
	"FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. "
	"The key features are fast to code, fewer bugs, easy to use, and production-ready. "
	"It is built on top of Starlette for the web parts and Pydantic for the data parts. "
	"FastAPI is used by many organizations and is one of the fastest-growing Python frameworks."
)

try:
	response = requests.get(wiki_url, timeout=10)
	response.raise_for_status()
	try:
		data = response.json()
		article_text = data.get("extract", "")
		if not article_text:
			print("Wikipedia article has no extract, using fallback text.\n")
			article_text = fallback_article
	except Exception as e:
		print(f"Error decoding JSON from Wikipedia: {e}\nUsing fallback article.\n")
		article_text = fallback_article
except Exception as e:
	print(f"Error fetching Wikipedia article: {e}\nUsing fallback article.\n")
	article_text = fallback_article

print("📰 Original Wikipedia Article:\n")
print(article_text)

# Step 3: Summarize the text into 2 sentences
summary = summarizer(article_text, max_length=80, min_length=30, do_sample=False)

# Step 4: Print the final summarized text
print("\n--- ✨ Summarized Article (2 sentences) ---\n")
print(summary[0]['summary_text'])
