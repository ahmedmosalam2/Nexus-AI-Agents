from abc import ABC, abstractmethod
from typing import List, Any

class LLMinference(ABC):
    
    @abstractmethod
    def set_generate_model(self, model_id: str): 
        pass
    
    @abstractmethod
    def set_emmbed_model(self, model_id: str, model_size: int = None): 
        pass
    
    @abstractmethod
    async def generate_text(
        self, 
        prompt: str, 
        max_output_tokens: int, 
        temperature: float, 
        chat_history: list = []
    ) -> str: 
        pass
    
    @abstractmethod
    async def embed_text(self, text: str, document_type: str) -> List[float]: 
        pass
    
    @abstractmethod
    def construct_prompt(self, prompts: str, role: str) -> dict: 
        pass