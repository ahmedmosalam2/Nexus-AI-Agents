import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from src.enums.BaseEnum import AgentRole

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: AgentRole
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Metadata: لتخزين المصادر (Citations) أو وقت المعالجة
    metadata: dict = Field(default_factory=dict)

class ChatSession(BaseModel):


    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    title: Optional[str] = "New Chat"
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_message(self, role: AgentRole, content: str, metadata: dict = None):

        msg = Message(
            role=role, 
            content=content, 
            metadata=metadata or {}
        )
        self.messages.append(msg)
        self.updated_at = datetime.utcnow()