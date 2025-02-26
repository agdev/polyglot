# Polyglot - AI Language Learning Assistant

An AI-powered language learning assistant that helps users learn foreign languages through interactive chat. The application supports both text and voice interactions, leveraging state-of-the-art AI models for transcription, translation, and speech synthesis.

## Features

- Voice and text input support
- Real-time translation
- Interactive chat with AI language tutor
- Personal dictionary and phrase storage
- Text-to-speech for pronunciation practice

## Tech Stack

- Frontend: Streamlit
- Backend: LangGraph, LangChain
- Speech Processing: Whisper (STT), Coqui (TTS)
- LLM: Google Gemini via LangChain

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with the following:
```
GROQ_API_KEY = your_groq_api_key

```
if not .env file is provided user will be prompted to enter their API key.

3. Run the application:
```bash
streamlit run streamlit_app/main.py
```

4. for Hugging Face
---
title: Polyglot
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: streamlit_app/main.py
---


## Contributing

Feel free to submit issues and enhancement requests!
