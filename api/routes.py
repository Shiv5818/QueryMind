from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from langchain_pinecone import PineconeVectorStore
import time
from loguru import logger

from api.schemas import (
    CrawlRequest, CrawlResponse,
    QueryRequest, QueryResponse,
    ChatRequest, ChatResponse,
    ErrorResponse
)
from api.dependencies import get_vector_store_with_error_handling
from services.crawl_service import process_crawl
from services.query_service import process_query
from services.chat_service import process_chat

# Create router
api_router = APIRouter(prefix="/api")

@api_router.post(
    "/crawl", 
    response_model=CrawlResponse, 
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"}
    }
)
async def crawl_endpoint(request: CrawlRequest):
    """
    Crawl a website and index its content into the vector store.
    
    Args:
        request: The crawl request containing the URL to crawl
        
    Returns:
        Information about the crawled and indexed content
    """
    logger.info(f"Crawl request received for URL: {request.url}")
    start_time = time.time()
    
    try:
        result = await process_crawl(str(request.url))
        
        elapsed_time = time.time() - start_time
        logger.info(f"Crawl completed in {elapsed_time:.2f}s: {result.chunk_count} chunks, {result.indexed_count} indexed")
        
        return result
    except Exception as e:
        logger.error(f"Error during crawl operation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Crawling failed: {str(e)}"
        )

@api_router.post(
    "/query", 
    response_model=QueryResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"}
    }
)
async def query_endpoint(
    request: QueryRequest, 
    vector_store: PineconeVectorStore = Depends(get_vector_store_with_error_handling)
):
    """
    Query the vector store for relevant documents.
    
    Args:
        request: The query request containing the search query
        vector_store: The vector store to search in (injected dependency)
        
    Returns:
        Query results containing matching documents
    """
    logger.info(f"Query request received: '{request.query}'")
    start_time = time.time()
    
    try:
        result = await process_query(request.query, vector_store)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Query completed in {elapsed_time:.2f}s: {len(result.results)} results found")
        
        return result
    except Exception as e:
        logger.error(f"Error during query operation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )

@api_router.post(
    "/chat", 
    response_model=ChatResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"}
    }
)
async def chat_endpoint(
    request: ChatRequest, 
    vector_store: PineconeVectorStore = Depends(get_vector_store_with_error_handling)
):
    """
    Chat with the RAG-enhanced assistant.
    
    Args:
        request: The chat request containing the user message and optional conversation history
        vector_store: The vector store to search in (injected dependency)
        
    Returns:
        The assistant's response based on retrieved documents and conversation context
    """
    logger.info(f"Chat request received: '{request.message}'")
    start_time = time.time()
    
    try:
        result = await process_chat(request, vector_store)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Chat completed in {elapsed_time:.2f}s")
        
        return result
    except Exception as e:
        logger.error(f"Error during chat operation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )