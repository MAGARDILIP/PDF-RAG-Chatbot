"""Debug script: See what PyPDF actually extracts from the PDF."""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from core.pdf_loader import load_single_pdf
from config import PDF_FOLDER

# Find the first PDF
pdfs = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
if not pdfs:
    print("No PDFs found!")
    sys.exit(1)

pdf_path = os.path.join(PDF_FOLDER, pdfs[0])
print(f"Inspecting: {pdfs[0]}\n")

pages = load_single_pdf(pdf_path)

# Find pages that mention "Semester" or "semester"
print("=" * 80)
print("PAGES THAT MENTION 'SEMESTER' (showing raw extracted text):")
print("=" * 80)

for page in pages:
    text = page.page_content
    page_num = page.metadata.get("page", "?")
    
    if "semester" in text.lower() or "sem" in text.lower():
        print(f"\n{'─' * 80}")
        print(f"PAGE {int(page_num) + 1} (first 2000 chars):")
        print(f"{'─' * 80}")
        print(text[:2000])
        print(f"... (total {len(text)} chars on this page)")
