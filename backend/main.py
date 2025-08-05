# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
import uuid
import os

from crew.crew_setup import run_crew
from utils.pdf_utils import extract_text_from_pdf, save_redacted_pdf

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    file_paths = []
    for file in files:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        file_paths.append(file_path)
    return {"message": "Files uploaded successfully", "files": file_paths}


@app.post("/redact")
async def redact_pdfs(
    file_name: str = Form(...),
    fields: List[str] = Form(...),
    page_range: Optional[str] = Form(None),
    use_ocr: Optional[bool] = Form(False)
):
    full_path = os.path.join(UPLOAD_DIR, file_name)

    result = run_crew(full_path, use_ocr=use_ocr)

    redacted_path = save_redacted_pdf(file_name, result)
    return {
        "message": "Redaction complete",
        "download_url": f"/download?file_id={file_name}"
    }



@app.get("/preview")
async def preview_file(file_id: str):
    return {
        "message": f"Preview for {file_id}",
        "url": f"https://dummy-url/{file_id}_preview.pdf"
    }

@app.get("/download")
async def download_file(file_id: str):
    return {
        "download_url": f"https://storage.googleapis.com/my-bucket/{file_id}_redacted.pdf"
    }
