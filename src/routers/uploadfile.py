import os
import hashlib
import pdfplumber
import src.services.read_pdf as read_pdf
from fastapi import APIRouter, UploadFile, File, HTTPException
import json

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def calculate_file_hash(file_bytes: bytes) -> str:
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()

@router.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()

    file_hash = calculate_file_hash(content)

    _, ext = os.path.splitext(file.filename)
    file_path = os.path.join(UPLOAD_DIR, f"{file_hash}{ext}")

    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Arquivo já enviado")

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        if ext.lower() == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                page = pdf.pages[0]
                page_words = page.extract_words()

                if not page_words[0]["text"] == "TECSYS":
                    pdf_text = " ".join([p["text"] for p in page_words])
                    result = read_pdf.find_PN_and_Adress_with_ai(pdf_text)
                else:
                    result = read_pdf.find_pn(page)
        else:
            result = "Arquivo não é PDF. Apenas PDFs são analisados."

        return json.loads(result)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Erro na análise do PDF: {str(e)}")

