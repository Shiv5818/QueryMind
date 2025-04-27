import streamlit as st
from src.api.client import RagAPIClient
from src.utils.memory import get_conversation_history, add_message_to_memory, clear_chat_history

def render_chatbot_tab():
    """Render the RAG chatbot tab"""
    
    st.header("RAG Chatbot with Memory")
    st.markdown("Chat with your indexed content using the power of RAG and conversation memory.")
    
    # Initialize API client
    api_client = RagAPIClient()
    
    # Clear chat button
    if st.button("Clear Chat History", key="chat_clear"):
        clear_chat_history()
        st.rerun()
    
    # Display chat messages using Streamlit's built-in chat components
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input using Streamlit's built-in chat input
    if prompt := st.chat_input("Ask something about the indexed content..."):
        # Add user message to the UI and memory
        add_message_to_memory("user", prompt)
        st.chat_message("user").markdown(prompt)
        
        # Process with the assistant
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Get conversation history from memory
            conversation_history = get_conversation_history()
            
            # Send request to RAG backend
            result = api_client.chat(prompt, conversation_history)
            
            if "error" not in result:
                response = result.get("response", "")
                message_placeholder.markdown(response)
                add_message_to_memory("assistant", response)
            else:
                error_message = f"Sorry, I encountered an error: {result.get('error')}"
                message_placeholder.markdown(error_message)
                add_message_to_memory("assistant", error_message)