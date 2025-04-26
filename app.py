import streamlit as st
import requests
import json
from typing import List, Dict, Any
import time
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
import uuid

# Configure the app
st.set_page_config(
    page_title="RAG System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply dark theme styling
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput, .stTextArea {
        background-color: #262730;
        color: #FAFAFA;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #4F8BF9;
        color: white;
        border-radius: 5px;
    }
    .stProgress .st-bo {
        background-color: #4F8BF9;
    }
    div[data-testid="stMarkdownContainer"] {
        color: #FAFAFA;
    }
    div[role="tab"] {
        background-color: #262730;
        color: #FAFAFA;
    }
    div[role="tab"][aria-selected="true"] {
        background-color: #4F8BF9;
        color: white;
    }
    .stAlert {
        background-color: #262730;
        color: #FAFAFA;
    }
    /* Fix chat input box to bottom */
    form[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        left: 10%;
        width: 80%;
        z-index: 999;
    }
    /* Add padding to chat container so messages aren't hidden behind input */
    div[data-testid="stVerticalBlock"] {
        padding-bottom: 100px;
    }
</style>
""", unsafe_allow_html=True)

# Constants
API_BASE_URL = "http://localhost:8000"  # Update this if your API is hosted elsewhere

# Initialize session ID for memory management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Helper Functions

def crawl_url(url: str) -> Dict[str, Any]:
    """Crawl and index a URL through the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/crawl",
            json={"url": url},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error during crawling: {e}")
        return {"error": str(e)}

# Remove query_index and related routes from frontend

def chat_with_rag(message: str) -> Dict[str, Any]:
    """Chat with the RAG system, incorporating conversation memory"""
    try:
        # Get conversation history
        conversation_history = get_conversation_history()

        # Make the API call
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()

        # Update memory
        st.session_state.memory.chat_memory.add_user_message(message)
        st.session_state.memory.chat_memory.add_ai_message(result.get("response", ""))

        return result
    except requests.exceptions.RequestException as e:
        st.error(f"Error during chat: {e}")
        return {"error": str(e)}


def get_conversation_history() -> List[Dict[str, str]]:
    """Extract conversation history from memory"""
    messages = st.session_state.memory.chat_memory.messages
    history = []
    for message in messages:
        if isinstance(message, HumanMessage):
            history.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            history.append({"role": "assistant", "content": message.content})
    return history


def clear_chat_history():
    """Clear the chat history and memory"""
    st.session_state.memory.clear()
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())

# App Header
st.title("🔍 RAG Web Crawler & Chatbot")
st.markdown("A Retrieval-Augmented Generation system that can crawl websites and answer questions.")

# Create tabs for different functionality
tab1, tab2 = st.tabs(["Web Crawler", "RAG Chatbot"])

# Tab 1: Web Crawler
with tab1:
    st.header("Web Crawler")
    st.markdown("Enter a URL to crawl and index its content for later retrieval.")

    # Use a form to stabilize input position
    with st.form("crawl_form", clear_on_submit=False):
        col1, col2 = st.columns([4, 1])
        url = col1.text_input("URL to Crawl", placeholder="https://example.com", key="crawl_url")
        submit = col2.form_submit_button("Crawl")

        if submit:
            if url:
                with st.spinner("Crawling and indexing the website..."):
                    result = crawl_url(url)
                    if "error" not in result:
                        st.success(f"Successfully crawled and indexed: {result.get('url', url)}")
                        st.info(f"Chunks created: {result.get('chunk_count', 0)}, Documents indexed: {result.get('indexed_count', 0)}")
                    else:
                        st.error("Failed to crawl the URL")
            else:
                st.warning("Please enter a URL to crawl")

# Tab 2: RAG Chatbot
with tab2:
    st.header("RAG Chatbot with Memory")
    st.markdown("Chat with your indexed content using the power of RAG, Gemini, and conversation memory.")

    # Clear chat button
    if st.button("Clear Chat History", key="clear_chat"):
        clear_chat_history()
        st.experimental_rerun()

    # Initialize chat display list
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask something about the indexed content..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Thinking...")
            result = chat_with_rag(prompt)
            if "error" not in result:
                response = result.get("response", "")
                placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                placeholder.markdown("Sorry, I encountered an error while processing your request.")

# Sidebar with app info
with st.sidebar:
    st.header("About")
    st.markdown("""
    ### RAG Web Crawler & Chatbot
    This application combines:
    - **Web Crawling**: Extract content from websites
    - **Generative AI**: Answer questions based on the indexed content
    - **Conversation Memory**: Remember chat history for context
    """)
    st.divider()
    st.markdown("### How to use")
    st.markdown("""
    1. Crawl websites in the **Web Crawler** tab
    2. Chat with the content in the **RAG Chatbot** tab
    3. The chatbot will remember your conversation history!
    """)
    st.divider()
    st.subheader("Session Info")
    st.write(f"Session ID: {st.session_state.session_id[:8]}...")
    with st.expander("View Conversation Memory"):
        history = get_conversation_history()
        if history:
            for item in history:
                st.markdown(f"**{item['role'].title()}**: {item['content'][:50]}...")
        else:
            st.write("No conversation history yet.")
    st.divider()
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            st.success("✅ Connected to API")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ Cannot connect to API")

# To run: streamlit run app_fixed.py
