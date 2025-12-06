
from abc import ABC

from abc import abstractmethod
from typing import List
class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        pass
        
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass