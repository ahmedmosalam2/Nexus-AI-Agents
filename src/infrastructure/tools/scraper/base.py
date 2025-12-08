from abc import ABC, abstractmethod

class BaseScraper(ABC):
    
    @abstractmethod
    async def scrape(self, url: str) -> str:

        pass