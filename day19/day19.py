import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# --------------------------
# Load .env if exists
# --------------------------
try:
    from dotenv import load_dotenv
    base = os.path.dirname(__file__)
    env_path = os.path.join(base, ".env")
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
except Exception:
    pass

# --------------------------
# Import LangChain
# --------------------------
try:
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
except ModuleNotFoundError:
    print("Please install langchain: pip install langchain")
    raise

# --------------------------
# Ensure API key
# --------------------------
key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
if not key:
    raise RuntimeError("No API key found in environment. Set OPENROUTER_API_KEY or OPENAI_API_KEY.")
os.environ["OPENAI_API_KEY"] = key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

# --------------------------
# Initialize FastAPI
# --------------------------
app = FastAPI(title="Day19 LangChain Q&A API")

# --------------------------
# Request model
# --------------------------
class QARequest(BaseModel):
    text: str
    question: Optional[str] = None

# --------------------------
# Create LLM & Chain
# --------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Simple prompt template: answer question based on input text
prompt_template = """
Answer the question based on the following context:

Context:
{text}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(input_variables=["text", "question"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)

# --------------------------
# API endpoint: POST /qa
# --------------------------
@app.post("/qa")
async def qa_endpoint(request: QARequest):
    question = request.question or "Summarize the text."
    try:
        answer = chain.run({"text": request.text, "question": question})
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
