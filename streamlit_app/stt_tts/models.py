import whisper
import torch
from TTS.api import TTS
import torchaudio
import tempfile
import os

torch.classes.__path__ = [] # to silence warning

class STTModel:
    def __init__(self, model_name = 'small', audio_backend = 'sox_io'):
        self.model = whisper.load_model(model_name)
        torchaudio.set_audio_backend(audio_backend)  # or "soundfile" or "ffmpeg"
    
    def transcribe(self, audio_file:BytesIO):
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(audio_file.read())
        # Get the absolute path of the temporary audio file
        audio_file_path = os.path.abspath(temp_audio.name)
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
        self.model = TTS(model_name).to(device)
        torchaudio.set_audio_backend(audio_backend)  # or "soundfile" or "ffmpeg"

    def tts_to_file(self, text:str):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        self.model.tts_to_file(text=text, file_path=temp_audio_path)
        return temp_audio_path

    