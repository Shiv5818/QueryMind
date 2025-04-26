from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List
from loguru import logger
from config.settings import settings

class TextProcessor:
    """Text processing utilities for RAG."""
    
    @staticmethod
    def get_text_splitter() -> RecursiveCharacterTextSplitter:
        """
        Get a configured text splitter.
        
        Returns:
            A RecursiveCharacterTextSplitter instance
        """
        return RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " "]
        )
    
    @staticmethod
    def split_text(text: str) -> List[Document]:
        """
        Split text into chunks suitable for embedding.
        
        Args:
            text: The raw text to split
            
        Returns:
            A list of Document objects containing the text chunks
        """
        text_splitter = TextProcessor.get_text_splitter()
        docs = text_splitter.create_documents([text])
        
        logger.debug(f"Split text into {len(docs)} chunks")
        return docs
    
    @staticmethod
    def extract_texts_from_documents(docs: List[Document]) -> List[str]:
        """
        Extract raw text from Document objects.
        
        Args:
            docs: List of Document objects
            
        Returns:
            List of text strings
        """
        return [doc.page_content for doc in docs]