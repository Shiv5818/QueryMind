from loguru import logger
from typing import Dict, Any, List, Tuple, Optional
from langchain_pinecone import PineconeVectorStore
from core.llm import get_llm
from api.schemas import ChatRequest, ChatResponse
import json
import os
from enum import Enum

class IntentPipeline(str, Enum):
    FILTER = "filter"
    RAG = "rag"

class IntentDetectionService:
    def __init__(self, hotel_data_path: str = "cache/lucknowi_thaath.json"):
        self.llm = get_llm()
        self.hotel_data = self._load_hotel_data(hotel_data_path)
        logger.info(f"Intent Detection Service initialized with {len(self.hotel_data) if self.hotel_data else 0} hotel records")
    
    def _load_hotel_data(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.debug(f"Successfully loaded hotel data from {file_path}")
                return data
            else:
                logger.warning(f"Hotel data file not found at {file_path}")
                return []
        except Exception as e:
            logger.error(f"Error loading hotel data: {str(e)}")
            return []
    
    async def detect_intent(self, query: str) -> Tuple[IntentPipeline, float]:
        prompt = f"""
        Analyze the following user query and determine which processing pipeline would be more appropriate:
        
        User Query: {query}
        
        Available processing pipelines:
        1. FILTER pipeline: Best for specific queries about hotel details, amenities, prices, availability, 
           or any factual information that would be found in structured data. Examples include room rates, 
           hotel facilities, check-in times, etc.
           
        2. RAG (Retrieval-Augmented Generation) pipeline: Best for complex queries requiring synthesis 
           of information, explanations, recommendations, comparisons, or any query that needs context from 
           multiple sources or reasoning beyond simple fact retrieval.
        
        Return your answer as a JSON with two fields:
        - "pipeline": Either "filter" or "rag"
        - "confidence": A number between 0 and 1 indicating your confidence in this choice
        - "reasoning": A brief explanation of why you selected this pipeline
        
        JSON Response:
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            response_text = response.content
            
            # Extract JSON from response
            result = json.loads(response_text.strip())
            pipeline = IntentPipeline(result.get("pipeline", "rag").lower())
            confidence = float(result.get("confidence", 0.7))
            
            logger.info(f"Intent detected: {pipeline.value} (confidence: {confidence:.2f})")
            logger.debug(f"Reasoning: {result.get('reasoning', 'No reasoning provided')}")
            
            return pipeline, confidence
        except Exception as e:
            logger.error(f"Error in intent detection: {str(e)}")
            # Default to RAG pipeline as fallback
            return IntentPipeline.RAG, 0.5
    
    async def process_query(self, request: ChatRequest, vector_store: PineconeVectorStore) -> ChatResponse:
        query = request.message
        logger.info(f"Processing query: '{query}'")
        
        # Detect intent to determine which pipeline to use
        pipeline, confidence = await self.detect_intent(query)
        
        if pipeline == IntentPipeline.FILTER:
            logger.info(f"Using FILTER pipeline for query (confidence: {confidence:.2f})")
            return await self._process_filter_pipeline(request)
        else:
            logger.info(f"Using RAG pipeline for query (confidence: {confidence:.2f})")
            return await self._process_rag_pipeline(request, vector_store)
    
    async def _process_filter_pipeline(self, request: ChatRequest) -> ChatResponse:
        query = request.message
        
        # Extract conversation context
        conversation_context = self._extract_conversation_context(request)
        
        # Prepare hotel data context
        hotel_data_context = json.dumps(self.hotel_data, indent=2)
        
        prompt = f"""
        Based on the following hotel data, conversation history, and user query, provide a helpful response.
        
        Hotel Data:
        {hotel_data_context}
        
        {conversation_context}
        
        User Query: {query}
        
        Please respond directly to the user's query using the hotel data provided.
        If the specific information isn't available in the data, clearly state that
        and provide the closest relevant information if possible.
        """
        
        try:
            logger.debug("Sending query to filtering pipeline LLM")
            response = await self.llm.ainvoke(prompt)
            response_text = response.content
            
            return ChatResponse(
                response=response_text,
                metadata={
                    "pipeline": "filter",
                    "confidence": 1.0,
                    "data_source": "hotel_json"
                }
            )
        except Exception as e:
            logger.error(f"Error in filter pipeline: {str(e)}")
            return ChatResponse(
                response="I'm sorry, I encountered an error while processing your request about hotel information. Please try again or rephrase your question.",
                metadata={"error": str(e)}
            )
    
    async def _process_rag_pipeline(self, request: ChatRequest, vector_store: PineconeVectorStore) -> ChatResponse:
        query = request.message
        
        try:
            # Retrieve relevant documents from vector store
            logger.info(f"Retrieving relevant documents for: '{query}'")
            docs = vector_store.similarity_search(query, k=10)
            context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
            logger.debug(f"Retrieved {len(docs)} relevant documents")
            
            # Extract conversation context
            conversation_context = self._extract_conversation_context(request)
            
            # Construct prompt with context and conversation history
            prompt = f"""
            Based on the following retrieved information and conversation history, answer the user's question.
            
            {conversation_context}
            
            Context from knowledge base:
            {context}
            
            User's question: {query}
            
            Please provide a helpful response based on the context information and previous conversation.
            If the answer cannot be found in the context, say so clearly but try to provide related information if possible.
            """
            
            # Get response from LLM
            logger.info("Generating response from LLM using RAG pipeline")
            response = await self.llm.ainvoke(prompt)
            response_text = response.content
            
            logger.debug(f"Generated RAG response of {len(response_text)} characters")
            return ChatResponse(
                response=response_text,
                metadata={
                    "pipeline": "rag",
                    "sources": len(docs),
                    "top_document_id": docs[0].metadata.get("id", "unknown") if docs else "none"
                }
            )
        except Exception as e:
            logger.error(f"RAG pipeline processing failed: {str(e)}", exc_info=True)
            return ChatResponse(
                response="I'm sorry, I encountered an error while retrieving and processing information for your query. Please try again or rephrase your question.",
                metadata={"error": str(e)}
            )
    
    def _extract_conversation_context(self, request: ChatRequest) -> str:
        conversation_context = ""
        
        if request.conversation_history and len(request.conversation_history) > 0:
            logger.debug(f"Processing conversation history with {len(request.conversation_history)} messages")
            
            # Extract recent conversation
            recent_messages = []
            for item in request.conversation_history[-5:]:  # Last 5 messages
                recent_messages.append(f"{item.role}: {item.content}")
            
            conversation_context = "Recent conversation:\n" + "\n".join(recent_messages) + "\n\n"
            
            # Add memory data if available
            if hasattr(request, 'memory_data') and request.memory_data:
                memory_data = request.memory_data
                
                if 'summary' in memory_data and memory_data['summary']:
                    conversation_context += f"Conversation summary:\n{memory_data['summary']}\n\n"
                
                if 'key_points' in memory_data and memory_data['key_points']:
                    conversation_context += f"Key points from conversation:\n{memory_data['key_points']}\n\n"
        
        return conversation_context
