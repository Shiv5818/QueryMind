# RAG Web Crawler & Chatbot

A powerful Retrieval-Augmented Generation (RAG) system that combines web crawling capabilities with an intelligent chatbot, featuring conversation memory and advanced content processing.

## 🌟 Features

### Web Crawling
- Advanced web content extraction
- Intelligent text preprocessing using Gemini Pro
- Automatic content chunking and indexing
- Support for multiple webpage formats

### RAG Chatbot
- Powered by Google's Gemini 1.5 Pro
- Conversation memory for contextual responses
- Vector-based semantic search using Pinecone
- Intelligent document retrieval and ranking

### Technical Features
- FastAPI backend for high-performance API endpoints
- Streamlit frontend for intuitive user interface
- Pinecone vector database for efficient similarity search
- Advanced text processing and chunking capabilities
- Comprehensive error handling and logging
- Environment-based configuration

## 🏗️ Architecture

### Backend (FastAPI)
- **API Layer**: RESTful endpoints for crawling, querying, and chat
- **Core Services**: 
  - Crawl Service: Web content extraction and processing
  - Query Service: Vector search and document retrieval
  - Chat Service: LLM integration and response generation
- **Vector Store**: Pinecone integration for document storage and retrieval
- **LLM Integration**: Google Gemini 1.5 Pro for text generation

### Frontend (Streamlit)
- **Web Crawler Tab**: Interface for URL submission and crawling
- **RAG Chatbot Tab**: Chat interface with conversation history
- **Sidebar**: Application information and session details
- **Custom Styling**: Modern, responsive dark theme UI

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- API Keys:
  - Google API (Gemini)
  - Pinecone API
  - (Optional) Additional crawler API keys

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd rag-web-crawler-chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_gemini_api_key
PINECONE_INDEX_NAME=rag
PINECONE_ENVIRONMENT=us-west1-gcp
DEBUG=False
PORT=8000
```

### Running the Application

1. Start the FastAPI backend:
```bash
python main.py
```

2. Start the Streamlit frontend:
```bash
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Google API key for Gemini
- `PINECONE_API_KEY`: Pinecone API key
- `GEMINI_API_KEY`: Gemini API key
- `PINECONE_INDEX_NAME`: Name of Pinecone index
- `PINECONE_ENVIRONMENT`: Pinecone environment
- `EMBEDDING_MODEL`: Model for text embeddings
- `LLM_MODEL`: Language model selection
- `CHUNK_SIZE`: Text chunk size
- `CHUNK_OVERLAP`: Overlap between chunks
- `SIMILARITY_TOP_K`: Number of similar documents to retrieve
- `PORT`: API server port
- `DEBUG`: Debug mode toggle

### Application Settings
- `APP_TITLE`: Application title
- `APP_DESCRIPTION`: Application description
- `APP_VERSION`: Application version
- `HOST`: API host address
- `CACHE_DIR`: Directory for cached files
- `LOG_LEVEL`: Logging level

## 📚 API Endpoints

### /api/crawl
- **Method**: POST
- **Purpose**: Crawl and index web content
- **Response**: Crawl statistics and status

### /api/query
- **Method**: POST
- **Purpose**: Search indexed content
- **Response**: Relevant document chunks

### /api/chat
- **Method**: POST
- **Purpose**: Chat with RAG system
- **Response**: AI-generated responses

## 🎨 UI Components

### Web Crawler Tab
- URL input field
- Crawl status indicators
- Success/error messages
- Crawl statistics display

### RAG Chatbot Tab
- Chat interface with message history
- Clear chat functionality
- Real-time response indicators
- Error handling displays

### Sidebar
- Application information
- Usage instructions
- Session information
- System status

## 🛠️ Development

### Project Structure
```
├── api/
│   ├── routes.py
│   ├── schemas.py
│   └── dependencies.py
├── core/
│   ├── crawler.py
│   ├── embeddings.py
│   ├── llm.py
│   └── text_processing.py
├── services/
│   ├── crawl_service.py
│   ├── query_service.py
│   └── chat_service.py
├── src/
│   ├── ui/
│   └── utils/
├── config/
│   └── settings.py
├── main.py
└── app.py
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Acknowledgments

- Google Gemini for LLM capabilities
- Pinecone for vector storage
- FastAPI for backend framework
- Streamlit for frontend framework

## 📧 Contact

For questions and support, please open an issue in the repository.