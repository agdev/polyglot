import streamlit as st
from streamlit_chat_widget import chat_input_widget
from graph.workflow import create_workflow
import pandas as pd

def create_translation_word_dfs(result):
    """
    Create translation and word dataframes from the translation options
    Args:
        result: The result from the workflow
    Returns:
        translation_df: dataframe from the translation options
        word_df: dataframe from the words of the translation options
    """
   # Extract target language
    target_language = result["translation"]["target_language"]
    source_language = result["translation"]["source_language"]
    # Create list to hold rows for DataFrame
    translation_data = []
    word_data = []
    for option in result["translation"]["options"]:
        translation_data.append({
                "Translation_Language": target_language,
                "Source_Language": source_language,
                "Translation": option["translation"],
                "Context": option["description"]
            })
        # For each word in the translation, create a row with translation details
        for word in option["words"]:
            word_data.append({
                "Translation_Language": target_language,
                "Source_Language": source_language,
                "Original_Word": word["original_word"],
                "Translated_Word": word["translated_word"]
            })
    
    # Create DataFrame
    df_translation = pd.DataFrame(translation_data)                        
    df_words = pd.DataFrame(word_data)
    return df_translation, df_words

def merge_translation_word_dfs(session_state, new_translation_df, new_word_df):
    """
    Merge the translation and word dataframes
    Args:
        session_state: The session state
        new_translation_df: The new translation dataframe
        new_word_df: The new word dataframe
    Returns:
        merged_translation_df: The merged translation dataframe
        merged_word_df: The merged word dataframe
    """
    merged_translation_df = None
    merged_word_df = None
    # If existing dataframes exist, merge with new ones
    if hasattr(session_state, 'translation_df') and session_state.translation_df is not None:
        # Merge translation dataframes, dropping duplicates based on language
        merged_translation_df = pd.concat([
            session_state.translation_df,
            new_translation_df
        ]).drop_duplicates(subset=['Translation_Language', 'Source_Language', 'Translation'])
    else:
        merged_translation_df = new_translation_df
        
    if hasattr(st.session_state, 'word_df') and st.session_state.word_df is not None:
        # Merge word dataframes, dropping duplicates based on language 
        merged_word_df = pd.concat([
            session_state.word_df,
            new_word_df
        ]).drop_duplicates(subset=['Translation_Language', 'Source_Language', 'Original_Word', 'Translated_Word'])
    else:
        merged_word_df = new_word_df
    
    return merged_translation_df, merged_word_df

def display_translation_options(translation_options):
    """
    Display the translation options
    Args:
        translation_options: The translation options
    """
    for idx, option in enumerate(translation_options):
        translation_text = option['translation']
        audio_file_path = option['audio_file_path']
        context_text = option['description'] 
        translation_number = idx + 1
        translation_message = f"**Translation {translation_number}:** {translation_text}\n*Context:* {context_text}"
        st.session_state.messages.append({"role": "assistant", "content": translation_message, "audio_file_path": audio_file_path})
        st.markdown(f"**Translation {translation_number}:** {translation_text}")
        st.markdown(f"*Context:* {context_text}")        
        st.audio(audio_file_path)
        # os.remove(audio_file_path)

def process_chat_message(input_text: str, is_audio: bool = False) -> None:
    """
    Process a chat message and update the chat interface with the response.
    
    Args:
        input_text: The text to process (either direct input or transcribed audio)
        is_audio: Boolean indicating if the input was from audio
    """
    # Add user message to chat history
    display_text = f"🎤 *Audio message*:\n{input_text}" if is_audio else input_text
    st.session_state.messages.append({"role": "user", "content": display_text})
    
    with st.chat_message("user"):
        st.markdown(display_text)
        if is_audio:
            st.markdown(input_text)  # Show transcription below audio message
    
    # Process through workflow
    workflow = create_workflow(llm=st.session_state.llm,tts_model=st.session_state.tts)    
    app_workflow = workflow.compile()
    result = app_workflow.invoke({"input": input_text})
    
    # Display assistant response
    with st.chat_message("assistant"):
        if "error" in result and result["error"] is not None:
            st.markdown("An Error occurred while processing your message. Please try again.")
            st.markdown(result["error"])
        elif "chat_resp" in result and result["chat_resp"] is not None:
            st.markdown(result["chat_resp"])
            st.session_state.messages.append({"role": "assistant", "content": result["chat_resp"]})
        elif (result["translation"] is not None):                        
            # Convert translation data to DataFrame                                                
            new_translation_df, new_word_df = create_translation_word_dfs(result)            
            # Merge with existing dataframes
            merged_translation_df, merged_word_df = merge_translation_word_dfs(st.session_state, new_translation_df, new_word_df)            
            # Update session state
            st.session_state.translation_df = merged_translation_df
            st.session_state.word_df = merged_word_df                        
            display_translation_options(result["translation"]["options"])

def display_chat_interface():
    """
    Display the chat interface
    """ 
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # # Create columns for text and audio input
    # col1, col2 = st.columns([4, 1])
    
    # with col1:
    #     prompt = st.chat_input("Type your message here...")
    
    # with col2:
    #     audio = st.audio_input("🎤")
    # with bottom():
    user_input = chat_input_widget()
    # with st.chat_message("user"):
        

    if user_input:                    
        # Process text input
        if "text" in user_input:
            process_chat_message(user_input['text'])
        elif "audioFile" in user_input: # Process audio input
            chat_message_user= st.chat_message("user")
            chat_message_user.markdown("🎤 *Audio message*")
            audio =bytes(user_input["audioFile"])        
            chat_message_user.audio(audio)
            with st.spinner("Transcribing audio..."):
            # chat_message_user.markdown("Transcribing audio...")
                try:
                    transcription = st.session_state.stt.transcribe(audio)
                    print(f"transcription: {transcription}")
                    if transcription and transcription["text"] and len(transcription["text"]) > 0:                    
                        process_chat_message(transcription["text"], is_audio=True)
                    else:
                        chat_message_user.markdown("Transcribing resulted in an empty text, try again")
                except Exception as e:
                    chat_message_user.error(f"Error transcribing audio: {str(e)}")
                    chat_message_user.markdown("Failed to transcribe audio, try again")

# Check for API key before displaying chat interface
if "llm" in st.session_state:
    # Main chat interface
    display_chat_interface()
else:
    st.info("Please configure your GROQ API key to start chatting.")