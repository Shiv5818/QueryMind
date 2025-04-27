import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styling to the Streamlit app"""
    
    st.markdown("""
    <style>
    /* General app styling */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 1) Scrollable message area with room for fixed input */
    div[data-testid="stVerticalBlock"] {
        height: 100vh;           /* fill viewport */
        overflow-y: auto;        /* enable vertical scrolling */
        box-sizing: border-box;  /* include padding in height */
        padding-bottom: 80px;    /* reserve space for the fixed input */
    }

    /* 2) Fixed-position input bar */
    div[data-testid="stChatInput"] {
        position: fixed;           /* pin to viewport edge */
        bottom: 0;                 /* align at bottom */
        left: 0;                   /* stretch full width */
        right: 0;
        z-index: 999;              /* above all messages */
        background-color: #0E1117;
        padding: 12px 20px;
        border-top: 1px solid #262730;
    }

    /* 3) Sidebar-aware offset when expanded */
    [data-testid="stSidebar"][aria-expanded="true"] ~ div 
      div[data-testid="stChatInput"] {
        left: 21rem;  /* shift right by sidebar width */
    }
    [data-testid="stSidebar"][aria-expanded="false"] ~ div 
      div[data-testid="stChatInput"] {
        left: 0;      /* full-width when sidebar hidden */
    }

    /* Style the chat input text field */
    div[data-testid="stChatInput"] input {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #434654;
        border-radius: 8px;
        padding: 10px;
        width: 100%;
    }

    /* Chat message container styling */
    .stChatMessage {
        margin: 10px 20px;
    }

    /* User and assistant message content */
    .stChatMessageContent {
        background-color: #262730;
        color: #FAFAFA;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 16px;
        line-height: 1.5;
    }

    /* User message specific styling */
    .stChatMessage[data-testid="stChatMessageUser"] 
      .stChatMessageContent {
        background-color: #4F8BF9;
        color: #FFFFFF;
    }

    /* Assistant message specific styling */
    .stChatMessage[data-testid="stChatMessageAssistant"] 
      .stChatMessageContent {
        background-color: #262730;
    }

    /* Button styling */
    .stButton > button {
        background-color: #4F8BF9;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #3B7DE9;
    }

    /* Text input and textarea styling */
    .stTextInput input, .stTextArea textarea {
        background-color: #262730;
        color: #FAFAFA;
        border: 1px solid #434654;
        border-radius: 8px;
        padding: 10px;
    }

    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: #4F8BF9;
    }

    /* Markdown container text color */
    div[data-testid="stMarkdownContainer"] {
        color: #FAFAFA;
    }

    /* Tab styling */
    div[role="tab"] {
        background-color: #262730;
        color: #FAFAFA;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }
    div[role="tab"][aria-selected="true"] {
        background-color: #4F8BF9;
        color: #FFFFFF;
    }

    /* Alert styling */
    .stAlert {
        background-color: #262730;
        color: #FAFAFA;
        border-radius: 8px;
        padding: 10px;
    }

    /* Spinner styling */
    .stSpinner > div > div {
        border-color: #4F8BF9 transparent transparent transparent;
    }

    /* Ensure headers are styled consistently */
    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA;
        font-weight: 600;
    }

    /* Improve form styling */
    form {
        background-color: #0E1117;
        padding: 0;
        border: none;
        box-shadow: none;
    }
    div[data-testid="stForm"] {
        background-color: #0E1117;
        border: none;
        box-shadow: none;
    }
    .stForm div[data-testid="stHorizontalBlock"] {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
