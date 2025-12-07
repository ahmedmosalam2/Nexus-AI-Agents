import chromadb
import uuid
from typing import List, Dict, Any
from src.domain.interfaces.document_store import DocumentStore
from src.config.settings import settings
from src.enums.BaseEnum import VectorDBType # لو حبيت تستخدم الـ Enum مستقبلاً للاختيار

class VectorDBProvider(DocumentStore):
    def __init__(self, collection_name: str = "nexus_knowledge"):
      
        db_path = str(settings.DATA_DIR / "chroma_db")

        self.client = chromadb.PersistentClient(path=db_path)
        
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"Vector DB Initialized at: {db_path} | Collection: {collection_name}")

    async def add_documents(
            self, 
            texts: List[str], 
            embeddings: List[List[float]], 
            metadatas: List[Dict[str, Any]] = None
        ):
        
            if not texts:
                return
            
            ids = [str(uuid.uuid4()) for _ in texts]
            final_metadatas = []
            
            if metadatas:
                for m in metadatas:
                    if not m: 
                        final_metadatas.append({"source": "unknown"}) 
                    else:
                        final_metadatas.append(m)
            else:
                
                final_metadatas = [{"source": "unknown"} for _ in texts]

            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=final_metadatas,
                ids=ids
            )

    async def search(self, query: str = None, query_embedding: List[float] = None, k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        formatted_results = []

        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "score": results['distances'][0][i] if results['distances'] else 0.0
                })
                
        return formatted_results

    async def delete(self, document_id: str):

        self.collection.delete(ids=[document_id])