from fastapi import FastAPI, UploadFile, File, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
import tempfile

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="PDF Summarizer API", version="1.0")

# Initialize the LLM
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the summarization prompt
summary_template = """
Summarize the following text into a concise paragraph:

{text}
"""
prompt = PromptTemplate(input_variables=["text"], template=summary_template)

# Modern LangChain composition
chain = prompt | llm

@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    """API endpoint to summarize an uploaded PDF file."""
    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Load and process the PDF
    try:
        loader = PyPDFLoader(tmp_path)
        pages = loader.load()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid or corrupted PDF file: {str(e)}")

    # Summarize each page
    page_summaries = []
    for i, page in enumerate(pages, 1):
        text = page.page_content[:3000]  # limit text for safety
        summary = chain.invoke({"text": text})
        print(f"\n📄 Page {i} summary:\n{summary}\n")
        page_summaries.append(summary.strip())

    # Combine all summaries
    final_summary = "\n".join(page_summaries)
    return {"summary": final_summary}


# -------- Example console demonstration --------
if __name__ == "__main__":
    example_pdf = "py_day17/sample.pdf"

    if os.path.exists(example_pdf):
        loader = PyPDFLoader(example_pdf)
        pages = loader.load()

        combined_text = " ".join([p.page_content for p in pages[:2]])  # take first 2 pages
        result = chain.invoke({"text": combined_text})
        print("\n✅ Example Summary from 2-page PDF:\n")
        print(result)
    else:
        print("\n⚠️ No example PDF found. Please add 'sample.pdf' in py_day17 folder.")
