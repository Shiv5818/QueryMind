# services/crawl_service.py

from loguru import logger
from core.crawler import WebCrawlerManager
from core.text_processing import TextProcessor
from core.vectorstore import index_texts
from api.schemas import CrawlResponse
from langchain.schema import Document

async def process_crawl(url: str) -> CrawlResponse:
    # Add these debug statements at the beginning of process_crawl in crawl_service.py
    print(f"TextProcessor class: {TextProcessor}")
    print(f"TextProcessor.split_text: {getattr(TextProcessor, 'split_text', 'NOT FOUND')}")
    """
    Process a crawl request for a URL with enhanced preprocessing and metadata.
    
    Args:
        url: The URL to crawl
        
    Returns:
        CrawlResponse object with information about the crawl operation
        
    Raises:
        Exception: If any step in the crawl process fails
    """
    try:
        # Step 1: Crawl the URL
        logger.info(f"Starting enhanced crawl process for URL: {url}")
        markdown_text = await WebCrawlerManager.crawl_url(url)
        
        # Step 2: Split the text into chunks
        docs = TextProcessor.split_text(markdown_text)
        texts = TextProcessor.extract_texts_from_documents(docs)
        raw_chunk_count = len(texts)
        logger.info(f"Generated {raw_chunk_count} raw text chunks from crawled content")
        
        # Step 3: Preprocess chunks with LLM
        processed_texts = await TextProcessor.preprocess_chunks(texts)
        processed_count = len(processed_texts)
        logger.info(f"After preprocessing: {processed_count} relevant chunks")
        
        # Step 4: Create new Document objects with processed text
        processed_docs = [Document(page_content=text) for text in processed_texts]
        
        # Step 5: Add metadata to documents
        enriched_docs = TextProcessor.add_metadata_to_documents(processed_docs)
        logger.info(f"Added metadata to {len(enriched_docs)} documents")
        
        # Step 6: Extract texts and metadata for indexing
        final_texts = TextProcessor.extract_texts_from_documents(enriched_docs)
        metadatas = [doc.metadata for doc in enriched_docs]
        
        # Step 7: Index the processed chunks with metadata into the vector store
        if processed_count > 0:
            # Pass both text and metadata to indexing function
            indexed_count = index_texts(
                texts=final_texts,
                metadatas=metadatas
            )
            logger.info(f"Successfully indexed {indexed_count} processed chunks into vector store")
        else:
            indexed_count = 0
            logger.warning("No relevant content chunks were found from the crawled URL")
        
        # Return the result
        return CrawlResponse(
            url=url,
            chunk_count=raw_chunk_count,
            processed_count=processed_count,
            indexed_count=indexed_count
        )
    except Exception as e:
        logger.error(f"Enhanced crawl process failed for URL {url}: {str(e)}", exc_info=True)
        raise Exception(f"Enhanced crawl processing failed: {str(e)}")