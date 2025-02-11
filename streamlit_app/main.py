import streamlit as st
from pathlib import Path
import json
import os
from dotenv import load_dotenv
from streamlit_app.graph import workflow
from streamlit_app.stt_tts.models import STTModel

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dictionary" not in st.session_state:
    st.session_state.dictionary = {}
if "stt" not in st.session_state:
    st.session_state.stt = STTModel()
if "tts" not in st.session_state:
    st.session_state.tts = TTSModel()

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
    workflow = create_workflow()
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Create columns for text and audio input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Text input
        prompt = st.chat_input("Type your message here...")
    
    with col2:
        # Audio input
        audio = st.audio_input("🎤")
    
    # Process text input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        workflow.invoke({"input": prompt})
        with st.chat_message("assistant"):
            response = f"Echo: {prompt}"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    # Process audio input
    elif audio:
        # Add user audio message to chat history
        st.session_state.messages.append({"role": "user", "content": "🎤 *Audio message*"})
        transcribed = False
        with st.chat_message("user"):
            st.markdown("🎤 *Audio message*")
            st.audio(audio)
            st.markdown("Transcribing audio...")
            try:
                transcription = st.session_state.stt.transcribe(audio)
                st.markdown(transcription)
                st.session_state.messages.append({"role": "user", "content": transcription})
                # Transcribe audio
                transcription = st.session_state.stt.transcribe(audio)
                transcribed = True
            except Exception as e:
                st.error(f"Error transcribing audio: {str(e)}")
                st.markdown("Failed to transcribe audio, try again")
        # TODO: Process audio through LangGraph workflow
            
        if  transcribed:            
            st.session_state.messages.append({"role": "user", "content": transcription})
            st.markdown(transcription)

            # TODO: Process audio through LangGraph workflow
            # For now, just acknowledge receipt
            with st.chat_message("assistant"):
                response = "I received your audio message. Audio processing will be implemented soon!"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    initialize_app()
    create_sidebar()
    
    # Main chat interface
    display_chat_interface()

if __name__ == "__main__":
    main()
