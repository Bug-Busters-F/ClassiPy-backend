import re
from markdownify import markdownify
from src.services.scraping.browser_pool import BrowserPool

browser_pool = BrowserPool()


def VisitWebpage(url: str, max_length: int = 10000) -> str:
    """
    Visita uma página (renderiza JS) e retorna seu conteúdo em Markdown.
    Usa um navegador persistente do Playwright.
    """
    try:
        page = browser_pool.get_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        html = page.content()
        page.close()

        markdown_content = markdownify(html).strip()
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        if len(markdown_content) > max_length:
            markdown_content = markdown_content[:max_length] + "\n\n...[content truncated]"

        return markdown_content
    except Exception as e:
        return f"Erro ao acessar/renderizar a página: {str(e)}"
