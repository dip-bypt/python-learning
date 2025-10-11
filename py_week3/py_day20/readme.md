# Day 20: Retrieval-Augmented Generation (RAG) Q&A Bot for School Report

## Comprehensive Learning Topics
- **Basic RAG (Retrieval-Augmented Generation):**
  - Concept of combining document retrieval with LLMs for more accurate, context-aware answers.
  - Use of embeddings and vector stores to enable semantic search over documents.
- **Practical Implementation:**
  - Load and parse a PDF (school_student_report.pdf) containing student results and class information.
  - Create a mini Q&A bot that can answer questions about the PDF content.

## Project Overview
This project demonstrates a simple RAG-based Q&A chatbot that answers questions about a school's student report card PDF. The bot uses document loaders, embeddings, a vector store, and an LLM to provide accurate, context-aware answers.

### Main Features
- **PDF Parsing:** Extracts text and tables from the provided school report PDF.
- **Chunking:** Splits extracted content into manageable chunks for embedding.
- **Embeddings & Vector Store:** Uses OpenAI embeddings and FAISS for efficient semantic search.
- **Conversational Q&A:** Integrates a conversational retrieval chain to answer user queries, including context retention and disambiguation.

## Example Console Session
```
If you have any questions regarding the school report or need information about a specific student, feel free to ask!

You: How much percentage did Ananya Iyer got in standard 2?
Bot: Ananya Iyer scored 63.96% in Standard 2.

You: how much percentage did Manav Desai got?
Bot: Manav Desai scored 91.96%.

You: Who is the class moniter of standard 3?
Bot: The class monitor of Standard 3 is Ankit Verma.

You: how much percentage did Manav got ?
Bot: There are multiple students named Manav. Could you please specify if you mean Manav Shukla or Manav Desai?

You: Manav Desai!
Bot: Manav Desai scored 91.96%.

You: quit
👋 Exiting chatbot. Goodbye!
```

## Code Structure
- **main.py:**
  - `extract_text_and_tables(pdf_path)`: Parses the PDF and extracts all text and tables.
  - `create_chunks(texts)`: Splits the extracted content into chunks for embedding.
  - `create_vector_store(chunks)`: Embeds the chunks and stores them in a FAISS vector store.
  - `create_chatbot(vector_store)`: Sets up a conversational retrieval chain for Q&A.
  - Console loop for interactive Q&A with context retention and disambiguation.

- **school_student_report.pdf:**
  - Contains student names, percentages, and class monitor information for multiple standards.
  - Used as the knowledge base for the Q&A bot.

- **test_main.py:**
  - Automated tests for PDF extraction, chunking, vector store creation, and chatbot Q&A.
  - Example test cases:
    - Querying for a student's percentage (e.g., "How much percentage did Ananya Iyer got in standard 2?").
    - Handling ambiguous names (e.g., "how much percentage did Manav got?").
    - Asking for class monitor information.
    - Disambiguation follow-up (e.g., "Manav Desai!").
  - All tests pass, confirming robust integration and answer accuracy.

## How to Use
1. Place your school report PDF as `school_student_report.pdf` in the `py_day20` folder.
2. Install dependencies (if not already):
   ```bash
   pip install -r requirement.txt
   ```
3. Run the main Q&A bot:
   ```bash
   python py_day20/main.py
   ```
4. Ask questions about students, percentages, or class monitors as shown in the example session.

## How to Run Test Cases
1. Make sure you have `pytest` installed:
   ```bash
   pip install pytest
   ```
2. Run the test suite from the project root:
   ```bash
   pytest py_day20/test_main.py
   ```
   All tests should pass, confirming the bot's accuracy and integration.

## Learning Outcomes
- Understand and implement the RAG (Retrieval-Augmented Generation) paradigm.
- Combine document loaders, embeddings, vector stores, and LLMs for practical Q&A systems.
- Handle conversational context and ambiguity in user queries.

---
**Task Recap:**
- Load a school report PDF.
- Build a mini Q&A bot using RAG principles.
- Enable users to ask questions and get accurate, context-aware answers from the document.
