from typing import TypedDict
from pathlib import Path
import os
from dotenv import load_dotenv

class Config(TypedDict):
    WHISPER_MODEL: str
    TTS_MODEL: str
    GOOGLE_API_KEY: str
    AUDIO_BACKEND: str
    DEVICE: str


def load_config() -> Config:        
    env_path = os.path.join( os.getcwd(), "env", ".env")
    env_found = False
    # Try the original path first
    if os.path.exists(env_path):
       env_found = True
    else:
        # Try alternative path if original doesn't exist
        env_path = os.path.join(os.getcwd(), 'streamlit_app', 'env', '.env')
        env_found = os.path.exists(env_path)
        
    # Load the .env file if it exists, otherwise show error
    if env_found == True:
        print(f"env_path: {env_path}")
        load_dotenv(env_path)
    else:
        print(f"Error: Environment file not found at: {env_path}")
        
    return {
        "WHISPER_MODEL": os.getenv("WHISPER_MODEL","small"),
        "TTS_MODEL": os.getenv("TTS_MODEL","tts_models/en/jenny/jenny"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
        "MISTRAL_API_KEY": os.getenv("MISTRAL_API_KEY", ""),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
        "AUDIO_BACKEND": os.getenv("AUDIO_BACKEND","sox_io"),
        "DEVICE": "cpu"
    } 