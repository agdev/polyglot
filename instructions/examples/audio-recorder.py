import streamlit as st
from audiorecorder import audiorecorder

st.title("Audio Recorder")

audio = st.audio_input("Record")
if audio:
    # To play audio in frontend:
    st.audio(audio)  

# audio = audiorecorder("Click to record", "Click to stop recording","Click to pause recording", show_visualizer=True,)
# if len(audio) > 0:
#     # To play audio in frontend:
#     st.audio(audio.export().read())  

#     # To save audio to a file, use pydub export method:
#     audio.export("audio.wav", format="wav")

#     # To get audio properties, use pydub AudioSegment properties:
#     st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")