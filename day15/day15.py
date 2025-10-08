"""
Day 15: Using LangChain + OpenRouter (ChatOpenAI) to rewrite text

This example shows a minimal LangChain usage pattern:
 - Create a prompt template with input variables
 - Initialize an LLM client (ChatOpenAI via OpenRouter)
 - Build an LLMChain and run it with input data

Security note: Do NOT hard-code API keys in source code. This file reads the
OpenRouter API key from the environment variable OPENROUTER_API_KEY.
"""

import os
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI


# Try to load a local .env file first (useful for local development).
# If `.env` is not present, try `.env.example` as a fallback so users can run
# quickly if they placed the key there. This requires python-dotenv, but we
# gracefully continue if it's not installed.
try:
    from dotenv import load_dotenv
    base = os.path.dirname(__file__)
    env_path = os.path.join(base, ".env")
    example_path = os.path.join(base, ".env.example")
    if os.path.isfile(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
    elif os.path.isfile(example_path):
        load_dotenv(example_path)
        print(f"Loaded environment from {example_path} (fallback)")
    else:
        # No .env files found; continue — rely on already-set environment
        pass
except Exception:
    # python-dotenv not installed or other issue; continue and read environment
    pass

# Read API key from environment (safer than hard-coding)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY environment variable is not set. "
        "Set it before running this script (see day15/day15_instructions.txt)."
    )


# Initialize OpenRouter client via ChatOpenAI
# - model_name: the model on the OpenRouter / OpenAI side to use
# - temperature: controls randomness (0.0 = deterministic)
# - max_tokens: maximum tokens to generate
# - base_url: OpenRouter API endpoint
# - api_key: read securely from the environment
llm = ChatOpenAI(
    model_name="openai/gpt-4o",
    temperature=0.7,
    max_tokens=200,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


# Define a prompt template. PromptTemplate lets you define a reusable template
# with named input variables. Here the input variable is 'sentence'.
template = """
Rewrite the following sentence politely:

"{sentence}"
"""
prompt = PromptTemplate(input_variables=["sentence"], template=template)


# Create LLMChain: a LangChain utility that ties together a prompt and an LLM
chain = LLMChain(llm=llm, prompt=prompt)


# Example usage: run the chain with a sample sentence and print the result
input_sentence = "Give me your report by tomorrow."
result = chain.run({"sentence": input_sentence})

print("Original:", input_sentence)
print("Polite:", result)
