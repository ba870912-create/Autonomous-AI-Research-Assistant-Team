from playwright.sync_api import sync_playwright
from markdownify import markdownify
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class ScraperInput(BaseModel):
    url: str = Field(description="URL to scrape")

class WebScraperTool(BaseTool):
    name: str = "scrape_page"
    description: str = "Extract full text content from a webpage"
    args_schema: type[BaseModel] = ScraperInput

    def _run(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=30000)
            html = page.content()
            browser.close()

        markdown = markdownify(html, heading_style="ATX")
        # Trim to first 4000 chars to stay within token limits
        return markdown[:4000]