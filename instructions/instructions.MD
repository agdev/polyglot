# Product Requirements Document (PRD)

## Project Overview

**Polyglot** is an AI-powered language learning assistant designed to help users learn a foreign language through interactive chat. The application will support both text and voice interactions, leveraging **LangGraph, LangChain, Streamlit, Whisper, Coqui, and LangChain's ChatGoogleGenerativeAI** open-source models for transcription, translation, speech synthesis, and LLM processing.

---

## Core Functionalities

### 1. User Interaction Modes

- **Voice Input:** Users can record audio messages.
- **Text Input:** Users can enter text via keyboard.
- **Chat Responses:** The system provides translated responses, pronunciation, and conversational interaction.

### 2. Audio Processing

- **Transcription (Whisper):** Converts user-recorded voice messages into text.
- **Translation Detection:** Determines if the user’s intent is a general chat or a translation request.
- **Language Identification:** Detects the language of the input text/audio to categorize dictionary entries per language.

### 3. Response Handling

#### 3.a Translation Mode

- **Translation (LLM via LangChain's ChatGoogleGenerativeAI - Gemini-2.0-Flash):** The model translates text into the target language.
- **Speech Synthesis (Coqui):** Converts translated text into spoken audio.
- **Sentence Breakdown:** Breaks sentences into individual words for further learning.
- **Dictionary Storage:** Saves phrases and words categorized by language for future study and review.

#### 3.b Regular Chat Mode

- **Conversational AI (LangChain's ChatGoogleGenerativeAI - Gemini-2.0-Flash):** Engages in general chat using an LLM without translation.
- **Multi-turn Conversations:** Maintains conversation context.

---

## Implementation Details

### 1. Tech Stack

- **Frontend:** Streamlit (UI, audio recording, and text input)
- **Backend:** LangGraph (orchestrating workflow), LangChain (LLM processing via LangChain's ChatGoogleGenerativeAI)
- **Audio Processing:** Whisper (speech-to-text), Coqui (text-to-speech)
- **LLM:** LangChain's ChatGoogleGenerativeAI (Model: Gemini-2.0-Flash)
  - [LangChain's ChatGoogleGenerativeAI Documentation](https://python.langchain.com/api_reference/google_genai/chat_models/langchain_google_genai.chat_models.ChatGoogleGenerativeAI.html)

### 2. Directory Structure

```
streamlit_app/
│── graph/         # LangGraph implementation
│── state/         # Application state management
│── instructions/examples/      # Code examples for reference
│── instructions/examples/audio-recorder.py  # Streamlit audio recorder example
│── instructions/examples/whisper-app.py     # Whisper integration example
│── instructions/examples/coqui-app.py       # Coqui integration example
```

### 3. Workflow Breakdown

#### **3.1 Voice Input Flow**

1. User records audio in Streamlit.
2. Whisper transcribes audio to text.
3. The system checks for intent (chat or translation request).The system checks for intent (chat or translation request).
   ## If translation:
   - The system detects the language to translate text to.
   - Translate text via LLM (LangChain's ChatGoogleGenerativeAI - Gemini-2.0-Flash).
   - Convert translated text to speech using Coqui.
   - Store phrases/words categorized by language for learning.
4. If chat:
   - Generate a response using LLM (LangChain's ChatGoogleGenerativeAI - Gemini-2.0-Flash).
   - Display text response.

#### **3.2 Text Input Flow**

1. User enters text manually.
2. System detects the language of the input text.
3. System determines intent (chat or translation).
4. If translation:
   - LLM translates text (LangChain's ChatGoogleGenerativeAI - Gemini-2.0-Flash).
   - Display translated text.
   - Convert to speech via Coqui.
   - Store phrases/words categorized by language.
5. If chat:
   - LLM generates a response (LangChain's ChatGoogleGenerativeAI - Gemini-2.0-Flash).
   - Display response.

---

## UX Design

- **Chat Interface:** ChatGPT-style interface with an input text field and audio recording button.
- **Sidebar:**
  - At the top, two buttons:
    1. **Dictionary:** Allows users to view saved words and phrases categorized by language.
    2. **Phrases:** Displays commonly used translations and learned phrases.
  - **Download Option:** Users should be able to download their dictionary and phrases for offline access. When downloading, users should be prompted to enter an email address before the file is generated..

---

## Documentation & References

- **Building a Chat App in Streamlit:**

  - [Streamlit Chat Guide](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
  - [LLM Quickstart](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/llm-quickstart)
  - [Chat Response Feedback](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/chat-response-feedback)
  - [LangChain Tutorial](https://blog.streamlit.io/langchain-tutorial-1-build-an-llm-powered-app-in-18-lines-of-code/)

- **Audio Processing:**

  - [Whisper (Speech-to-Text)](https://github.com/openai/whisper)

  - Example: `examples/whisper-app.py`

  - [Coqui (Text-to-Speech)](https://docs.coqui.ai/en/latest/)

  - Example: `examples/coqui-app.py`

- **LLM Processing:**

  - [LangChain's ChatGoogleGenerativeAI Documentation](https://docs.litellm.ai/docs/)

---

## Developer Notes

- Ensure **low latency** in voice-to-text and text-to-voice conversion.
- Implement **error handling** for API failures in Whisper, Coqui, and LLM processing.
- Use **LangGraph** to maintain conversation context and manage workflow dependencies.
- **Persist user dictionary** (words/phrases) categorized by language for personalized learning.
- **Enable users to download** their dictionary and phrases for offline study.
- **Optimize UI** for seamless chat and audio recording experience.

---

## Future Enhancements

- Multi-language support for UI and translations.
- Integration with spaced repetition for better vocabulary retention.
- Speech recognition feedback to correct pronunciation.