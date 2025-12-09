from src.domain.interfaces.tool import BaseTool
from src.infrastructure.tools.scraper.bs4_scraper import BeautifulSoupScraper

class WebScraperTool(BaseTool):
    def __init__(self):
        self.scraper = BeautifulSoupScraper()

    @property
    def name(self) -> str:
        return "web_scraper"

    @property
    def description(self) -> str:
        return "Use this tool to read the full content of a specific webpage url."

    async def run(self, url: str) -> str:
        print(f"Nexus Agent is reading content from: {url}...")
        try:
            content = await self.scraper.scrape(url)
            

            if content.startswith("Error"):
                return f" {content}"
            
            if not content:
                return f"❌ Failed: Empty content returned from {url}."
            
            return f"--- Webpage Content ({url}) ---\n{content}\n-----------------------------------"
            
        except Exception as e:
            return f"Error scraping website: {str(e)}"