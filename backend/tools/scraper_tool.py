from playwright.sync_api import sync_playwright
from markdownify import markdownify
from crewai.tools import BaseTool  
from pydantic import BaseModel, Field

class ScraperInput(BaseModel):
    url: str = Field(description="URL to scrape")

class WebScraperTool(BaseTool):
    name: str = "scrape_page"
    description: str = "Extract full text content from a webpage"
    args_schema: type[BaseModel] = ScraperInput

    def _run(self, url: str) -> str:
        # ✅ Basic URL validation
        if not url.startswith(("http://", "https://")):
            return "Error: Invalid URL — must start with http:// or https://"

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                try:
                    page = browser.new_page()

                    # ✅ Block images/fonts to speed up scraping
                    page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf}",
                               lambda route: route.abort())

                    page.goto(url, timeout=30000, wait_until="domcontentloaded")

                    # ✅ Wait for body to be ready
                    page.wait_for_selector("body", timeout=5000)

                    html = page.content()
                finally:
                    browser.close()

        except Exception as e:
            return f"Error scraping {url}: {str(e)}"

        markdown = markdownify(html, heading_style="ATX")

        # ✅ Clean up excessive whitespace
        import re
        markdown = re.sub(r'\n{3,}', '\n\n', markdown).strip()

        # ✅ Trim to token limit
        return markdown[:1000] if len(markdown) > 4000 else markdown
