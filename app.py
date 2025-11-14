"""
Streamlit Web Application for RAG-based Question Answering System
Built with LangGraph and ChromaDB
"""

# Workaround for Python 3.13 compatibility with scikit-learn/joblib
import sys
if sys.version_info >= (3, 13):
    import threading
    if not hasattr(threading, '_register_atexit'):
        threading._register_atexit = lambda func: None

import streamlit as st
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

def extract_text_content(content):
    """Extract clean text from various content formats"""
    # Handle None
    if content is None:
        return ""
    
    # Handle list format: [{'type': 'text', 'text': '...', 'extras': {...}}]
    if isinstance(content, list):
        # Empty list
        if len(content) == 0:
            return ""
        # List of dicts with 'text' field
        if isinstance(content[0], dict):
            # Look for 'text' field first
            if 'text' in content[0]:
                return content[0]['text']
            # Fallback to 'content' field
            if 'content' in content[0]:
                return content[0]['content']
        # List of strings
        if isinstance(content[0], str):
            return ' '.join(content)
        # Unknown list format
        return str(content)
    
    # Handle dict format: {'type': 'text', 'text': '...', 'extras': {...}}
    if isinstance(content, dict):
        # Look for 'text' field first (Gemini format)
        if 'text' in content:
            return content['text']
        # Fallback to 'content' field
        if 'content' in content:
            return content['content']
        # Unknown dict format
        return str(content)
    
    # Already a string or other primitive
    return str(content)

# Cache the graph initialization to prevent reloading on every interaction
@st.cache_resource
def initialize_graph():
    """Initialize and cache the LangGraph workflow"""
    try:
        from src.graph.graph_builder import graph
        return graph
    except ImportError as e:
        st.error(f"Import error: {e}")
        st.error("Please make sure all dependencies are installed and the graph is properly built.")
        return None

# Initialize the graph once
graph = initialize_graph()

if graph is None:
    st.stop()

try:
    from langchain_core.messages import HumanMessage
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="RAG Question Answering System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🤖 RAG Question Answering System")
st.markdown("Ask questions about LangChain and LangGraph documentation!")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    st.markdown("**LLM**: Google Gemini 2.5 Flash")
    st.markdown("**Vector Store**: ChromaDB")
    st.markdown("**Embeddings**: TF-IDF (Offline)")
    st.markdown("**Framework**: LangGraph")
    
    # Add a button to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Sample Questions:**")
    st.markdown("- What is LangGraph?")
    st.markdown("- How does LangChain work?")
    st.markdown("- Explain vector stores")
    st.markdown("- What are document loaders?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Extract clean text if needed
        clean_content = extract_text_content(message["content"])
        st.markdown(clean_content)

# React to user input
if prompt := st.chat_input("Ask a question about LangChain or LangGraph..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                # Create the input for the graph
                input_messages = [HumanMessage(content=prompt)]
                
                # Run the graph
                result = graph.invoke({"messages": input_messages})
                
                # Extract the response with proper text extraction
                if result and "messages" in result and result["messages"]:
                    raw_content = result["messages"][-1].content
                    response = extract_text_content(raw_content)
                else:
                    response = "I'm sorry, I couldn't generate a response. Please try again."
                
                # Display the response
                st.markdown(response)
                
                # Add assistant response to chat history (store clean text)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Built with ❤️ using LangGraph, Google Gemini, ChromaDB, and Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)
