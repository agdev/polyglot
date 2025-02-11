**I. Overall Architecture**

Polyglot will adopt a modular architecture, separating the frontend (Streamlit app), backend (LangGraph workflows), and external services (Whisper, Coqui, LLM). This promotes maintainability, scalability, and testability.

**II. Component Breakdown**

1.  **Frontend (Streamlit App):**
    *   Responsible for user interaction (text input, audio recording, chat display).
    *   Handles UI elements like the chat interface, sidebar (dictionary, phrases), and download option.
    *   Communicates with the backend via API calls.
    *   Key files: `streamlit_app/main.py` (entry point), UI components in dedicated modules.

2.  **Backend (LangGraph Workflows):**
    *   Orchestrates the overall workflow, managing dependencies between different components.
    *   Handles intent detection (chat vs. translation).
    *   Manages conversation context (multi-turn conversations).
    *   Persists user dictionaries.
    *   Key files: `streamlit_app/graph/workflow.py`, `streamlit_app/graph/nodes.py` (individual processing steps).

3.  **Audio Processing:**
    *   **Whisper:** Transcribes audio to text.  Integrated as an external service called by the backend.
    *   **Coqui:** Converts text to speech. Integrated as an external service called by the backend.

4.  **LLM (LangChain's ChatGoogleGenerativeAI):**
    *   Provides translation and conversational AI functionalities.
    *   Integrated via LangChain.

5.  **Data Storage:**
    *   User dictionaries (words/phrases categorized by language) will be persisted.  The specific database to use is not defined, so I will assume a simple JSON file for now.

**III. Workflow**

The [instructions.MD](cci:7://file:///home/yoda/Library/Projects/Portfolio/Polyglot/instructions/instructions.MD:0:0-0:0) document describes two main workflows: Voice Input and Text Input. LangGraph will manage the state and transitions between steps in these workflows.

**Voice Input Flow:**

1.  Streamlit captures audio.
2.  Streamlit sends audio to backend.
3.  Backend uses Whisper to transcribe audio to text.
4.  Backend determines intent (chat or translation).
5.  If translation:
    *   Backend detects the language.
    *   Backend uses LLM to translate text.
    *   Backend uses Coqui to convert translated text to speech.
    *   Backend stores phrases/words in the dictionary.
    *   Backend sends translated text and audio to Streamlit for display.
6.  If chat:
    *   Backend uses LLM to generate a response.
    *   Backend sends text response to Streamlit for display.

**Text Input Flow:**

1.  Streamlit captures text.
2.  Streamlit sends text to backend.
3.  Backend determines intent (chat or translation).
4.  If translation:
    *   Backend detects the language.
    *   Backend uses LLM to translate text.
    *   Backend uses Coqui to convert translated text to speech.
    *   Backend stores phrases/words in the dictionary.
    *   Backend sends translated text and audio to Streamlit for display.
5.  If chat:
    *   Backend uses LLM to generate a response.
    *   Backend sends text response to Streamlit for display.

**IV. Key Considerations**

*   **Error Handling:** Implement robust error handling for API failures in Whisper, Coqui, and LLM processing.
*   **State Management:** LangGraph will be crucial for maintaining conversation context and managing workflow dependencies.
*   **Persistence:** User dictionaries should be persisted to provide a personalized learning experience.
*   **Scalability:** The architecture should be designed to handle a growing number of users and languages.

**V. Leveraging Documentation**

The [instructions.MD](cci:7://file:///home/yoda/Library/Projects/Portfolio/Polyglot/instructions/instructions.MD:0:0-0:0) file provides links to relevant documentation for Streamlit, Whisper, Coqui, LangGraph, and LangChain. These resources will be essential for implementing the project.

* [How to add cross-thread persistence to your graph](https://langchain-ai.github.io/langgraph/how-tos/cross-thread-persistence/)
* [How to add cross-thread persistence to your graph](https://langchain-ai.github.io/langgraph/how-tos/cross-thread-persistence/)
*   [LangChain's ChatGoogleGenerativeAI Documentation](https://docs.litellm.ai/docs/)
*   [Streamlit Chat Guide](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
*   [Whisper (Speech-to-Text)](https://github.com/openai/whisper)
*   [Coqui (Text-to-Speech)](https://docs.coqui.ai/en/latest/)
*   [Langgraph - cross-thread persistence](https://langchain-ai.github.io/langgraph/how-tos/cross-thread-persistence/)