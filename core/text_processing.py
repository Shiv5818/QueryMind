# core/text_processing.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Optional, Dict, Any
from loguru import logger
from config.settings import settings
from core.llm import get_llm

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
    
    @staticmethod
    async def preprocess_chunks(chunks: List[str]) -> List[str]:
        """
        Preprocess text chunks before indexing them in the vector store.
        
        Args:
            chunks: List of raw text chunks to preprocess
            
        Returns:
            List of cleaned and structured text chunks
        """
        logger.info(f"Preprocessing {len(chunks)} chunks")
        
        processed_chunks = []
        llm = get_llm()
        
        for i, chunk in enumerate(chunks):
            logger.debug(f"Processing chunk {i+1}/{len(chunks)}")
            
            # Construct preprocessing prompt
            prompt = f"""You are a preprocessing assistant for a RAG pipeline. Below is a CHUNK of raw restaurant data. Your task is to:
1. Identify and RETAIN only facts about:
   - Restaurant name and location
   - Menu items (names, descriptions, prices)
   - Special features (vegetarian options, spice levels, allergens)
   - Operating hours and contact info
2. REMOVE any irrelevant or noisy content, including:
   - Navigation menus, boilerplate text, ads, or unrelated commentary
   - Repetitions, promotional slogans, or HTML tags
   - Any text not directly tied to the required facts above
3. CONDENSE the retained text by:
   - Summarizing long sentences into concise statements
   - Using bullet points for lists (e.g., menu items)
   - Merging similar data points where possible
4. ENSURE the processed output:
   - Does not exceed 500 tokens
   - Maintains semantic completeness (no half facts)
   - Uses a consistent structure with labeled sections
   - Special focus on: "name", "location", "menu", "features", "hours", "contact"

Format all extracted information in clear sections. If the chunk contains no relevant restaurant information, respond with "NO_RELEVANT_DATA".

Raw chunk:
{chunk}

Processed output:"""
            
            try:
                # Process with LLM
                response = await llm.ainvoke(prompt)
                processed_text = response.content.strip()
                
                # Only keep chunks with relevant data
                if processed_text != "NO_RELEVANT_DATA":
                    processed_chunks.append(processed_text)
                    
            except Exception as e:
                logger.error(f"Error preprocessing chunk {i+1}: {str(e)}")
                # Fall back to original chunk if preprocessing fails
                processed_chunks.append(chunk)
                
        logger.info(f"Preprocessing complete. {len(processed_chunks)} chunks retained")
        return processed_chunks

    @staticmethod
    def add_metadata_to_documents(docs: List[Document]) -> List[Document]:
        """
        Add metadata to Document objects based on their content.
        
        Args:
            docs: List of Document objects
            
        Returns:
            List of Document objects with enriched metadata
        """
        enriched_docs = []
        
        for doc in docs:
            content = doc.page_content
            metadata = doc.metadata if hasattr(doc, 'metadata') and doc.metadata else {}
            
            # Extract restaurant name if present (simple heuristic)
            name_indicators = ["Restaurant:", "Name:", "Welcome to"]
            for indicator in name_indicators:
                if indicator in content:
                    try:
                        name_line = [line for line in content.split('\n') if indicator in line][0]
                        restaurant_name = name_line.split(indicator)[1].strip()
                        metadata["restaurant_name"] = restaurant_name
                        break
                    except (IndexError, KeyError):
                        pass
            
            # Tag content types
            if "Menu" in content or "menu items" in content or "$" in content or "price" in content.lower():
                metadata["content_type"] = metadata.get("content_type", "") + " menu"
            
            if "hours" in content.lower() or "open" in content.lower() or "close" in content.lower():
                metadata["content_type"] = metadata.get("content_type", "") + " hours"
                
            if "location" in content.lower() or "address" in content.lower():
                metadata["content_type"] = metadata.get("content_type", "") + " location"
                
            if "allergen" in content.lower() or "vegetarian" in content.lower() or "vegan" in content.lower():
                metadata["content_type"] = metadata.get("content_type", "") + " dietary"
            
            # Add chunk length metadata
            metadata["token_count"] = len(content.split())
            
            # Create new document with metadata
            enriched_doc = Document(page_content=content, metadata=metadata)
            enriched_docs.append(enriched_doc)
        
        return enriched_docs