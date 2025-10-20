from typing import List
from ddgs import DDGS
import re

# from src.services.search.web_search import DuckDuckGoSearch

class DuckDuckGoFindChips:
    """
    Realiza uma busca por um part number no DuckDuckGo, priorizando resultados
    do site FindChips.
    """
    def __init__(self, max_results: int = 3, **kwargs):
        self.max_results = max_results
        self.ddgs = DDGS(**kwargs)
        
        # self.fallback_search = DuckDuckGoSearch(max_results=max_results)

    def search(self, part_number: str) -> List[str]:
        query = f"site:findchips.com {part_number}"
        results = self.ddgs.text(query, max_results=self.max_results)

        urls = []
        if results:
            pattern = re.compile(
                rf"^https?://(www\.)?findchips\.com/detail/{re.escape(part_number)}(/[\w\-\.\(\)%]+)?/?$",
                re.IGNORECASE
            )
            urls = [
                r["href"]
                for r in results
                if r.get("href") and pattern.match(r["href"])
            ]

        # fallback caso nenhum resultado no findchips
        if not urls:
            print("[INFO] Nenhum resultado encontrado em Findchips")
            # urls = self.fallback_search.search(part_number)

        return urls
