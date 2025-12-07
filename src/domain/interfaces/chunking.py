from abc import ABC, abstractmethod
from typing import List

class BaseChunker(ABC):
    @abstractmethod
    def chunk_text(self, text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
        pass