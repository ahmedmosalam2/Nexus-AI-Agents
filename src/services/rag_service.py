from typing import List, Dict, Any
from src.infrastructure.llm.generic_provider import GenericLLMProvider
from src.infrastructure.vector_store.vector_provider import VectorDBProvider

class RagService:
    def __init__(self):

        self.llm = GenericLLMProvider()
        self.vector_db = VectorDBProvider()

    async def add_knowledge(self, text: str):

        embedding_vector = await self.llm.embed_text(text)
        await self.vector_db.add_documents(
            texts=[text],
            embeddings=[embedding_vector]
        )
        print(" Document added to knowledge base.")

    async def search(self, query: str, k: int = 5) -> List[str]:

        print(f" Searching for: {query}")
        query_vector = await self.llm.embed_text(query)
        
        results = await self.vector_db.search(
            query_embedding=query_vector, 
            k=k
        )
        found_texts = [res['content'] for res in results]
        
        return found_texts