from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from typing import List, Optional, Any
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from functools import partial
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
        # output_parser=JsonOutputParser()
    )

    
    llm_structured = llm.with_structured_output(Intent)
    return prompt_template | llm_structured
    # return prompt_template | llm | StrOutputParser()
    # return prompt_template | llm | JsonOutputParser(pydantic_object=Intent)
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

# def parse_translation_response(result) -> TranslationResponse:
#     parser = JsonOutputParser(pydantic_object=TranslationResponse)
#     return parser.parse(result)

def parse_to_model(result, model: BaseModel) -> Any:
    parser = JsonOutputParser(pydantic_object=model)
    return parser.parse(result)

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
            
        Respond in JSON format.
        Example response:
        {json_format}
        """,
        partial_variables={"json_format": JsonOutputParser(pydantic_object=TranslationResponse).get_format_instructions()}
    )
   
   ##NOTE: using llm.with_structured_output with Free tier google api key does not work
    llm_structured = llm.with_structured_output(TranslationResponse)
    return prompt_template | llm_structured
    # return prompt_template | llm | StrOutputParser() | RunnableLambda(partial(parse_to_model, model=TranslationResponse))
# | JsonOutputParser(pydantic_object=TranslationResponse)

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
    from langchain_openai import ChatOpenAI
    from langchain_google_vertexai import ChatVertexAI

    from dotenv import load_dotenv
    import os
    
    env_path = os.path.join( os.getcwd(), "streamlit_app", "env", ".env")
    load_dotenv(env_path)
    google_api_key = os.getenv("GOOGLE_API_KEY")
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    google_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            api_key=google_api_key
    )

    import vertexai

    print('getcwd',os.getcwd())
    
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    vertexai.init(project=PROJECT_ID, location=LOCATION)

    vertex_llm = ChatVertexAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        api_key=google_api_key
    )

    openai_llm = ChatOpenAI(
        model="gpt-4o-2024-08-06", #"gpt-3.5-turbo-0125"
        api_key=openai_api_key
    )
    
    from langchain_mistralai.chat_models import ChatMistralAI
    mistral_llm = ChatMistralAI(
        model="mistral-large-latest",
        api_key=mistral_api_key
    )

    def test_translate_chain(llm):        
        translate_chain = create_translate_chain(llm)
        result = translate_chain.invoke({"user_request": "Translate 'hello' to Spanish"})
        print(f"result: {result}")
        # parser = JsonOutputParser(pydantic_object=TranslationResponse)
        # translation = parser.parse(result)
        # print(f"translation: {translation}")

    def test_detect_intent_chain(llm):
        # config = load_config()
        detect_intent_chain = create_detect_intent_chain(llm)
        result = detect_intent_chain.invoke({"input": "Translate 'hello' to Spanish"})
        print(f"result: {result}")

    # test_translate_chain(vertex_llm)
    test_detect_intent_chain(vertex_llm)
    
    # {'target_language': 'Spanish', 'options': [{'translation': 'Hola', 'description': "This is the most common and general translation of 'hello'. Use it in most situations."}, {'translation': 'Aló', 'description': "This translation is used in some Latin American countries, especially when answering the phone. It's similar to saying 'hello' on the phone in English."}, {'translation': 'Qué tal', 'description': "This translates more closely to 'What's up?' or 'How's it going?', but can be used as an informal greeting similar to 'hello'."}]}