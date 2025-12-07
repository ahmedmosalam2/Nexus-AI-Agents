from src.domain.interfaces.tool import BaseTool
from src.infrastructure.tools.search.duckduckgo import DuckDuckGoSearch

class WebSearchTool(BaseTool):
    def __init__(self, max_results: int = 5):
        self.max_results = max_results

        self.provider = DuckDuckGoSearch()

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "Search the internet for current information using DuckDuckGo."

    async def run(self, query: str) -> str:
 
        raw_results = await self.provider.search(query, self.max_results)
        
        if not raw_results:
            return "No results found."

        report = "Web Search Results:\n"
        for i, res in enumerate(raw_results, 1):
            report += f"{i}. {res['title']}\n   Link: {res['url']}\n   Summary: {res['content']}\n\n"
            
        return report