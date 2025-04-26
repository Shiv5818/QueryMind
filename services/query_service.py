from loguru import logger
from langchain_pinecone import PineconeVectorStore
from config.settings import settings
from api.schemas import QueryResponse

async def process_query(query: str, vector_store: PineconeVectorStore) -> QueryResponse:
    """
    Process a query against the vector store.
    
    Args:
        query: The search query string
        vector_store: The vector store to search in
        
    Returns:
        QueryResponse object with search results
        
    Raises:
        Exception: If the query process fails
    """
    try:
        # Search for similar documents
        logger.info(f"Performing similarity search for query: '{query}'")
        results = vector_store.similarity_search(
            query, 
            k=settings.SIMILARITY_TOP_K
        )
        
        # Extract and return results
        hits = [doc.page_content for doc in results]
        logger.info(f"Found {len(hits)} results for query")
        
        return QueryResponse(
            query=query,
            results=hits
        )
    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}", exc_info=True)
        raise Exception(f"Query processing failed: {str(e)}")