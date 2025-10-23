from playwright.async_api import async_playwright

class BrowserPool:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
        )

    async def get_page(self):
        return await self.context.new_page()

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()
