from src.services.scraping.visit_webpage import VisitWebpage
from src.services.ai.ollama_service import run_ollama
from src.services.search.findchips_search import DuckDuckGoFindChips
import json

search_tool_findchips = DuckDuckGoFindChips()

def process_part_number(part_number: str, info: bool = False):
    try:
        links = search_tool_findchips.search(part_number)
        
        if not links:
            return {"erro: [ERRO] Nenhum link encontrado para o PN '{part_number}'"}
        
        contents = []
        for link in links:
            try:
                content = VisitWebpage(link)
                contents.append(content)
            except Exception as e:
                    print(f"[ERRO] Falha ao visitar {link}: {e}")
        full_content = "\n".join(contents)
            
        response = run_ollama("extract_part_info",full_content)
        
        if info:
            print(f"Links encotrados para o PN {part_number}:")
            print(links)
            print("\n---------------------------------------------------------------------\nConteudo raspado:")
            print(full_content)
            print("\n---------------------------------------------------------------------\nResposta do Ollama:")
        
        return response
    
    except Exception as e:
        print(f"[ERRO] Falha no processamento de {part_number}: {e}")
        return None
