import os
import re
import pdfplumber
from langchain_core.documents import Document

# I switched from PyPDF to pdfplumber because:
# - PyPDF merges words together (e.g., "IntroductiontoResearch" instead of "Introduction to Research")
# - PyPDF extracts tables as garbled text
# - pdfplumber reads tables as structured data and preserves word spacing
# - This dramatically improves RAG search accuracy


def clean_text(text):
    """
    Clean extracted text to fix common PDF extraction issues.
    - Adds spaces between merged words (e.g., "IntroductiontoResearch" → "Introduction to Research")
    - Handles "Masterof" → "Master of", "Nameof" → "Name of" patterns
    - Normalizes whitespace
    """
    if not text:
        return ""

    # Fix merged words: add space before uppercase letter that follows a lowercase letter
    # "IntroductiontoResearchMethodology" → "Introductionto Research Methodology"
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Fix "Masterof" → "Master of", "Boardof" → "Board of", "Listof" → "List of"
    # Pattern: uppercase letter(s) followed by common short words without space
    text = re.sub(r'([a-z])(of|and|the|for|in|on|to|with|from|by|at|is|as|or|an)\b', r'\1 \2', text, flags=re.IGNORECASE)

    # Fix merged words: add space before a digit that follows a letter
    # "Unit1" → "Unit 1"
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)

    # Fix merged words: add space after a period/colon followed by a letter (no space)
    # "results.The" → "results. The"
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    text = re.sub(r':([A-Z])', r': \1', text)

    # Normalize multiple spaces/tabs into single space
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize multiple newlines into max 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def format_table(table):
    """
    Convert a pdfplumber table (list of rows) into a clean text representation.
    This makes tables searchable by the RAG pipeline.
    """
    if not table:
        return ""

    rows = []
    for row in table:
        # Replace None cells with empty string
        cleaned_cells = [str(cell).strip() if cell else "" for cell in row]
        # Skip completely empty rows
        if any(cell for cell in cleaned_cells):
            rows.append(" | ".join(cleaned_cells))

    return "\n".join(rows)


def load_single_pdf(file_path):
    """
    Load a single PDF file using pdfplumber.
    Extracts both regular text AND table data for much better accuracy.
    Returns a list of LangChain Document objects (one per page).
    """
    try:
        file_name = os.path.basename(file_path)
        pages = []

        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract regular text
                text = page.extract_text() or ""

                # Extract tables separately for structured data
                tables = page.extract_tables()
                table_text = ""
                if tables:
                    table_parts = []
                    for table in tables:
                        table_parts.append(format_table(table))
                    table_text = "\n\n".join(table_parts)

                # Combine text + tables (tables may contain info not in regular text)
                if table_text:
                    full_text = text + "\n\n[TABLE DATA]\n" + table_text
                else:
                    full_text = text

                # Clean up merged words and spacing issues
                full_text = clean_text(full_text)

                # Only add non-empty pages
                if full_text.strip():
                    doc = Document(
                        page_content=full_text,
                        metadata={
                            "page": page_num,
                            "source_file": file_name
                        }
                    )
                    pages.append(doc)

        print(f"Loaded {len(pages)} pages from: {file_name}")
        return pages

    except Exception as e:
        print(f"Error loading PDF {file_path}: {e}")
        return []


def load_all_pdfs(pdf_folder):
    """Load all PDF files from a folder and return all pages combined."""
    all_pages = []

    # Check if the folder exists
    if not os.path.exists(pdf_folder):
        print(f"PDF folder not found: {pdf_folder}")
        return all_pages

    # Find all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the folder.")
        return all_pages

    print(f"Found {len(pdf_files)} PDF files. Loading...")

    # Load each PDF one by one
    for pdf_file in pdf_files:
        file_path = os.path.join(pdf_folder, pdf_file)
        pages = load_single_pdf(file_path)
        all_pages.extend(pages)

    print(f"Total pages loaded: {len(all_pages)}")
    return all_pages
