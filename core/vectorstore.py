# This should be in core/vectorstore.py
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from typing import List, Optional, Dict, Any
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

def index_texts(texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None):
    """
    Index a list of texts into the vector store with optional metadata.
    
    Args:
        texts: List of text strings to index
        metadatas: Optional list of metadata dictionaries corresponding to each text
        
    Returns:
        Number of texts successfully indexed
        
    Raises:
        Exception: If indexing fails
    """
    try:
        embeddings = get_embeddings()
        
        # Different approach based on whether metadata is provided
        if metadatas:
            logger.info(f"Indexing {len(texts)} texts with metadata into Pinecone")
            vector_store = PineconeVectorStore.from_texts(
                texts,
                embedding=embeddings,
                metadatas=metadatas,  # Pass the metadata
                index_name=settings.PINECONE_INDEX_NAME
            )
        else:
            logger.info(f"Indexing {len(texts)} texts without metadata into Pinecone")
            vector_store = PineconeVectorStore.from_texts(
                texts,
                embedding=embeddings,
                index_name=settings.PINECONE_INDEX_NAME
            )
        
        logger.info(f"Successfully indexed {len(texts)} texts into Pinecone")
        return len(texts)
    except Exception as e:
        logger.error(f"Failed to index texts: {str(e)}", exc_info=True)
        raise Exception(f"Indexing failed: {str(e)}")