import re
from markdownify import markdownify
from src.services.scraping.browser_pool import BrowserPool
import asyncio

browser_pool = BrowserPool()

async def VisitWebpageAsync(url: str, max_length: int = 5000) -> str:
    """
    Visita uma página, renderiza JS e retorna o conteúdo relevante em Markdown.
    Se nenhum elemento for encontrado, retorna uma string vazia.
    """
    try:
        if browser_pool.context is None:
            await browser_pool.start()

        page = await browser_pool.get_page()
        await page.goto(url, wait_until="networkidle", timeout=30000)

        content_html_list = []

        part_info_html = await page.eval_on_selector(
            "div.analytics-part-info", "element => element.outerHTML"
        )
        if part_info_html:
            content_html_list.append(part_info_html)

        desc_html = await page.eval_on_selector(
            "p.part-description", "element => element.outerHTML"
        )
        if desc_html:
            content_html_list.append(desc_html)

        page_section_html = await page.eval_on_selector(
            "section#page", """
            element => {
                const infoHeader = element.querySelector('h2.part-class-desc');
                if (!infoHeader) return '';

                let htmlContent = '';
                let sibling = infoHeader.nextElementSibling;
                htmlContent += infoHeader.outerHTML;

                while (sibling && sibling.tagName.toLowerCase() !== 'h2') {
                    htmlContent += sibling.outerHTML;
                    sibling = sibling.nextElementSibling;
                }

                return htmlContent;
            }
        """
        )
        if page_section_html:
            content_html_list.append(page_section_html)

        table_rows_html = await page.eval_on_selector_all(
            "section#partDataAttHeader table.default-table tr.data-row",
            """
            rows => rows.map(row => {
                const key = row.querySelector('td.field-cell')?.innerText.trim();
                const value = row.querySelector('td.main-part-cell')?.innerText.replace(/\\s+/g,' ').trim();
                return `<p><strong>${key}</strong>: ${value}</p>`;
            }).join('')
            """
        )
        if table_rows_html:
            content_html_list.append(''.join(table_rows_html))

        await page.close()

        if not content_html_list:
            return ""

        combined_html = "\n".join(content_html_list)
        markdown_content = markdownify(combined_html).strip()
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        if len(markdown_content) > max_length:
            markdown_content = markdown_content[:max_length] + "\n\n...[content truncated]"

        return markdown_content

    except Exception:
        return ""
    
def VisitWebpage(url: str, max_length: int = 5000):
    """
    Wrapper síncrono/assíncrono para VisitWebpageAsync.
    """
    try:
        loop = asyncio.get_running_loop()
        return VisitWebpageAsync(url, max_length)
    except RuntimeError:
        return asyncio.run(VisitWebpageAsync(url, max_length))