import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

load_dotenv()


# === STEP 1: Load & Parse PDF ===
def extract_text_and_tables(pdf_path):
    print("📘 Parsing PDF and extracting text + tables...")
    all_texts = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                all_texts.append(text)

            tables = page.extract_tables()
            for table in tables:
                headers = table[0]
                for row in table[1:]:
                    if len(row) == len(headers):
                        # Create a fact-style sentence
                        sentence_parts = []
                        for h, v in zip(headers, row):
                            if v and v.strip():
                                sentence_parts.append(f"{h.strip()}: {v.strip()}")
                        structured_sentence = (
                                " | ".join(sentence_parts)
                                + ". This data belongs to the school's academic records."
                        )
                        all_texts.append(structured_sentence)
    return all_texts


# === STEP 2: Create Document Chunks ===
def create_chunks(texts):
    print("✂️ Splitting extracted text into manageable chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    joined_text = "\n\n".join(texts)
    return splitter.split_text(joined_text)


# === STEP 3: Create Embeddings and FAISS Vector Store ===
def create_vector_store(chunks):
    print("🧩 Creating embeddings using OpenAI...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.from_texts(chunks, embeddings)


# === STEP 4: Build Chat Model with Memory ===
def create_chatbot(vector_store):
    print("🤖 Initializing school Q&A chatbot...")
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0.2
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    # ✅ Proper PromptTemplate instead of raw string
    context_prompt = PromptTemplate.from_template("""
You are a school report Q&A assistant.
The document contains details of multiple standards (1st–10th), teachers, and students.
Each table represents one standard and includes student names, roll numbers, percentages, and remarks.
Use the extracted table and text data to answer precisely and clearly.
If a question mentions a student (like “What percentage did Rohan get?”),
find that student’s data from any table.
If multiple matches exist, ask the user which standard or full name they mean.
If data is unavailable, politely say you don’t have that information.

Chat history:
{chat_history}

Context:
{context}

Question:
{question}
""")

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": context_prompt},
    )

    return qa_chain


# === STEP 5: Main Chat Loop ===
def main():
    pdf_path = "py_day20/school_student_report.pdf"
    texts = extract_text_and_tables(pdf_path)
    print(f"✅ Loaded {len(texts)} text/table segments from the school report.")

    chunks = create_chunks(texts)
    vector_store = create_vector_store(chunks)

    chatbot = create_chatbot(vector_store)

    print("🧠 School Report Q&A Chatbot Ready! Type your question or 'quit' to exit.")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["quit", "exit"]:
            print("👋 Exiting chatbot. Goodbye!")
            break
        result = chatbot({"question": query})
        print(f"Bot: {result['answer']}")


if __name__ == "__main__":
    main()
