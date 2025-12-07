from abc import ABC, abstractmethod
from typing import List, Dict

class SearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:

        pass