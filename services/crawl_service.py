from loguru import logger
from core.crawler import WebCrawlerManager
from core.text_processing import TextProcessor
from core.vectorstore import index_texts
from api.schemas import CrawlResponse

async def process_crawl(url: str) -> CrawlResponse:
    """
    Process a crawl request for a URL.
    
    Args:
        url: The URL to crawl
        
    Returns:
        CrawlResponse object with information about the crawl operation
        
    Raises:
        Exception: If any step in the crawl process fails
    """
    try:
        # Step 1: Crawl the URL
        logger.info(f"Starting crawl process for URL: {url}")
        markdown_text = await WebCrawlerManager.crawl_url(url)
        
        # Step 2: Split the text into chunks
        docs = TextProcessor.split_text(markdown_text)
        texts = TextProcessor.extract_texts_from_documents(docs)
        chunk_count = len(texts)
        logger.info(f"Generated {chunk_count} text chunks from crawled content")
        
        # Step 3: Index the chunks into the vector store
        if chunk_count > 0:
            indexed_count = index_texts(texts)
            logger.info(f"Successfully indexed {indexed_count} chunks into vector store")
        else:
            indexed_count = 0
            logger.warning("No content chunks were generated from the crawled URL")
        
        # Return the result
        return CrawlResponse(
            url=url,
            chunk_count=chunk_count,
            indexed_count=indexed_count
        )
    except Exception as e:
        logger.error(f"Crawl process failed for URL {url}: {str(e)}", exc_info=True)
        raise Exception(f"Crawl processing failed: {str(e)}")