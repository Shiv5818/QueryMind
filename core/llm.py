from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger
from config.settings import settings

def get_llm():
    """
    Get a configured language model.
    
    Returns:
        A ChatGoogleGenerativeAI instance
        
    Raises:
        Exception: If LLM initialization fails
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL, 
            api_key=settings.GEMINI_API_KEY
        )
        
        logger.info(f"Initialized LLM model: {settings.LLM_MODEL}")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}", exc_info=True)
        raise Exception(f"LLM initialization failed: {str(e)}")