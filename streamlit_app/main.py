import streamlit as st
from pathlib import Path
import json
import os
from dotenv import load_dotenv
# from streamlit_app.graph import workflow
from stt_tts.models import STTModel, TTSModel
from graph.workflow import create_workflow
from config import load_config
from langchain_google_genai import ChatGoogleGenerativeAI
# Load environment variables
# load_dotenv()
config = load_config()
# print(f"config: {config}")
def print_available_tts_models():
    from TTS.api import TTS

    available_models = TTS.list_models(language="en")
    print(available_models)
# Initialize session state

if "messages" not in st.session_state:
    st.session_state.messages = []
if "dictionary" not in st.session_state:
    st.session_state.dictionary = {}
if "stt" not in st.session_state:
    st.session_state.stt = STTModel(config["WHISPER_MODEL"])
if "tts" not in st.session_state:
    # print_available_tts_models()
    st.session_state.tts = TTSModel(config["TTS_MODEL"],  audio_backend=config["AUDIO_BACKEND"])
    

if "llm" not in st.session_state:
# Initialize LLM
    st.session_state.llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
    )    

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

def display_translation_options(translation_options, audio_files):
    for idx, option in enumerate(translation_options):
        translation_text = option['translation']
        context_text = option['description'] 
        translation_number = idx + 1
        translation_message = f"**Translation {translation_number}:** {translation_text}\n*Context:* {context_text}"
        st.session_state.messages.append({"role": "assistant", "content": translation_message})
        st.markdown(f"**Translation {translation_number}:** {translation_text}")
        st.markdown(f"*Context:* {context_text}")
        if audio_files and idx < len(audio_files):
            st.audio(audio_files[idx])
        else:
            st.markdown("An error occurred while processing your message. Please try again.")

def process_chat_message(input_text: str, is_audio: bool = False) -> None:
    """
    Process a chat message and update the chat interface with the response.
    
    Args:
        input_text: The text to process (either direct input or transcribed audio)
        is_audio: Boolean indicating if the input was from audio
    """
    # Add user message to chat history
    display_text = f"🎤 *Audio message*:\n{input_text}" if is_audio else input_text
    st.session_state.messages.append({"role": "user", "content": display_text})
    
    with st.chat_message("user"):
        st.markdown(display_text)
        if is_audio:
            st.markdown(input_text)  # Show transcription below audio message
    
    # Process through workflow
    workflow = create_workflow(llm=st.session_state.llm,tts_model=st.session_state.tts)    
    app_workflow = workflow.compile()
    result = app_workflow.invoke({"input": input_text})
    
    # Display assistant response
    with st.chat_message("assistant"):
        if (result["chat_resp"] is not None):
            st.markdown(result["chat_resp"])
            st.session_state.messages.append({"role": "assistant", "content": result["chat_resp"]})
        elif (result["translation"] is not None):
            # Display each translation option with its audio
            display_translation_options(result["translation"]["options"], result.get("audio_response_files", []))



def display_chat_interface():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Create columns for text and audio input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        prompt = st.chat_input("Type your message here...")
    
    with col2:
        audio = st.audio_input("🎤")
    
    # Process text input
    if prompt:
        process_chat_message(prompt)
    elif audio: # Process audio input
        chat_message_user= st.chat_message("user")
        chat_message_user.markdown("🎤 *Audio message*")
        chat_message_user.audio(audio)
        chat_message_user.markdown("Transcribing audio...")
        try:
            transcription = st.session_state.stt.transcribe(audio)
            print(f"transcription: {transcription}")
            if transcription and transcription["text"] and len(transcription["text"]) > 0:                    
                process_chat_message(transcription["text"], is_audio=True)
            else:
                chat_message_user.markdown("Transcribing resulted in an empty text, try again")
        except Exception as e:
            chat_message_user.error(f"Error transcribing audio: {str(e)}")
            chat_message_user.markdown("Failed to transcribe audio, try again")

def main():
    initialize_app()
    create_sidebar()
    
    # Main chat interface
    display_chat_interface()

if __name__ == "__main__":
    main()
