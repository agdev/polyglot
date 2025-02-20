from io import BytesIO
import whisper
import torch
from TTS.api import TTS
import torchaudio
import tempfile
import os
from typing import Optional, Dict, Any

torch.classes.__path__ = [] # to silence warning

class STTModel:
    def __init__(self,  model_name: str = 'small', device = 'cpu') -> None:
        self.model = whisper.load_model(model_name, device=device)
    
    def transcribe(self, audio: bytes) -> Optional[Dict[str, Any]]:
        """
        Transcribe audio file to text using Whisper model.
        
        Args:
            audio_file: BytesIO object containing audio data
            
        Returns:
            Dict containing transcription result or None if error occurs
        """
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(audio)
        # Get the absolute path of the temporary audio file
        audio_file_path = os.path.abspath(temp_audio.name)
        print(f"Transcribing audio from: {audio_file_path}")
        try:
            transcription = self.model.transcribe(audio_file_path)    
            return transcription
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
        finally:
            os.remove(temp_audio.name)

class TTSModel:
    def __init__(self, model_name = 'tts_models/en/jenny/jenny', device = 'cpu', audio_backend = 'sox_io'):
        # print(f"Initializing TTS model with model_name: {model_name}, device: {device}, audio_backend: {audio_backend}")
        self.model = TTS(model_name).to(device)
        self.audio_backend = audio_backend

    def tts_to_file(self, text:str):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        self.model.tts_to_file(text=text, file_path=temp_audio_path,audio_backend=self.audio_backend)
        return temp_audio_path

    