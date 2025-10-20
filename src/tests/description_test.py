from src.services.scraping.visit_webpage import VisitWebpage
from src.services.ai.ollama_service import run_ollama
from src.services.search.findchips_search import DuckDuckGoFindChips

pn = "CL10C330JB8NNNC"
search_tool_findchips = DuckDuckGoFindChips()
links = search_tool_findchips.search(pn)

print("Links encotrados para o PN "+pn+":")
print(links)
print("\n\n")
print("Conteudo raspado (link: "+links[0]+"):")
# conteudo = VisitWebpage("https://www.findchips.com/detail/CL10C330JB8NNNC/Samsung-Electro--Mechanics")
conteudo = VisitWebpage(links[0])
print(conteudo)
print("\n\n")
print("Resposta do Ollama:")
print(run_ollama("extract_part_info",conteudo))