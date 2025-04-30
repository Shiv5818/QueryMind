from loguru import logger
from langchain_pinecone import PineconeVectorStore
from config.settings import settings
from core.llm import get_llm
from api.schemas import ChatRequest, ChatResponse
from typing import Dict, Any
from services.intent_detection_service import IntentDetectionService

# Initialize the intent detection service
intent_service = IntentDetectionService()

async def process_chat(request: ChatRequest, vector_store: PineconeVectorStore) -> ChatResponse:
    """
    Process incoming chat requests using intent detection to route to appropriate pipeline.
    
    Args:
        request: The chat request containing user message and history
        vector_store: Vector store for RAG retrieval
        
    Returns:
        Chat response with answer to user's query
    """
    try:
        logger.info(f"Processing chat request: '{request.message}'")
        
        # Use intent detection service to process the query
        response = await intent_service.process_query(request, vector_store)
        
        logger.info(f"Chat response generated successfully with {len(response.response)} characters")
        return response
        
    except Exception as e:
        logger.error(f"Chat processing failed: {str(e)}", exc_info=True)
        return ChatResponse(
            response="I'm sorry, I encountered an error while processing your request. Please try again or contact support if the issue persists.",
            metadata={"error": str(e)}
        )
