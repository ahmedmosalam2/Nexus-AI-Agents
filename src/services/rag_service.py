from typing import List
from src.infrastructure.llm.generic_provider import GenericLLMProvider
from src.infrastructure.vector_store.vector_provider import VectorDBProvider
from src.infrastructure.chunking.recursive_chunker import RecursiveChunker
from src.infrastructure.llm.factory import LLMFactory


class RagService:
    def __init__(self):
        self.llm = LLMFactory.create_provider()
        
        self.vector_db = VectorDBProvider()
        self.chunker = RecursiveChunker()

    async def add_knowledge(self, text: str):

        embedding_vector = await self.llm.embed_text(text)
        await self.vector_db.add_documents(texts=[text], embeddings=[embedding_vector])
        print(f" Added: {text[:30]}...")

    async def search(self, query: str, k: int = 3) -> str:

        query_vector = await self.llm.embed_text(query)
        results = await self.vector_db.search(query_embedding=query_vector, k=k)
        
        found_texts = [res['content'] for res in results]
        return "\n".join(found_texts)

    async def ask(self, question: str) -> str:

        print(f" Thinking about: {question}")

        context = await self.search(question)
        
        if not context:
            return "No relevant information found in knowledge base."


        full_prompt = f"""
        Use the following pieces of context to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context:
        {context}
        
        Question: {question}
        """

        answer = await self.llm.generate_text(
            prompt=full_prompt,
            max_output_tokens=500,
            temperature=0.3
        )
        
        return answer