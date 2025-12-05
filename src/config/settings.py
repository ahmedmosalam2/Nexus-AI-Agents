from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    # --- Project Info ---
    PROJECT_NAME: str = "Nexus AI Agent"
    API_V1_STR: str = "/api/v1"
    debug: bool = False
    
    # --- Logging ---
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR


    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    DOCS_DIR: Path = DATA_DIR / "docs"


    OPENAI_API_KEY: str
    SECRET_KEY: str = "super-secret-key-change-it" 
    

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB: str = "nexus_db"
    POSTGRES_PORT: int = 5432

    DEFAULT_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    TEMPERATURE: float = 0.0

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()