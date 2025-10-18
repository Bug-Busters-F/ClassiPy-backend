from playwright.sync_api import sync_playwright
# playwright install chromium

class BrowserPool:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
        )

    def get_page(self):
        return self.context.new_page()

    def close(self):
        self.browser.close()
        self.playwright.stop()
