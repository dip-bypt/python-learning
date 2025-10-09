from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the polite rewriting prompt
template = "Rewrite the following sentence politely:\n\n{sentence}"
prompt = PromptTemplate(input_variables=["sentence"], template=template)

# Create the LLM chain
# chain = LLMChain(prompt=prompt, llm=llm)

# ✅ Modern LangChain Composition (no more LLMChain)
chain = prompt | llm

# Example input
input_sentence = "Send me the report now!"

# Run inference using the modern method (.invoke)
result = chain.invoke({"sentence": input_sentence})
print("Original sentence:", input_sentence)
print("Polite version:", result)

# Initialize FastAPI app
app = FastAPI(title="LangChain Polite Rewriter API", version="1.0")

# Define input model
class SentenceRequest(BaseModel):
    sentence: str


@app.post("/rewrite")
async def rewrite_sentence(request: SentenceRequest):
    """API endpoint to rewrite any sentence politely."""
    answer = chain.invoke({"sentence": request.sentence})
    return {
        "original_sentence": request.sentence,
        "polite_version": answer.strip()
    }

@app.get("/")
async def root():
    return {"message": "LangChain Polite Rewriter API is running 🚀"}
