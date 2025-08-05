# backend/utils/pdf_utils.py
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str, page_range: tuple = None) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    pages = range(len(doc)) if page_range is None else range(page_range[0], page_range[1] + 1)
    for i in pages:
        text += doc[i].get_text()
    return text

def save_text_as_pdf(text: str, output_path: str):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text, fontsize=12)
    doc.save(output_path)
    return output_path
