import streamlit as st
# from pathlib import Path
# import json
# import os
# from dotenv import load_dotenv
# from streamlit_app.graph import workflow
from stt_tts.models import STTModel, TTSModel
# from graph.workflow import create_workflow
from config import load_config
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_mistralai.chat_models import ChatMistralAI
from langchain_groq import ChatGroq
from config import Config
# from streamlit_chat_widget import chat_input_widget
# from streamlit_extras.bottom_container import bottom

def has_api_key(config: Config) -> bool:
    """
    Check if GROQ API key is present and valid.
    Returns True if key is valid, False otherwise.
    """
    return not ("GROQ_API_KEY" not in config or not config["GROQ_API_KEY"])

# Load environment variables
# load_dotenv()
config = load_config()

# print(f"config: {config}")
def print_available_tts_models():
    from TTS.api import TTS

    available_models = TTS.list_models(language="en")
    print(available_models)
# Initialize session state
def init_llm():
    if "llm" not in st.session_state:
    # Initialize LLM  
        st.session_state.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=config["GROQ_API_KEY"]
        )
        # st.session_state.llm = ChatMistralAI(
        #     model="mistral-large-latest",
        #     api_key=config["MISTRAL_API_KEY"]
        # )
        # st.session_state.llm = ChatGoogleGenerativeAI(
        #     model="gemini-2.0-flash",
        #     temperature=0.7,
        #     api_key=config["GOOGLE_API_KEY"]
        # )    

def initialize_app():
    # Must be the first Streamlit command
    st.set_page_config(
        page_title="Polyglot - AI Language Learning Assistant",
        page_icon="🗣️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "dictionary" not in st.session_state:
        st.session_state.dictionary = {}
    if "stt" not in st.session_state:
        st.session_state.stt = STTModel(config["WHISPER_MODEL"])
    if "tts" not in st.session_state:
        # print_available_tts_models()
        st.session_state.tts = TTSModel(config["TTS_MODEL"],  audio_backend=config["AUDIO_BACKEND"])    

    st.title("🗣️ Polyglot - AI Language Learning Assistant")

    if "llm" not in st.session_state:
        if has_api_key(config) == False:
            st.sidebar.header("API Configuration")
            st.sidebar.markdown("""### API keys are stored only in session state of this Streamlit app. \n You can see the code of this app 
                                [here](https://github.com/agdev/polyglot/tree/main).  
                                You can obtain free API keys from [Groq](https://groq.com/api-key).
                                """)
            llm_api_key = st.sidebar.text_input(
                "API Key}",
                type="password",
                key="llm_api_key"
            )

            if st.sidebar.button("Save API Key"):
                if llm_api_key :
                    config["GROQ_API_KEY"] = llm_api_key            
                    st.session_state.config = config
                    st.sidebar.success("API keys saved successfully!")                
                    init_llm()
                else:
                    st.sidebar.error("Please enter GROQ API key")    
        else:
            init_llm()                    
    
def main():
    initialize_app()
    words_page = st.Page(page="words_page.py", title="Words", icon="📖")
    translations_page = st.Page(page="translation_page.py", title="Translations", icon="🗣️")
    chat_page = st.Page(page="chat_page.py", title="Chat", icon="💬")

    pg = st.navigation([chat_page, translations_page, words_page])
    pg.run()

if __name__ == "__main__":
    main()
