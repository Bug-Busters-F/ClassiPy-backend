from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..database.crud import schemes
from ..services.search.classify_PN import classify_PN

router = APIRouter(
    prefix="/classify",
    tags=["Classificação IA"]
)

class BulkPartNumbers(BaseModel):
    part_numbers: List[str]

class BulkClassificationResult(BaseModel):
    part_number: str
    classification: Optional[schemes.ClassificationResponse] = None
    error: Optional[str] = None

@router.get("/{part_number}", response_model = schemes.ClassificationResponse)
def getClassification(
    part_number: str = Path(..., title = "Part Number", min_length = 1)
):
    """
    Recebe um Part Number, busca a classificação usando o serviço
    e retorna os dados formatados.
    """
    try:
        response_data = classify_PN(part_number)

        if not response_data or response_data.get("error"):
            error_detail = response_data.get("error", "Não foi possível obter a classificação da IA.")
            print(f"❌ Erro na classificação de {part_number}: {error_detail}")
            raise HTTPException(
                status_code = 500, 
                detail = error_detail
            )
        return response_data
    
    except Exception as e:
        print(f"❌ Erro inesperado em /classify/{part_number}: {str(e)}")
        raise HTTPException(
            status_code = 500, 
            detail = f"Erro interno do servidor ao processar a classificação: {str(e)}"
        )

def process_part_number_wrapper(part_number: str):
    """
    Wrapper to handle classification and exceptions for a single part number.
    """
    try:
        response_data = classify_PN(part_number)
        if not response_data or response_data.get("error"):
            error_detail = response_data.get("error", f"Não foi possível obter a classificação da IA para {part_number}.")
            return BulkClassificationResult(part_number=part_number, error=error_detail)
        
        classification = schemes.ClassificationResponse(**response_data)
        return BulkClassificationResult(part_number=part_number, classification=classification)
    except Exception as e:
        error_detail = f"Erro interno do servidor ao processar a classificação para {part_number}: {str(e)}"
        return BulkClassificationResult(part_number=part_number, error=error_detail)

@router.post("/bulk", response_model=List[BulkClassificationResult])
def get_bulk_classification(payload: BulkPartNumbers):
    """
    Recebe uma lista de Part Numbers, busca a classificação para cada um de forma concorrente
    e retorna uma lista de dados formatados.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        future_to_part_number = {executor.submit(process_part_number_wrapper, pn): pn for pn in payload.part_numbers}
        for future in as_completed(future_to_part_number):
            results.append(future.result())
    
    return results