import os
from typing import Any, Optional

"""
Day 17: PDF Summarization using LangChain + OpenRouter

This script loads a PDF, splits it into chunks, and summarizes it using a
map-reduce summarization chain. The OpenRouter/OpenAI API key is read from
environment variables (or loaded from a local .env file if present).

For testing, `process_pdf` accepts an optional `llm_callable` so tests can
inject a mock and avoid network calls.
"""

# Try to load a local .env file for development convenience
try:
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
    pass


def process_pdf(pdf_path: str, llm_callable: Optional[Any] = None) -> str:
    """Summarize the PDF at `pdf_path` and return the summary string.

    If `llm_callable` is provided, it will be called with the list of document
    chunks and should return the final summary string. This allows unit tests
    to inject a mock pipeline.
    """
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # If a mock callable is provided, use it and return its result
    if llm_callable is not None:
        return llm_callable(pdf_path)

    # Try to use LangChain if available. If it's not installed, fall back to
    # local PDF text extraction (PyPDF2) or a binary fallback so the script
    # can still run for demo purposes.
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        langchain_available = True
    except Exception:
        langchain_available = False

    if not langchain_available:
        # Try to extract text with PyPDF2 if available
        try:
            import PyPDF2

            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join((page.extract_text() or "") for page in reader.pages)
            short = text.strip()[:1500]
            return "LOCAL_TEXT_SUMMARY (no langchain):\n" + (short or "(no extractable text)")
        except Exception:
            # Binary fallback
            with open(pdf_path, "rb") as f:
                data = f.read(1500)
            return "FALLBACK_BINARY_SUMMARY (no langchain/PyPDF2):\n" + repr(data)

    # LangChain is available; proceed to load and split the document
    from langchain_openai import ChatOpenAI
    from langchain.chains.summarize import load_summarize_chain

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # Ensure API key is set (use OPENROUTER_API_KEY or OPENAI_API_KEY)
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        # If there's no API key, return a local summary (first N chars) so the
        # script remains useful without network credentials.
        joined = "\n\n".join([getattr(d, "page_content", str(d)) for d in documents])
        return "LOCAL_SUMMARY (no API key):\n" + joined[:1500]

    os.environ["OPENAI_API_KEY"] = key
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    # Initialize model and summarization chain
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")

    # Run summarization and return result
    summary = chain.run(splits)
    return summary


if __name__ == "__main__":
    # Resolve sample.pdf relative to this file so running from repo root works
    base = os.path.dirname(__file__)
    pdf_path = os.path.join(base, "sample.pdf")

    # If sample.pdf is missing, try to create a small demo PDF using
    # reportlab (preferred) or PyPDF2; otherwise write a tiny placeholder.
    if not os.path.isfile(pdf_path):
        print(f"sample.pdf not found at {pdf_path}, attempting to create a demo PDF...")
        created = False
        try:
            from reportlab.pdfgen import canvas

            c = canvas.Canvas(pdf_path)
            c.setFont("Helvetica", 12)
            c.drawString(72, 720, "This is a demo PDF created by day17 for testing.")
            c.save()
            created = True
            print("Created sample.pdf using reportlab")
        except Exception:
            try:
                import PyPDF2

                writer = PyPDF2.PdfWriter()
                writer.add_blank_page(width=612, height=792)
                with open(pdf_path, "wb") as f:
                    writer.write(f)
                created = True
                print("Created blank sample.pdf using PyPDF2")
            except Exception:
                # Minimal placeholder PDF (may not be a full-featured PDF but
                # works as a binary fallback for demos)
                try:
                    with open(pdf_path, "wb") as f:
                        f.write(b"%PDF-1.1\n%\xe2\xe3\xcf\xd3\n1 0 obj<<>>endobj\ntrailer<></>\n%%EOF\n")
                    created = True
                    print("Wrote placeholder sample.pdf (binary fallback)")
                except Exception as e:
                    print(f"Could not create sample.pdf: {e}")

        if not created:
            print("Failed to create sample.pdf; will run demo mode with a mock summary.")
            # Create a dummy file so process_pdf's file-existence check passes,
            # but use a mock llm_callable to avoid actual parsing or network.
            try:
                with open(pdf_path, "w") as f:
                    f.write("Demo PDF content for day17 sample (not a real PDF).")
                demo_callable = lambda p: "DEMO SUMMARY: This is a demo summary because sample.pdf was not available."
                summary = process_pdf(pdf_path, llm_callable=demo_callable)
                print("\n📝 Document Summary (demo):\n")
                print(summary)
            except Exception as ee:
                print(f"Demo mode failed: {ee}")
            finally:
                # leave the dummy file for inspection
                pass
            # Exit after demo run
            raise SystemExit(0)

    # Quick sanity check for a valid PDF header before attempting to parse.
    try:
        with open(pdf_path, "rb") as f:
            header = f.read(5)
    except Exception:
        header = b""

    if not header.startswith(b"%PDF"):
        # Run demo mode to avoid parser errors on malformed PDFs
        demo_callable = lambda p: "DEMO SUMMARY: This is a demo summary because sample.pdf is not a valid PDF file."
        try:
            summary = process_pdf(pdf_path, llm_callable=demo_callable)
            print("\n📝 Document Summary (demo):\n")
            print(summary)
        except Exception as e:
            print(f"Demo mode failed: {e}")
    else:
        try:
            summary = process_pdf(pdf_path)
            print("\n📝 Document Summary:\n")
            print(summary)
        except Exception as e:
            print(f"Error: {e}")
