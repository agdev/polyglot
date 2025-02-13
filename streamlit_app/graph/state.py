from typing import Literal, TypedDict, Annotated, Optional
from operator import add

class TranslationOptions(TypedDict):
    description: str
    translation: str

class Translation(TypedDict):
    language: str
    options: Annotated[list[TranslationOptions], add]

class PolyglotState(TypedDict):
    input: str
    # input_type: Literal["text", "audio"]
    intent: Literal["chat", "translation"]
    # transcription: Optional[str]
    translation: Translation
    chat_resp: str
    chat_history: Annotated[list[str], add]
    audio_response_file: Annotated[list[str], add]

# class PolyglotStateInternal(TypedDict):
