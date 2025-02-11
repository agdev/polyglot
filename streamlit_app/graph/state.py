from ast import List
from typing import Dict, TypedDict, Annotated

class TranslationOptions(TypedDict):
    description: str
    translation: str

class Translation(TypedDict):
    language: str
    options: List[TranslationOptions]
# Define state schema
class PolyglotState(TypedDict):
    input: str
    # input_type: str  # "text" or "audio"
    intent: str  # "chat" or "translation"
    # transcription: str
    translation: Translation
    response: str
    audio_response_file: str

# class PolyglotStateInternal(TypedDict):
