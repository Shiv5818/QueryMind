from loguru import logger
from langchain_pinecone import PineconeVectorStore
from config.settings import settings
from core.llm import get_llm
from api.schemas import ChatRequest, ChatResponse

async def process_chat(request: ChatRequest, vector_store: PineconeVectorStore) -> ChatResponse:
    """
    Process a chat request, retrieving relevant documents and generating a response.
    
    Args:
        request: The chat request containing the user message and optional conversation history
        vector_store: The vector store to search in
        
    Returns:
        ChatResponse object with the assistant's response
        
    Raises:
        Exception: If the chat process fails
    """
    try:
        # Retrieve relevant documents from vector store (reduced from 20 to 5)
        logger.info(f"Retrieving relevant documents for: '{request.message}'")
        docs = vector_store.similarity_search(
            request.message, 
            k=10  # Reduced from settings.SIMILARITY_TOP_K
        )
        context = "\n".join([doc.page_content for doc in docs])
        logger.debug(f"Retrieved {len(docs)} relevant documents")
        
        # Build conversation history string if available
        conversation_context = ""
        if request.conversation_history and len(request.conversation_history) > 0:
            logger.debug(f"Processing conversation history with {len(request.conversation_history)} messages")
            conversation_context = "Previous conversation:\n"
            for item in request.conversation_history:
                conversation_context += f"{item.role}: {item.content}\n"
            conversation_context += "\n"
        
        # Construct prompt with context and conversation history
        prompt = f"""Based on the following context and previous conversation, answer the user's question.

{conversation_context}
Context:
{context}

User's question: {request.message}

Please provide a helpful response based on the context information. If the answer cannot be found in the context, say so clearly but try to provide related information if possible.
"""
        
        # Get response from LLM
        logger.info("Generating response from LLM")
        llm = get_llm()
        response = await llm.ainvoke(prompt)
        response_text = response.content
        
        logger.debug(f"Generated response of {len(response_text)} characters")
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Chat processing failed: {str(e)}", exc_info=True)
        raise Exception(f"Chat processing failed: {str(e)}")
