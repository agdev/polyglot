**Phase 1: Project Setup and Core Dependencies**
1.  **Create Directory Structure:**
    *   Create the following directory structure inside `streamlit_app`:
        ```
        streamlit_app/
        ├── graph/         # LangGraph implementation
        ├── state/         # Application state management
        ├── components/    # Streamlit components
        ├── utils/         # Utility functions
        ```

**Phase 2: Frontend (Streamlit App) Development**

1.  **Create `streamlit_app/main.py`:**
    *   Set up the basic Streamlit app structure.
    *   Add a title and a simple chat interface with a text input field.

2.  **Implement Chat Interface:**
    *   Create a function to display chat messages.
    *   Create a function to handle user input and send it to the backend.
    *   Use Streamlit's `st.session_state` to manage chat history.

3.  **Implement Audio Recording:**
    *   Use Streamlit's audio recording component (or a custom component) to allow users to record audio.
    *   Handle audio data and send it to the backend.

4.  **Implement Sidebar:**
    *   Add a sidebar with "Dictionary" and "Phrases" buttons.
    *   Create placeholder functions for dictionary and phrases views.
    *   Implement the "Download" option with email prompt (basic implementation, can be refined later).

**Phase 3: Backend (LangGraph) Development**

1.  **Create `streamlit_app/graph/workflow.py`:**
    *   Set up the basic LangGraph workflow.
    *   Define the nodes for transcription, intent detection, translation, speech synthesis, and response generation.

2.  **Implement Transcription Node:**
    *   Integrate Whisper to transcribe audio to text.
    *   Handle API calls to Whisper.

3.  **Implement Intent Detection Node:**
    *   Use a simple rule-based approach or a small LLM to determine if the user's intent is chat or translation.

4.  **Implement Translation Node:**
    *   Integrate LangChain's ChatGoogleGenerativeAI to translate text.
    *   Handle API calls to the LLM.

5.  **Implement Speech Synthesis Node:**
    *   Integrate Coqui to convert translated text to speech.
    *   Handle API calls to Coqui.

6.  **Implement Response Generation Node:**
    *   Use LangChain's ChatGoogleGenerativeAI to generate chat responses.
    *   Handle API calls to the LLM.

7.  **Implement Dictionary Storage:**
    *   Create a function to store phrases and words in a JSON file, categorized by language.

**Phase 4: Integration and Testing**

1.  **Connect Frontend and Backend:**
    *   Implement API endpoints in the backend to receive text and audio data from the frontend.
    *   Send data from the frontend to the backend using HTTP requests.

2.  **Test Voice Input Flow:**
    *   Record audio in the frontend and verify that it is transcribed correctly, translated (if applicable), and played back.

3.  **Test Text Input Flow:**
    *   Enter text in the frontend and verify that it is translated (if applicable) and displayed correctly.

4.  **Test Chat Mode:**
    *   Engage in a conversation with the chatbot and verify that it generates appropriate responses.

5.  **Test Dictionary Functionality:**
    *   Add words and phrases to the dictionary and verify that they are stored correctly.
    *   Test the "Download" option.

**Phase 5: Refinement and Enhancements**

1.  **Implement Error Handling:**
    *   Add error handling for API failures in Whisper, Coqui, and LLM processing.

2.  **Optimize Performance:**
    *   Optimize the performance of the transcription, translation, and speech synthesis processes.

3.  **Improve UI:**
    *   Refine the UI based on user feedback.

4.  **Implement Future Enhancements:**
    *   Implement multi-language support for the UI and translations.
    *   Integrate with spaced repetition for better vocabulary retention.
    *   Implement speech recognition feedback to correct pronunciation.