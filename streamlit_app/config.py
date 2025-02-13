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
    print(f"env_path: {env_path}")
    load_dotenv(env_path)
    
    return {
        "WHISPER_MODEL": os.getenv("WHISPER_MODEL","small"),
        "TTS_MODEL": os.getenv("TTS_MODEL","tts_models/en/jenny/jenny"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", ""),
        "AUDIO_BACKEND": os.getenv("AUDIO_BACKEND","sox_io"),
        "DEVICE": "cpu"
    } 