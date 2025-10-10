# day16.py
import os
from typing import Any

"""
Day 16: Summarization + Keyword Extraction Chain (LangChain)

This file builds a two-step pipeline using LangChain:
 1) Summarize the input text
 2) Extract top-5 keywords from the summary

The code reads the OpenRouter API key from the environment and configures
LangChain's OpenAI-compatible client. For testing, `process_text` accepts a
callable `llm_callable` which can be used to provide a mock implementation.
"""


# Read OpenRouter API key from environment if present. We do NOT raise here so
# tests that inject a mock LLM can import this module without requiring a key.
try:
    # Attempt to load a local .env file (or .env.example) for convenience in dev
    from dotenv import load_dotenv
    base = os.path.dirname(__file__)
    env_path = os.path.join(base, ".env")
    example_path = os.path.join(base, ".env")
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
    elif os.path.isfile(example_path):
        load_dotenv(example_path)
        print(f"Loaded environment from {example_path} (fallback)")
except Exception:
    # dotenv not installed or no .env file present — continue and rely on env
    pass

openrouter_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")

# Helper to configure OPENAI env vars when using the real client
def _configure_openai_env():
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY (or OPENAI_API_KEY) environment variable is not set.")
    os.environ["OPENAI_API_KEY"] = key
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


def create_chain(llm: Any):
    """Create and return a SequentialChain that summarizes and extracts keywords.

    The function accepts an `llm` instance so tests can inject a mock object.
    """
    # Import LangChain classes lazily so tests that inject a mock LLM can
    # run without requiring the heavy langchain packages to be installed.
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain, SequentialChain

    # 1️⃣ Create prompt for summarization
    summary_prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in 3-4 sentences:\n\n{text}"
    )

    # 2️⃣ Create chain for summarization
    summary_chain = LLMChain(
        llm=llm,
        prompt=summary_prompt,
        output_key="summary"
    )

    # 3️⃣ Create prompt for keyword extraction
    keyword_prompt = PromptTemplate(
        input_variables=["summary"],
        template="Extract the top 5 important keywords from this summary:\n\n{summary}"
    )

    # 4️⃣ Create chain for keyword extraction
    keyword_chain = LLMChain(
        llm=llm,
        prompt=keyword_prompt,
        output_key="keywords"
    )

    # 5️⃣ Combine both chains
    overall_chain = SequentialChain(
        chains=[summary_chain, keyword_chain],
        input_variables=["text"],
        output_variables=["summary", "keywords"]
    )

    return overall_chain


def process_text(input_text: str, llm_callable=None):
    """Process text and return a dict with 'summary' and 'keywords'.

    If `llm_callable` is provided, it should be a callable that accepts the input
    text and returns a dict {'summary': ..., 'keywords': ...}. This is used for
    unit testing to avoid calling real LLMs.
    """
    if llm_callable:
        # Use injected mock callable for testing
        return llm_callable(input_text)

    # Lazy import/initialization of the real model (uses environment variables)
    # Configure OPENAI env vars from OPENROUTER_API_KEY if needed.
    _configure_openai_env()
    # Import ChatOpenAI locally so tests don't require langchain_openai to be installed.
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="openai/gpt-4o", temperature=0.7)
    chain = create_chain(llm)
    # invoke the chain
    result = chain.invoke({"text": input_text})
    return result


if __name__ == "__main__":
    # CLI behavior: prompt for text, run the chain and print results
    input_text = input("Enter text to process: ")
    result = process_text(input_text)

    print("\n🧾 Summary:\n", result["summary"])
    print("\n🔑 Keywords:\n", result["keywords"])
