import os
from tavily import TavilyClient
from typing import List, Dict
from src.infrastructure.tools.search.base import SearchProvider
from src.config.settings import settings

class TavilySearch(SearchProvider):
    def __init__(self):

        api_key = settings.TAVILY_API_KEY
        if not api_key:
            raise ValueError(" TAVILY_API_KEY is missing in .env")
        
        self.client = TavilyClient(api_key=api_key)

    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        print(f"Tavily Searching for: {query}...")
        try:
  
            response = self.client.search(
                query=query, 
                search_depth="basic", 
                max_results=max_results,
                include_answer=True 
            )
            
            formatted_results = []
            

            if response.get("answer"):
                formatted_results.append({
                    "title": " Tavily AI Answer",
                    "url": "https://tavily.com",
                    "content": response["answer"]
                })

            for res in response.get("results", []):
                formatted_results.append({
                    "title": res.get("title"),
                    "url": res.get("url"),
                    "content": res.get("content")
                })
            
            return formatted_results
            
        except Exception as e:
            print(f" Tavily Error: {e}")
            return []