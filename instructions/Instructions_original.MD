# Project overview
You are developing plolyglot which is chat assitant that helps users to learn a foreighn language.
You will be using Langgraph, Langchain and Streamlit, Whisper and Coqui open source models


# Core functionalities
1. user can records or enter text via keyboard to chat
2. Whisper transcribes audio
3. LLM checks for intention, is it a normal chat or translation request
4
    4.a Translation
        1. LLM translates
        2. coqui model converts to audio 
        3. breaks down sentence into words for later study/review
        4. saves phrases and words into dictionary
   
   4.b Regular chat

# Directory Structure
streamlit_app
    graph
    state

# Documentation
How to build chat with Streamlit: 
https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps
https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/llm-quickstart
https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/chat-response-feedback
https://blog.streamlit.io/langchain-tutorial-1-build-an-llm-powered-app-in-18-lines-of-code/

Example of streamlit audio recorder: ./examples/audio-recorder.py

How to work with Whisper: https://github.com/openai/whisper

Example how to work with Whisper: ./examples/whisper-app.py

How to work with Coqui : https://docs.coqui.ai/en/latest/

Example how to work with Coqui: ./examples/coqui-app.py



