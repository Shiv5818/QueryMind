import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Pinecone Configuration
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "rag")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
    
    # LLM Models
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-pro")
    
    # Text Processing
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "10000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Vector Search
    SIMILARITY_TOP_K: int = int(os.getenv("SIMILARITY_TOP_K", "10"))  
    
    # File Storage
    CACHE_DIR: str = os.getenv("CACHE_DIR", "./cache/")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API Settings
    APP_TITLE: str = "RAG API"
    APP_DESCRIPTION: str = "RAG system with web crawling capabilities and conversation memory"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"

    def validate(self):
        """Validate that all required environment variables are set."""
        required_vars = ["GOOGLE_API_KEY", "PINECONE_API_KEY", "GEMINI_API_KEY"]
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Instantiate settings
settings = Settings()
try:
    settings.validate()
except ValueError as e:
    import sys
    print(f"Error in configuration: {e}", file=sys.stderr)
    sys.exit(1)
