# backend/agents/ocr_agent.py

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

def run_ocr_on_pdf(pdf_path: str) -> str:
    """
    Extracts visible text from PDF pages using Tesseract OCR.
    Returns combined OCR'd text from all pages.
    """
    doc = fitz.open(pdf_path)
    all_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)  # High-res for better OCR
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        all_text.append(text.strip())

    return "\n\n".join(all_text)
