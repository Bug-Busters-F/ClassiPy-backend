from fastapi import APIRouter, HTTPException, Path
from ..database.crud import schemes
from ..services.search.classify_PN import classify_PN

router = APIRouter(
    prefix="/classify",
    tags=["Classificação IA"]
)

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