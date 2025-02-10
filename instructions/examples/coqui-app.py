import torch
import streamlit as st
from TTS.api import TTS
import tempfile
import os
import torchaudio

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"

torch.classes.__path__ = []

torchaudio.set_audio_backend("sox_io")  # or "soundfile" or "ffmpeg"

model_name = 'tts_models/en/jenny/jenny'
tts = TTS(model_name).to(device)

st.title('Coqui TTS')

text_to_speak = st.text_area('Entire article text here:', '')


if st.button('Listen'):
    if text_to_speak:

        # temp path needed for audio to listen to
        temp_audio_path = './temp_audio.wav'

        tts.tts_to_file(text=text_to_speak, file_path=temp_audio_path)


        st.audio(temp_audio_path, format='audio/wav')


        os.unlink(temp_audio_path)
