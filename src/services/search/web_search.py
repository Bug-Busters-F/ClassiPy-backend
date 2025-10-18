from typing import List, Optional
from ddgs import DDGS

class DuckDuckGoSearch:
    def __init__(
        self,
        max_results: int = 3,
        sources: Optional[List[str]] = None,
        **kwargs
    ):
        self.max_results = max_results
        self.sources = sources or [
            "digikey.com",
            "octopart.com",
            "lcsc.com",
            "componentsearchengine.com",
            "alliedelec.com",
            "el-component.com"
        ]
        self.ddgs = DDGS(**kwargs)

    def search(self, part_number: str) -> List[str]:
        sources_query = " OR ".join([f"site:{s}" for s in self.sources])
        query = f"{part_number} {sources_query}"

        results = self.ddgs.text(query, max_results=self.max_results)
        if not results:
            return []

        return [r["href"] for r in results if r.get("href")]