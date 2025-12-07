import aiohttp
from typing import List
from src.domain.interfaces.llm import LLMinference
from src.config.settings import settings

class GenericLLMProvider(LLMinference):
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.gen_model = model
        self.embed_model = settings.EMBEDDING_MODEL

    async def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def set_generate_model(self, model_id: str):
        self.gen_model = model_id

    def set_emmbed_model(self, model_id: str, model_size: int = None):
        self.embed_model = model_id

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
        messages.append(self.construct_prompt(prompt, "user"))

        payload = {
            "model": self.gen_model,
            "messages": messages,
            "max_tokens": max_output_tokens,
            "temperature": temperature,
            "stream": False
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=await self._headers()) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Generate Error ({response.status}): {error_text}")
                    
                    data = await response.json()
                    # حماية إضافية: التأكد من وجود choices
                    if "choices" not in data or len(data["choices"]) == 0:
                        return "Error: No response from model."
                        
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                print(f" LLM Connection Error: {e}")
                raise e

    async def embed_text(self, text: str, document_type: str = "document") -> List[float]:

        url = f"{self.base_url}/api/embeddings" 
        

        if "googleapis" in self.base_url:
            url = "http://192.168.1.2:11434/api/embeddings"

        elif "/v1" in self.base_url:
            url = self.base_url.replace("/v1", "/api/embeddings")


        payload = {
            "model": self.embed_model,
            "prompt": text
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Embed Error: {await response.text()}")
                    data = await response.json()
                    return data["embedding"]
            except Exception as e:
                print(f" Embedding Error connecting to {url}: {e}")
                raise e