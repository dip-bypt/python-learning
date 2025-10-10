from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory  # ✅ Correct import path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize model
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")

# Create the conversation prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant that answers user queries."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# Store conversation memory in memory (can later use Redis or DB)
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retrieve or create new session history."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Build the conversation chain with memory
conversation = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# -----------------------------------
# 🚀 FastAPI Application
# -----------------------------------
app = FastAPI(title="LangChain Q&A API", version="2.0")

class QARequest(BaseModel):
    question: str
    session_id: str = "default"  # You can use different session IDs for multi-user chat


@app.post("/qa")
async def qa_endpoint(request: QARequest):
    """Answer questions using memory-enabled conversation."""
    result = conversation.invoke(
        {"question": request.question},
        config={"configurable": {"session_id": request.session_id}}
    )
    return {
        "question": request.question,
        "answer": result.content,
        "session_id": request.session_id
    }


@app.get("/")
async def root():
    return {"message": "LangChain Q&A API (v2.0) is running 🚀"}


# -----------------------------------
# 💬 Console Chat Mode (no warnings)
# -----------------------------------
if __name__ == "__main__":
    print("🧠 Conversational Q&A Mode (Modern API)")
    print("Type 'quit' to end.\n")

    session_id = "console_session"

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ["quit", "exit", "bye"]:
            print("👋 Conversation ended. Goodbye!")
            break

        result = conversation.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}}
        )
        print("AI:", result.content)
