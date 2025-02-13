from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from typing import List, Optional
from langchain_core.output_parsers import StrOutputParser
# Models for structured outputs
class Intent(BaseModel):
    Intent: str = Field(description="The intent of the user's message")

def create_detect_intent_chain(llm):
    prompt_template = PromptTemplate.from_template(
        """You are a helpful assistant that determines if a user's message is a request for translation or a general chat message.
        If the user is asking for translation (either explicitly or implicitly), respond with exactly 'translation'.
        If the user is having a general conversation or asking questions, respond with exactly 'chat'.
        Only respond with one of these two words: 'translation' or 'chat'.
        
        Examples:
        - "Translate 'hello' to Spanish" -> 'translation'
        - "How do you say 'hello' in Spanish" -> 'translation'
        - "What's the weather like?" -> 'chat'
        - "Can you help me learn Spanish?" -> 'chat'

        User: {input}    
        """
    )

    
    llm_structured = llm.with_structured_output(Intent)
    return prompt_template | llm_structured

# class ExtractedSentence(BaseModel):
#     sentence: str = Field(description="The cleaned sentence to be translated")
#     source_language: str = Field(description="Detected source language")
#     target_language: Optional[str] = Field(description="Requested target language if specified")

# def create_extract_sentence_chain(llm, user_message: str):
#     prompt_template = PromptTemplate.from_template(
#         """
#         You are a helpful language assistant that extracts the core sentence to be translated from the user's message. 
#         Detect the source language and identify target language if specified.
#         Remove any extra context like 'translate this:' or 'how do you say'.
        
#         Examples:
#         Input: "Can you translate 'hello my friend' to Spanish?"
#         Output: Core sentence: "hello my friend"
#         Source: English
#         Target: Spanish
        
#         Input: "How do you say 'I love programming' in Japanese?"
#         Output: Core sentence: "I love programming"
#         Source: English
#         Target: Japanese
        
#         User message: {user_message}
#         """
#     )
    
#     prompt = prompt_template.format(user_message=user_message)
#     llm_structured = llm.with_structured_output(ExtractedSentence)
#     return prompt | llm_structured

class TranslationOption(BaseModel):
    translation: str = Field(description="The translated text")
    description: str = Field(description="Description of this translation variant")
    # formality_level: str = Field(description="Formality level (formal, informal, neutral)")

class TranslationResponse(BaseModel):
    # source_text: str = Field(description="Original text")
    target_language: str = Field(description="Target language")
    options: List[TranslationOption] = Field(description="List of translation options")

def create_translate_chain(llm):
    # prompt_template = PromptTemplate.from_template(
    #     """Translate the following text from {source_language} to {target_language}.
    #     Provide multiple translation options with different formality levels and explanations.
        
    #     Text to translate: {sentence}
        
    #     For each translation, provide:
    #     1. The translated text
    #     2. A description of when to use this variant
    #     3. The formality level (formal, informal, neutral)
        
    #     Format your response as a structured list of translations with these components.
    #     """
    # )
    
    prompt_template = PromptTemplate.from_template(
        """You are a helpful language assistant that translates text
        Translate the provided user's request.
        Provide possible translations and their respecitve explanations.
        
        <user_request> {user_request} </user_request> 
        In your response, provide:
          - the target language.
          - For each translation, provide:
            1. The translated text
            2. A description of when to use this variant
            
        Respond in JSON format
        Example of JSON response:
        response:{
        "target_language": "here goes the target language",
        "translations":[
                {
                    "translation": "Here goes the translation",
                    "description": "Here goes the description/explanation of the translation",
                }          
            ]
        }
        """
    )
   
    llm_structured = llm.with_structured_output(TranslationResponse)
    return prompt_template | llm_structured

# class WordBreakdown(BaseModel):
#     word: str = Field(description="Individual word")
#     part_of_speech: str = Field(description="Part of speech (noun, verb, etc.)")
#     base_form: str = Field(description="Base/dictionary form")
#     explanation: str = Field(description="Meaning and usage explanation")

# class SentenceBreakdown(BaseModel):
#     words: List[WordBreakdown] = Field(description="List of word breakdowns")
#     # grammar_notes: Optional[str] = Field(description="Additional grammar explanations")


# def create_sentence_breakdown_chain(llm, translation: Translation):
#     prompt_template = PromptTemplate.from_template(
#         """Break down this translated sentence into individual words and provide detailed explanations.
        
#         Original text: {source_text}
#         Translated text: {translation}
        
#         For each word, provide:
#         1. The word itself
#         2. Part of speech
#         3. Base/dictionary form
#         4. Detailed explanation of meaning and usage
        
        
#         """
#     )
    
#     # Use the first translation option for breakdown
#     prompt = prompt_template.format(
#         source_text=translation.source_text,
#         translation=translation.options[0].translation
#     )
#     llm_structured = llm.with_structured_output(SentenceBreakdown)
#     return prompt | llm_structured

def create_chat_response_chain(llm):
    prompt_template = PromptTemplate.from_template(
        """You are a helpful language learning assistant. Engage in conversation with the user,
        helping them practice and learn languages.
        
        Previous conversation:
        {chat_history}
        
        User: {input}
        
        Respond naturally and engagingly, encouraging language practice when appropriate.
        """
    )
    # llm_structured = llm.with_structured_output(ChatResponse)
    return prompt_template | llm | StrOutputParser()



if __name__ == "__main__":
    from langchain_google_genai import ChatGoogleGenerativeAI
    from ..config import load_config

    
    def test_detect_intent_chain():
        config = load_config()
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
        )    
        detect_intent_chain = create_detect_intent_chain(llm)
        result = detect_intent_chain.invoke({"input": "Translate 'hello' to Spanish"})
        print(f"result: {result}")

    test_detect_intent_chain()