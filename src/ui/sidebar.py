import streamlit as st
from src.utils.memory import get_conversation_history, clear_chat_history

def render_sidebar():
    """Render the sidebar with app info and controls"""
    
    st.sidebar.header("About")
    st.sidebar.markdown("""
    ### RAG Web Crawler & Chatbot
    This application combines:
    - **Web Crawling**: Extract content from websites
    - **Generative AI**: Answer questions based on the indexed content
    - **Conversation Memory**: Remember chat history for context
    """)
    
    st.sidebar.divider()
    
    st.sidebar.markdown("### How to use")
    st.sidebar.markdown("""
    1. Crawl websites in the **Web Crawler** tab
    2. Chat with the content in the **RAG Chatbot** tab
    3. The chatbot will remember your conversation history!
    """)
    
    st.sidebar.divider()
    
    st.sidebar.subheader("Session Info")
    st.sidebar.write(f"Session ID: {st.session_state.session_id[:8]}...")
    
    if st.sidebar.button("Clear Chat History", key="sidebar_clear_chat"):
        clear_chat_history()
        st.rerun()
    
    with st.sidebar.expander("View Conversation Memory"):
        history = get_conversation_history()
        if history:
            for item in history:
                st.markdown(f"**{item['role'].title()}**: {item['content'][:50]}...")
        else:
            st.write("No conversation history yet.")