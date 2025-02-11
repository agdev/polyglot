from typing import Annotated
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from .state import PolyglotState
# Load environment variables
load_dotenv()

 # Define nodes (placeholder implementations)
    
# def transcribe(state: State) -> State:
#     # TODO: Implement Whisper transcription
#     if state["input_type"] == "audio":
#         state["transcription"] = state["input"]  # Placeholder
#     return state

def detect_intent(state: PolyglotState) -> Annotated[PolyglotState, str]:
    # Initialize ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,  # We want deterministic responses for intent detection
    )
    
    # Get the input text
    text = state["transcription"] if state["input_type"] == "audio" else state["input"]
    
    # Create system message and user message
    messages = [
        (
            "system",
            """You are a helpful assistant that determines if a user's message is a request for translation or a general chat message.
            If the user is asking for translation (either explicitly or implicitly), respond with exactly 'translation'.
            If the user is having a general conversation or asking questions, respond with exactly 'chat'.
            Only respond with one of these two words: 'translation' or 'chat'.
            
            Examples:
            - "Translate 'hello' to Spanish" -> 'translation'
            - "How do you say 'hello' in Spanish" -> 'translation'
            - "What's the weather like?" -> 'chat'
            - "Can you help me learn Spanish?" -> 'chat'
            """
        ),
        ("human", text)
    ]
    
    try:
        # Get intent from LLM
        ai_msg = llm.invoke(messages)
        intent = ai_msg.content.strip().lower()
        
        # Validate intent
        if intent not in ["translation", "chat"]:
            # Default to chat if response is invalid
            intent = "chat"
        
        state["intent"] = intent
        return state, intent
        
    except Exception as e:
        # Log the error (you might want to add proper logging)
        print(f"Error in intent detection: {str(e)}")
        # Default to chat on error
        state["intent"] = "chat"
        return state, "chat"

def translate(state: PolyglotState) -> PolyglotState:
    # TODO: Implement translation using Gemini
    text = state["transcription"] if state["input_type"] == "audio" else state["input"]
    text = text.replace("translate:", "").strip()
    state["translation"] = f"Translation placeholder: {text}"
    return state

def chat_response(state: PolyglotState) -> PolyglotState:
    # TODO: Implement chat using Gemini
    text = state["transcription"] if state["input_type"] == "audio" else state["input"]
    state["response"] = f"Chat response placeholder: {text}"
    return state

def synthesize_speech(state: PolyglotState, config: RunnableConfig) -> PolyglotState:
    # TODO: Implement Coqui TTS
    # Access the config through the configurable key
    tts_model    = config["configurable"].get("tts_model", None)
    state["audio_response"] = tts_model.tts_to_file(state["translation"])
    # state["audio_response"] = tts_model.tts_to_file(state["response"])
    state["audio_response"] = b""  # Placeholder
    return state
    

def create_workflow() -> StateGraph:
    # Initialize workflow graph
    workflow = StateGraph(PolyglotState)
    
   
    # Add nodes to graph
    # workflow.add_node("transcribe", transcribe)
    workflow.add_node("detect_intent", detect_intent)
    workflow.add_node("translate", translate)
    workflow.add_node("chat_response", chat_response)
    workflow.add_node("synthesize_speech", synthesize_speech)
    
    # Define edges
    workflow.add_edge("transcribe", "detect_intent")
    workflow.add_conditional_edges(
        "detect_intent",
        {
            "translation": "translate",
            "chat": "chat_response",
        }
    )
    workflow.add_edge("translate", "synthesize_speech")
    workflow.add_edge("synthesize_speech", END)
    workflow.add_edge("chat_response", END)
    
    # Set entry point
    workflow.set_entry_point("transcribe")
    
    return workflow

# Create singleton instance
workflow = create_workflow()
