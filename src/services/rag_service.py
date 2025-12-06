
from src.infrastructure.llm.generic_provider import GenericLLMProvider
from src.infrastructure.vector_store.vector_provider import VectorDBProvider
from typing import List, Dict, Any
from src.infrastructure.llm.factory import LLMFactory
from src.infrastructure.vector_store.chunking import RecursiveChunker

class RagService:
    def __init__(self):
       
        self.llm = LLMFactory.create_provider()  
        self.vector_db = VectorDBProvider()      
        self.chunker = RecursiveChunker()       

    async def add_knowledge(self, text: str, metadata: dict = None):
     
        print(" Chunking text...")

        chunks = self.chunker.chunk_text(text, chunk_size=500, chunk_overlap=50)
        print(f"Split text into {len(chunks)} chunks.")

        embeddings = []
        for chunk in chunks:
         
            emb = await self.llm.embed_text(chunk)
            embeddings.append(emb)
        
        metadatas_list = [metadata or {} for _ in chunks]
        
        await self.vector_db.add_documents(
            texts=chunks, 
            embeddings=embeddings, 
            metadatas=metadatas_list
        )
        print(f"Successfully stored {len(chunks)} chunks in Vector DB.")

    async def ask(self, question: str) -> str:
        print(f"Thinking about: {question}")
        
 
        query_vector = await self.llm.embed_text(question)

        results = await self.vector_db.search(query_embedding=query_vector, k=3)

        context_text = "\n\n".join([res['content'] for res in results])
        
        if not context_text:
            return "No relevant information found in knowledge base."


        full_prompt = f"""
        Use the following pieces of context to answer the user's question.
        If you don't know the answer, just say that you don't know.
        
        Context:
        {context_text}
        
        Question: {question}
        """

        answer = await self.llm.generate_text(
            prompt=full_prompt,
            max_output_tokens=1000,
            temperature=0.3
        )
        return answer