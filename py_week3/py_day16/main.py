from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Day 16 - Sequential Chain API", version="1.0")

# Initialize LLM
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1️⃣: Summarization prompt
summary_template = """
Summarize the following text in 2 concise sentences:
{text}
"""
summary_prompt = PromptTemplate(input_variables=["text"], template=summary_template)
summary_chain = summary_prompt | llm

# Step 2️⃣: Keyword extraction prompt
keyword_template = """
Extract 5 relevant keywords from this summary:
{summary}
Return them as a comma-separated list.
"""
keyword_prompt = PromptTemplate(input_variables=["summary"], template=keyword_template)
keyword_chain = keyword_prompt | llm


# ------------------------
# EXAMPLE EXECUTION (Console)
# ------------------------
if __name__ == "__main__":
    example_text = (
        "Python is a powerful programming language used for data science, web development, "
        "automation, and artificial intelligence. Its simple syntax and vast libraries make it "
        "a top choice for developers around the world."
    )

    print("\n🚀 Running Example for Day 16 - Sequential Chain\n")
    print("Original Text:\n", example_text)

    # Step 1: Summarize
    summary = summary_chain.invoke({"text": example_text}).strip()
    print("\n🧠 Summary:\n", summary)

    # Step 2: Extract keywords
    keywords = keyword_chain.invoke({"summary": summary}).strip()
    print("\n🔑 Extracted Keywords:\n", keywords)

    print("\n✅ Console Example Execution Complete.\n")

# ------------------------
# FASTAPI Implementation
# ------------------------

class TextRequest(BaseModel):
    text: str


@app.post("/analyze")
async def analyze_text(request: TextRequest):
    """Chain: Input text → Summarize → Extract Keywords"""
    summary = summary_chain.invoke({"text": request.text}).strip()
    keywords = keyword_chain.invoke({"summary": summary}).strip()

    return {
        "original_text": request.text,
        "summary": summary,
        "keywords": [k.strip() for k in keywords.split(",")]
    }


@app.get("/")
async def root():
    return {"message": "Day 16 - Sequential Chain API is running 🚀"}
