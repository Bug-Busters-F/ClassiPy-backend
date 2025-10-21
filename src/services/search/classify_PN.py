from src.services.processPN import process_part_number
from src.table_tipi.query import search_ncm

def classify_PN(pn_code):
    pn_info = process_part_number(pn_code, info=True)

    if not pn_info or "error" in pn_info:
        return {"error": "Não foi possível obter a descrição do part number."}

    descricao = pn_info.get("description", "").strip()
    key_words = pn_info.get("key_words", [])
    manufacturer = pn_info.get("manufacturer","")

    if not key_words:
        return {"error": "Nenhuma palavra-chave encontrada para o part number."}

    query_text = " ".join(key_words)

    print(query_text)

    results = search_ncm(query_text)
    if not results:
        return {"error": "Nenhum NCM encontrado para as palavras-chave geradas."}

    best_result = max(results, key=lambda r: r.get("score", 0))

    aliquota_str = str(best_result.get("Aliquota", "0")).replace(",", ".").replace("%", "").strip()
    try:
        aliquota_val = float(aliquota_str)
    except ValueError:
        aliquota_val = 0.0 

    final_result = {
        "ncm": best_result.get("NCM", "N/A"),
        "descricao": descricao,
        "fabricante":manufacturer,
        "descricao_ncm": best_result.get("Documento", "Descrição não disponível"),
        "score": round(float(best_result.get("score", 0)), 3),
        "aliquota": aliquota_val
    }

    return final_result


# Exemplo de uso
if __name__ == "__main__":
    pn_code = "CL10C330JB8NNNC"
    result_json = classify_PN(pn_code)
    print(result_json)

#Para testar execute "python -m src.services.search.classyfy_PN"