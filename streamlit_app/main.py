import streamlit as st
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dictionary" not in st.session_state:
    st.session_state.dictionary = {}

def initialize_app():
    st.set_page_config(
        page_title="Polyglot - AI Language Learning Assistant",
        page_icon="🗣️",
        layout="wide"
    )
    st.title("🗣️ Polyglot - AI Language Learning Assistant")

def create_sidebar():
    with st.sidebar:
        st.title("Learning Tools")
        
        if st.button("📚 Dictionary"):
            # TODO: Implement dictionary view
            st.session_state.current_view = "dictionary"
            
        if st.button("📝 Phrases"):
            # TODO: Implement phrases view
            st.session_state.current_view = "phrases"
            
        st.markdown("---")
        if st.button("⬇️ Download Progress"):
            # TODO: Implement download functionality
            st.text_input("Enter your email:", key="download_email")

def display_chat_interface():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # TODO: Process user input through LangGraph workflow
        # For now, just echo the input
        with st.chat_message("assistant"):
            response = f"Echo: {prompt}"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    initialize_app()
    create_sidebar()
    
    # Main chat interface
    display_chat_interface()
    
    # Audio input placeholder
    with st.expander("🎤 Voice Input"):
        st.write("Audio recording functionality coming soon...")
        # TODO: Implement audio recording

if __name__ == "__main__":
    main()
