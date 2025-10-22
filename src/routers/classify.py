from fastapi import APIRouter, HTTPException, Path
from ..database.crud import schemes
import json
import re
from ..services.search.classify_PN import classify_PN

router = APIRouter(
    prefix="/classify",
    tags=["Classificação IA"]
)

# Função auxiliar para extrair o dicionário da string da IA
def extractDict(response_string: str) -> dict | None:
    # Tenta encontrar a primeira ocorrência de '{' e a última de '}'
    start_index = response_string.find('{')
    end_index = response_string.rfind('}')

    if start_index != -1 and end_index != -1 and start_index < end_index:
        dict_str = response_string[start_index: end_index + 1]
        try:
            # Substitui aspas simples por aspas duplas para formar um JSON válido
            corrected_dict_str = dict_str.replace("'", '"')
            # Tenta carregar como JSON
            data = json.loads(corrected_dict_str)
            return data
        except json.JSONDecodeError:
            # Se falhar como JSON, tenta avaliar como Python literal
            try:
                data = eval(dict_str)
                if isinstance(data, dict):
                    return data
            except:
                return None # Falha ao extrair
    return None # Não encontrou um dicionário válido

@router.get("/{part_number}", response_model = schemes.ClassificationResponse)
async def getClassification(
    part_number: str = Path(..., title = "Part Number", min_length = 1)
):
    try:
        raw_response = classify_PN(part_number)
        print(f"Resposta bruta da IA para {part_number}: {raw_response}")

        extracted_data = extractDict(str(raw_response))

        if not extracted_data or not isinstance(extracted_data, dict):
            raise HTTPException(status_code = 500, detail = "Não foi possível extrair os dados da resposta da IA.")
        
        response_data = schemes.ClassificationResponse(
            ncm = extracted_data.get('ncm', 'N/A'),
            descricao = extracted_data.get('descricao', 'N/A'),
            fabricante = extracted_data.get('fabricante', 'N/A'),
            aliquota = float(extracted_data.get('aliquota', 0.0)),
            descricao_ncm = extracted_data.get('descricao_ncm', 'N/A')
        )    
            
        return response_data
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Erro ao classificar o Part Number: {str(e)}")