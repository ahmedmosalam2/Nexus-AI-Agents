import aiohttp
from typing import List
from src.domain.interfaces.llm import LLMinference
from src.config.settings import settings

class GenericLLMProvider(LLMinference):
    def __init__(self, base_url: str = None):
        # الإعدادات الافتراضية
        self.base_url = base_url or "http://localhost:11434/v1"
        self.gen_model = settings.DEFAULT_MODEL
        self.embed_model = settings.EMBEDDING_MODEL
        self.api_key = "ollama" 

    def set_generate_model(self, model_id: str):
        self.gen_model = model_id
        print(f"Switched Generation Model to: {self.gen_model}")


    def set_emmbed_model(self, model_id: str, model_size: int = None):
        self.embed_model = model_id
        print(f"Switched Embedding Model to: {self.embed_model}")

    def construct_prompt(self, prompts: str, role: str) -> dict:
        return {"role": role, "content": prompts}

    async def generate_text(
        self, 
        prompt: str, 
        max_output_tokens: int, 
        temperature: float, 
        chat_history: list = []
    ) -> str:
        url = f"{self.base_url}/chat/completions"
        

        messages = chat_history.copy()
  
        current_msg = self.construct_prompt(prompt, "user")
        messages.append(current_msg)

        payload = {
            "model": self.gen_model,
            "messages": messages,
            "max_tokens": max_output_tokens,
            "temperature": temperature,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: {await response.text()}")
                
                data = await response.json()
                return data["choices"][0]["message"]["content"]


    async def embed_text(self, text: str, document_type: str = "document") -> List[float]:

        url = "http://localhost:11434/api/embeddings"
        
        payload = {
            "model": self.embed_model,
            "prompt": text
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Embed Error: {await response.text()}")
                
                data = await response.json()
                return data["embedding"]
            