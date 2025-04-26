import os
import asyncio
from crawl4ai import AsyncWebCrawler
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from pinecone import Pinecone
from typing import List, Dict, Optional

# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCj-NvG7lmY6bTyOMmc2fnFZMuzvWZ2rEA")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "pcsk_4s6WqH_TkYHaaqZkA3cRxww3iAcGsqcop3VT7E9AJWT6NVwNzJa4SysZFRwi59ZebBQjfy")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC4OGwYFG5EqF_aa9mOftE_KAhkh2wxPSE")

# Validate required variables
for key, value in [("GOOGLE_API_KEY", GOOGLE_API_KEY), ("PINECONE_API_KEY", PINECONE_API_KEY), ("PINECONE_INDEX_NAME", PINECONE_INDEX_NAME), ("GEMINI_API_KEY", GEMINI_API_KEY)]:
    if not value:
        raise ValueError(f"{key} must be set")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY, environment="us-west1-gcp")

# Initialize FastAPI app
app = FastAPI(title="RAG API", description="RAG system with web crawling capabilities and conversation memory")

# Text splitter setup
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200, separators=["\n\n", "\n", " "])

# Cached embeddings setup
def get_embeddings():
    model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", api_key=GOOGLE_API_KEY)
    store = LocalFileStore("./cache/")
    return CacheBackedEmbeddings.from_bytes_store(model, store, namespace=model.model)

embed_model = get_embeddings()

# Initialize Gemini language model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Define Pydantic models for request/response
class CrawlRequest(BaseModel):
    url: str

class CrawlResponse(BaseModel):
    url: str
    chunk_count: int
    indexed_count: int

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    results: List[str]

class ConversationItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ConversationItem]] = None

class ChatResponse(BaseModel):
    response: str

# Dependency for vector store
def get_vector_store():
    return PineconeVectorStore.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embed_model)

# Crawl endpoint
@app.post("/crawl", response_model=CrawlResponse)
async def crawl_endpoint(request: CrawlRequest):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=request.url)
        markdown_text = result.markdown
    
    docs = text_splitter.create_documents([markdown_text])
    texts = [doc.page_content for doc in docs]
    PineconeVectorStore.from_texts(texts, embedding=embed_model, index_name=PINECONE_INDEX_NAME)
    
    return {"url": request.url, "chunk_count": len(texts), "indexed_count": len(texts)}

# Query endpoint
@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest, vector_store: PineconeVectorStore = Depends(get_vector_store)):
    results = vector_store.similarity_search(request.query, k=20)
    hits = [doc.page_content for doc in results]
    return {"query": request.query, "results": hits}

# Chatbot endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, vector_store: PineconeVectorStore = Depends(get_vector_store)):
    # Retrieve relevant documents from vector store
    docs = vector_store.similarity_search(request.message, k=20)
    context = "\n".join([doc.page_content for doc in docs])
    
    # Build conversation history string if available
    conversation_context = ""
    if request.conversation_history and len(request.conversation_history) > 0:
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
    response = await llm.ainvoke(prompt)
    response_text = response.content
    
    return {"response": response_text}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the RAG API with web crawling capabilities and conversation memory"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)