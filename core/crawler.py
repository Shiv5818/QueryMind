import asyncio
from crawl4ai import AsyncWebCrawler
from loguru import logger

class WebCrawlerManager:
    """Manager for web crawling operations."""
    
    @staticmethod
    async def crawl_url(url: str) -> str:
        """
        Crawl a URL and extract the content as markdown.
        
        Args:
            url: The URL to crawl
            
        Returns:
            The extracted content as markdown text
            
        Raises:
            Exception: If crawling fails
        """
        logger.debug(f"Starting crawl for URL: {url}")
        
        try:
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
                markdown_text = result.markdown
                
            logger.debug(f"Crawl completed for {url}, extracted {len(markdown_text)} characters")
            return markdown_text
        except Exception as e:
            logger.error(f"Crawl failed for URL {url}: {str(e)}", exc_info=True)
            raise Exception(f"Failed to crawl URL: {str(e)}")