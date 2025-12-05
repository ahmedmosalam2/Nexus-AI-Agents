from abc import ABC, abstractmethod
from typing import List

class LLMinference(ABC):
    @abstractmethod
    def set_generate_model(self, model_id: str): pass
    
    @abstractmethod
    def set_emmbed_model(self, model_id: str, model_size: int = None): pass
    
    @abstractmethod
    def generate_text(self, prompt: str, max_output_tokens: int, temperature: float, chat_history: list = []): pass
    
    @abstractmethod
    def embed_text(self, text: str, document_type: str): pass
    
    @abstractmethod
    def construct_prompt(self, prompts: str, role: str): pass