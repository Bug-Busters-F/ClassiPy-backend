from typing import List
from ddgs import DDGS
import re
import time

class DuckDuckGoFindChips:
    """
    Realiza uma busca por um part number no DuckDuckGo, priorizando resultados
    do site FindChips, com até 3 tentativas automáticas.
    """
    def __init__(self, max_results: int = 3, max_retries: int = 3, retry_delay: float = 1.5, **kwargs):
        self.max_results = max_results
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.ddgs = DDGS(**kwargs)

    def search(self, part_number: str) -> List[str]:
        query = f"site:findchips.com {part_number}"

        for attempt in range(1, self.max_retries + 1):
            try:
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

                if urls:
                    return urls
                
                time.sleep(self.retry_delay)

            except Exception as e:
                print(f"[ERRO] Tentativa {attempt} falhou: {e}")
                time.sleep(self.retry_delay)

        print(f"[ERRO] Nenhum resultado encontrado para '{part_number}' após {self.max_retries} tentativas.")
        return []
