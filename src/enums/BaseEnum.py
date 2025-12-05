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