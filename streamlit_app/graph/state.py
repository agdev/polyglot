from typing import Literal, TypedDict, Annotated, Optional
from operator import add
from pydantic import BaseModel

class Word(TypedDict):
    translated_word: str
    original_word: str

class TranslationOptions(TypedDict):
    description: str
    translation: str
    audio_file_path: Optional[str]
    words: Annotated[list[Word], add]
    
class Translation(TypedDict):
    target_language: str
    source_language: str
    options: Annotated[list[TranslationOptions], add]   

class PolyglotState(TypedDict):
    input: str
    # input_type: Literal["text", "audio"]
    intent: Literal["chat", "translation"]
    # transcription: Optional[str]
    translation: Translation
    chat_resp: str
    chat_history: Annotated[list[str], add]
    # audio_response_files: Annotated[list[str], add]
    error: Optional[str]

# class PolyglotStateInternal(TypedDict):
