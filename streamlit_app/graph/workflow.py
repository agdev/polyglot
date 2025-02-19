from typing import Annotated, Dict, Any, Callable
from langgraph.graph import StateGraph, END
# from dotenv import load_dotenv
import os
from .state import PolyglotState, Translation, TranslationOptions
from langchain_core.runnables.config import RunnableConfig
from .configSchema import ConfigSchema
from .chains import create_detect_intent_chain, Intent, create_translate_chain, TranslationResponse, create_chat_response_chain
from stt_tts.models import TTSModel
# Load environment variables
# load_dotenv()

 # Define nodes (placeholder implementations)
    
# def transcribe(state: State) -> State:
#     # TODO: Implement Whisper transcription
#     if state["input_type"] == "audio":
#         state["transcription"] = state["input"]  # Placeholder
#     return state
def create_detect_intent_node(llm)-> Callable[[PolyglotState, RunnableConfig], PolyglotState]:
    detect_intent_chain = create_detect_intent_chain(llm)    
    def detect_intent(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
        print(f"detect_intent")
        print(f"input: {state['input']}")
        try:
            # Get intent from LLM
            response: Intent = detect_intent_chain.invoke({"input": state["input"]})                        
            print(f"intent: {response}")
            intent = response.Intent
            # Validate intent
            if intent  not in ["translation", "chat"]:
                # Default to chat if response is invalid
                intent = "chat"                                                                
        except Exception as e:
            # Log the error (you might want to add proper logging)
            print(f"Error in intent detection: {str(e)}")
            # Default to chat on error
            intent = "chat"

        print(f"intent: {intent}")
        return {"intent": intent}            
    return detect_intent

    

# def create_extract_sentence(llm):
#     def extract_sentence_for_translation(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
#         """Extract sentences for translation using LLM."""
#         text = state["transcription"] if state["input_type"] == "audio" else state["input"]
        
#         messages = [
#             ("system", """Extract the sentence to be translated. Remove any extra context like 'translate this:' 
#             or 'how do you say'. Just return the core sentence to translate."""),
#             ("human", text)
#         ]
        
#         response = llm.invoke(messages)
#         state["sentence_to_translate"] = response.content.strip()
#         return state
    
#     return extract_sentence_for_translation

def create_translate_node(llm)-> Callable[[PolyglotState, RunnableConfig], PolyglotState]:
    translate_chain = create_translate_chain(llm)
    def translate_text(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
        """Translate text and provide multiple options."""
        print(f"translate_text")
        print(f"input: {state['input']}")
        try:
            response:TranslationResponse = translate_chain.invoke({"user_request": state["input"]})
            print(f"response: {response}")
            translation = Translation()
            translation["language"] = response.target_language
            translation["options"] = []
            for option in response.options:
                translation_option = TranslationOptions()
                translation_option["translation"] = option.translation
                translation_option["description"] = option.description
                translation["options"].append(translation_option)
            return {"translation": translation}
        except Exception as e:
            print(f"Error in translate_text: {str(e)}")
            return state
    
    return translate_text

# def create_sentence_breakdown(llm):
#     def break_down_sentence(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
#         """Break down translated sentence into words and store in state."""
#         if not state.get("translation"):
#             return state
            
#         messages = [
#             ("system", """Break down this translation into individual words and provide explanations.
#             Format as a list of word objects with 'word' and 'explanation' fields."""),
#             ("human", state["translation"]["options"][0]["translation"])
#         ]
        
#         response = llm.invoke(messages)
#         state["word_breakdown"] = response.content  # You'll want to parse this properly
#         return state
    
#     return break_down_sentence

def create_tts_node(tts_model:TTSModel) -> Callable[[PolyglotState, RunnableConfig], PolyglotState]:
    """Convert translations to speech."""
    def text_to_speech(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
        print(f"text_to_speech")
        if not state.get("translation"):
            return state
        print(f"translation: {state['translation']}")    
        try:
            translations = state["translation"]["options"]
            audio_files = []
            
            for option in translations:
                audio_path = tts_model.tts_to_file(option["translation"])
                audio_files.append(audio_path)

            print(f"audio_files: {audio_files}")
            return {"audio_response_files": audio_files}
        except Exception as e:
            print(f"Error in text_to_speech: {str(e)}")
            return state
    
    return text_to_speech

def create_chat_response_node(llm)-> Callable[[PolyglotState, RunnableConfig], PolyglotState]:
    chat_response_chain = create_chat_response_chain(llm)
    def chat_response(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
        """Generate a chat response using LLM."""
        response = chat_response_chain.invoke({"chat_history": state["chat_history"], "input": state["input"]})
        return {"chat_resp": response}
    return chat_response

def where_to_go(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
    """Determine where to go based on intent."""
    if state["intent"] == "translation":
        return "translate"
    else:
        return "chat_response"

def create_workflow(llm, tts_model:TTSModel) -> StateGraph:
    """Create the workflow graph with dependencies injected."""
    
    # Initialize workflow graph
    workflow = StateGraph(PolyglotState)
    
    # Create nodes with dependencies
    detect_intent_node = create_detect_intent_node(llm)
    # extract_sentence_node = create_extract_sentence(llm)
    translate_node = create_translate_node(llm)
    # breakdown_node = create_sentence_breakdown(llm)
    tts_node = create_tts_node(tts_model=tts_model)
    chat_response_node = create_chat_response_node(llm)
    # Add nodes to graph
    workflow.add_node("detect_intent", detect_intent_node)
    workflow.add_node("chat_response", chat_response_node)
    # workflow.add_node("extract_sentence", extract_sentence_node)
    workflow.add_node("translate", translate_node)
    # workflow.add_node("break_down_sentence", breakdown_node)
    workflow.add_node("text_to_speech", tts_node)
    
    # Define edges based on flow chart
    workflow.add_conditional_edges(
        "detect_intent",
        where_to_go,
        {
            "translate": "translate",
            "chat_response": "chat_response",
        }
    )
    
    # Translation flow
    workflow.add_edge("translate", "text_to_speech")
    # workflow.add_edge("extract_sentence", "translate")
    # workflow.add_edge("translate", "break_down_sentence")
    # workflow.add_edge("break_down_sentence", "text_to_speech")
    workflow.add_edge("text_to_speech", END)
    
    # Chat flow
    workflow.add_edge("chat_response", END)
    
    # Set entry point
    workflow.set_entry_point("detect_intent")
    
    return workflow