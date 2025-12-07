from duckduckgo_search import DDGS
from typing import List, Dict
from src.infrastructure.tools.search.base import SearchProvider

class DuckDuckGoSearch(SearchProvider):
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        print(f" DuckDuckGo Searching for: {query}...")
        try:
            results = DDGS().text(keywords=query, max_results=max_results)
            formatted_results = []
            if results:
                for res in results:
                    formatted_results.append({
                        "title": res.get("title", ""),
                        "url": res.get("href", ""),
                        "content": res.get("body", "")
                    })
            return formatted_results
            
        except Exception as e:
            print(f" Search Error: {e}")
            return []