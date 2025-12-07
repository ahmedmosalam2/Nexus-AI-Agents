from googlesearch import search
from typing import List, Dict
from src.infrastructure.tools.search.base import SearchProvider

class GoogleFreeSearch(SearchProvider):

    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        print(f"🔍 Google Searching for: {query}...")
        try:

            results = search(query, num_results=max_results, advanced=True)
            
            formatted_results = []
            for res in results:
                formatted_results.append({
                    "title": res.title,
                    "url": res.url,
                    "content": res.description 
                })
            
            return formatted_results
            
        except Exception as e:
            print(f" Google Search Error: {e}")
            return []