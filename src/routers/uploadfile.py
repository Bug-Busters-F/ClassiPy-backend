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

def safe_json_parse(possible_json):
    """Tenta extrair JSON válido de uma string ou retorna dict vazio"""
    if isinstance(possible_json, dict):
        return possible_json

    if not isinstance(possible_json, str):
        return {}

    start = possible_json.find("{")
    end = possible_json.rfind("}") + 1

    if start != -1 and end != -1:
        try:
            return json.loads(possible_json[start:end])
        except Exception:
            pass

    return {}

@router.post("/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    file_hash = calculate_file_hash(content)

    _, ext = os.path.splitext(file.filename)
    file_path = os.path.join(UPLOAD_DIR, f"{file_hash}{ext}")


    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(content)

    try:
        if ext.lower() != ".pdf":
            return {"erro": "Arquivo não é PDF. Apenas PDFs são analisados."}

        all_parts = []
        seen_pn = set() 

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                page_words = page.extract_words()

                if not page_words:
                    continue

                pdf_text = " ".join([p["text"] for p in page_words])

                if not page_words[0]["text"] == "TECSYS":
                    ai_result = read_pdf.find_PN_and_Adress_with_ai(pdf_text)
                    result_json = safe_json_parse(ai_result)
                else:
                    result_json = safe_json_parse(read_pdf.find_pn(page))


                for part in result_json.get("Parts", []):
                    pn = part.get("PartNumber")
                    if pn and pn not in seen_pn:
                        all_parts.append(part)
                        seen_pn.add(pn)

        if not all_parts:
            raise HTTPException(status_code=404, detail="Nenhuma peça foi identificada no PDF.")

        response = {
            "Parts": all_parts,
            "hash_code": file_hash
        }

        return response

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Erro na análise do PDF: {str(e)}")