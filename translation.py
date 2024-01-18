from translate import Translator
import json
import openai
from dotenv import load_dotenv
import os
import re
import langid 

# Load environment variables from .env
load_dotenv()

# Access API keys from the environment variables
chat_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_TRANS_KEY")

# Creating variables to store base and work folders
base_folder = os.getcwd()
work_folder = os.path.join(base_folder,"WORK")

# Translate text using chatGPT api
def translate_text_chat(text_to_translate: str, source_language: str, target_language: str):
    def parse_brackets(response_string):
        # Define a regular expression pattern to match substrings inside curly braces
        pattern = r'\{([^}]+)\}'
    
        # Use re.findall to find all matches in the input string
        matches = re.findall(pattern, response_string)
    
        return matches
    
    # If the inputted text is already in the target language, return NULL
    if determine_lang(text_to_translate) == target_language:
        return None

    # Create OpenAI client
    chatclient = openai.OpenAI(api_key=chat_key)

    chatprompt = '''
    Translate the following text. Translated text should be inside of {} brackets, 
    eg: Input: hello! Output: hola!
    If there's any text not in the source language, just ignore it
    If there's no text in the target language, just return {NULL} with the brackets
    '''

    userprompt = f"translate from f{source_language} to f{target_language}: {text_to_translate} \n if any text is english"

    past_messages = [
        {"role": "system", "content": chatprompt},
        {"role": "user", "content": "Translate to english: hola!"},
        {"role": "assistant", "content": '{hello!}'},
        {"role": "user", "content": userprompt},
    ]

    # Sending request
    completion = chatclient.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=past_messages
    )

    chat_output = completion.choices[0].message.content
    parsed_chat_output = parse_brackets(chat_output)

    return parsed_chat_output

# Translate text using local "translate" library
def translate_text_pytranslate(text, source_language='ja',target_language='en'):
    # Checking to make sure text isn't already in the target language
    if determine_lang(text) == target_language:
        return None
    
    try:
        translator = Translator(from_lang=source_language, to_lang=target_language)
        translation = translator.translate(text)
        
        return translation

    except Exception as e:
        print("error")
        print(f"Error: {e}")
        return None

# Translate text using google translate API
def translate_text_google(text):
    #TODO : implement google translate api
    pass

# Determine what language a piece of text is
def determine_lang(text):
    # Detect the language of the input text
    lang, confidence = langid.classify(text)

    return lang
