import re
from markdownify import markdownify
from src.services.scraping.browser_pool import BrowserPool

browser_pool = BrowserPool()

def VisitWebpage(url: str, max_length: int = 5000) -> str:
    """
    Visita uma página, renderiza JS e retorna o conteúdo da tabela de atributos (#partDataAttHeader) em Markdown.
    """
    try:
        page = browser_pool.get_page()
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Seleciona apenas a seção de atributos da peça
        part_data_html = page.eval_on_selector(
            "#partDataAttHeader", "element => element.innerHTML"
        )
        page.close()

        markdown_content = markdownify(part_data_html).strip()
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        if len(markdown_content) > max_length:
            markdown_content = markdown_content[:max_length] + "\n\n...[content truncated]"

        return markdown_content

    except Exception as e:
        return f"Erro ao acessar/renderizar a página: {str(e)}"