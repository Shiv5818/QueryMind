from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from pathlib import Path
from loguru import logger
from config.settings import settings

def get_embeddings():
    """
    Get a configured embeddings model with caching.
    
    Returns:
        A CacheBackedEmbeddings instance
        
    Raises:
        Exception: If the embeddings model initialization fails
    """
    try:
        # Create cache directory if it doesn't exist
        cache_dir = Path(settings.CACHE_DIR)
        cache_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize Google AI embeddings model
        model = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL, 
            api_key=settings.GOOGLE_API_KEY
        )
        
        # Set up caching for embeddings
        store = LocalFileStore(str(cache_dir))
        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
            model, 
            store, 
            namespace=model.model
        )
        
        logger.info(f"Initialized embeddings model {settings.EMBEDDING_MODEL} with caching")
        return cached_embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embeddings model: {str(e)}", exc_info=True)
        raise Exception(f"Embeddings initialization failed: {str(e)}")