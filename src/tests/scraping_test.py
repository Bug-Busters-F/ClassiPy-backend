from src.services.search.findchips_search import DuckDuckGoFindChips
from src.services.scraping.visit_webpage import VisitWebpage

search_tool_findchips = DuckDuckGoFindChips()
links = search_tool_findchips.search("CL10C330JB8NNNC")
print(links)

content = ""

for link in links:
    content = VisitWebpage(link)
    print(content)
