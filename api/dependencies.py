from fastapi import Depends, HTTPException, status
from core.vectorstore import get_vector_store
from core.embeddings import get_embeddings
from loguru import logger

async def get_vector_store_with_error_handling():
    """Dependency to get vector store with error handling."""
    try:
        vector_store = get_vector_store()
        return vector_store
    except Exception as e:
        logger.error(f"Error connecting to vector store: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector store service unavailable"
        )

async def get_embeddings_with_error_handling():
    """Dependency to get embeddings with error handling."""
    try:
        embeddings = get_embeddings()
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embeddings model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Embeddings service unavailable"
        )