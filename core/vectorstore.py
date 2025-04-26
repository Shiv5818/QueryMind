from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from typing import List
from loguru import logger
from config.settings import settings
from core.embeddings import get_embeddings

# Initialize Pinecone client
try:
    pc = Pinecone(
        api_key=settings.PINECONE_API_KEY,
        environment=settings.PINECONE_ENVIRONMENT
    )
    logger.info("Pinecone client initialized")
except Exception as e:
    logger.error(f"Failed to initialize Pinecone client: {str(e)}", exc_info=True)
    raise RuntimeError(f"Pinecone initialization failed: {str(e)}")

def get_vector_store():
    """
    Get an initialized vector store instance.
    
    Returns:
        A PineconeVectorStore instance connected to the configured index
        
    Raises:
        Exception: If the vector store initialization fails
    """
    try:
        embeddings = get_embeddings()
        vector_store = PineconeVectorStore.from_existing_index(
            index_name=settings.PINECONE_INDEX_NAME, 
            embedding=embeddings
        )
        
        logger.info(f"Connected to Pinecone index: {settings.PINECONE_INDEX_NAME}")
        return vector_store
    except Exception as e:
        logger.error(f"Failed to connect to vector store: {str(e)}", exc_info=True)
        raise Exception(f"Vector store initialization failed: {str(e)}")

def index_texts(texts: List[str]):
    """
    Index a list of texts into the vector store.
    
    Args:
        texts: List of text strings to index
        
    Returns:
        Number of texts successfully indexed
        
    Raises:
        Exception: If indexing fails
    """
    try:
        embeddings = get_embeddings()
        vector_store = PineconeVectorStore.from_texts(
            texts, 
            embedding=embeddings, 
            index_name=settings.PINECONE_INDEX_NAME
        )
        
        logger.info(f"Indexed {len(texts)} texts into Pinecone")
        return len(texts)
    except Exception as e:
        logger.error(f"Failed to index texts: {str(e)}", exc_info=True)
        raise Exception(f"Indexing failed: {str(e)}")