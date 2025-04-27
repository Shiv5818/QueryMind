import streamlit as st

# Import configuration
from src.config import APP_TITLE, APP_ICON, APP_LAYOUT, SIDEBAR_STATE

# Import utility functions
from src.utils.memory import initialize_session_memory

# Import UI components
from src.ui.styles import apply_custom_styles
from src.ui.sidebar import render_sidebar
from src.ui.crawler import render_crawler_tab
from src.ui.chatbot import render_chatbot_tab

def main():
    """Main entry point for the Streamlit app"""
    
    # Configure the app settings
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=APP_LAYOUT,
        initial_sidebar_state=SIDEBAR_STATE,
    )
    
    # Apply custom styling
    apply_custom_styles()
    
    # Initialize session memory
    initialize_session_memory()
    
    # App title and description
    st.title(APP_TITLE)
    st.markdown("A Retrieval-Augmented Generation system that can crawl websites and answer questions.")
    
    # Create tabs for different functionality
    tab1, tab2 = st.tabs(["Web Crawler", "RAG Chatbot"])
    
    # Render the crawler tab
    with tab1:
        render_crawler_tab()
    
    # Render the chatbot tab
    with tab2:
        render_chatbot_tab()
    
    # Render the sidebar
    render_sidebar()

if __name__ == "__main__":
    main()