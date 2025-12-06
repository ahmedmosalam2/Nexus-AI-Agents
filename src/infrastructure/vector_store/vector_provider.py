import chromadb
import uuid
from typing import List, Dict, Any
from src.domain.interfaces.document_store import DocumentStore
from src.config.settings import settings
from src.enums.BaseEnum import VectorDBType # لو حبيت تستخدم الـ Enum مستقبلاً للاختيار

class VectorDBProvider(DocumentStore):
    def __init__(self, collection_name: str = "nexus_knowledge"):
      
        db_path = str(settings.DATA_DIR / "chroma_db")
        
        # تشغيل عميل Chroma (Persistent يعني بيحفظ الداتا على الهارد)
        self.client = chromadb.PersistentClient(path=db_path)
        
        # إنشاء المجموعة (Collection) أو تحميلها لو موجودة
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"Vector DB Initialized at: {db_path} | Collection: {collection_name}")

    async def add_documents(
        self, 
        texts: List[str], 
        embeddings: List[List[float]], 
        metadatas: List[Dict[str, Any]] = None
    ):
        """تخزين النصوص مع الـ Embeddings"""
        if not texts:
            return

        # لو مفيش ميتاداتا، نعمل قاموس فاضي لكل نص
        if metadatas is None:
            metadatas = [{} for _ in texts]
            
        # توليد ID عشوائي لكل مستند (ضروري للداتا بيز)
        ids = [str(uuid.uuid4()) for _ in texts]

        # الإضافة للداتا بيز
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    async def search(self, query: str = None, query_embedding: List[float] = None, k: int = 5) -> List[Dict[str, Any]]:
        """البحث باستخدام الـ Embedding (البحث الدلالي)"""
        # ChromaDB بترجع النتائج في شكل قوائم، محتاجين ننسقها
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        formatted_results = []
        # التأكد إن فيه نتائج رجعت
        if results and results['documents']:
            # تجميع النتائج في شكل قائمة من القواميس
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "score": results['distances'][0][i] if results['distances'] else 0.0
                })
                
        return formatted_results

    async def delete(self, document_id: str):

        self.collection.delete(ids=[document_id])