from src.services.processPN import process_part_number
from src.table_tipi.query import search_ncm

def classify_PN(pn_code):
    # Processa o Part Number
    pn_info = process_part_number(pn_code, info=True)

    if not pn_info or "error" in pn_info:
        return {"error": "Não foi possível obter a descrição do part number."}

    descricao = pn_info.get("description", "").strip()
    key_words = pn_info.get("key_words", [])
    manufacturer = pn_info.get("manufacturer", "")

    # Consulta ChromaDB usando a descrição
    results = search_ncm(descricao, top_k=3)
    if not results:
        return {"error": "Nenhum NCM encontrado para as palavras-chave geradas."}

    # Seleciona o resultado com maior score
    best_result = max(results, key=lambda r: r.get("score", 0))

    # Normaliza alíquota
    aliquota_str = str(best_result.get("aliquota", "0")).replace(",", ".").replace("%", "").strip()
    try:
        aliquota_val = float(aliquota_str)
    except ValueError:
        aliquota_val = 0.0 

    # Monta resultado final
    final_result = {
        "ncm": best_result.get("ncm", "N/A"),
        "descricao": descricao,
        "fabricante": manufacturer,
        "descricao_ncm": best_result.get("descricao_ncm", "Descrição não disponível"),
        "score": round(float(best_result.get("score", 0)), 3),
        "aliquota": aliquota_val
    }

    return final_result


# -------------------------
# Exemplo de uso
# -------------------------
if __name__ == "__main__":
    pn_code = "597-2401-407F"
    result_json = classify_PN(pn_code)
    print(result_json)


#Execute "python -m src.services.search.classify_PN" para testar