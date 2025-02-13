from typing import TypedDict, Any
from stt_tts.models import TTSModel, STTModel

class ConfigSchema(TypedDict):
    tts_model: TTSModel
    stt_model: STTModel
    llm_config: dict[str, Any]
    
    