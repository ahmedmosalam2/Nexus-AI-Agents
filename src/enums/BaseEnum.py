from enum import Enum

class ModelProvider(str, Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    AZURE = "azure"
    GROQ = "groq" 

class VectorDBType(str, Enum):
    CHROMA = "chroma"
    PINECONE = "pinecone"
    PGVECTOR = "pgvector"
    QDRANT = "qdrant"

class AgentRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class EmbeddingModel(str, Enum):
    OPENAI_TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    OPENAI_TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    HUGGINGFACE_ALL_MiniLM_L6_V2 = "all-MiniLM-L6-v2"
    HUGGINGFACE_ALL_DistilRoBERTa_V1 = "all-DistilRoBERTa-v1"
    HUGGINGFACE_Sentence_Transformer_V1 = "sentence-transformers/all-mpnet-base-v2"
