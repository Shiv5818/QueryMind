import uuid
import streamlit as st
from typing import List, Dict
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage


def initialize_session_memory():
    """Initialize session memory if not already present"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(return_messages=True)
        
    if "messages" not in st.session_state:
        st.session_state.messages = []


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


def add_message_to_memory(role: str, content: str):
    """Add a message to the conversation memory"""
    if role == "user":
        st.session_state.memory.chat_memory.add_user_message(content)
    elif role == "assistant":
        st.session_state.memory.chat_memory.add_ai_message(content)
    
    # Also add to streamlit chat display messages
    if role in ["user", "assistant"]:
        st.session_state.messages.append({"role": role, "content": content})


def clear_chat_history():
    """Clear the chat history and memory"""
    st.session_state.memory.clear()
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())