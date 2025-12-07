from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DocumentStore(ABC):


    @abstractmethod
    def add_documents(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):

        pass

    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:

        pass
    
    @abstractmethod
    def delete(self, document_id: str):
  
        pass