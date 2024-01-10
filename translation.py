from translate import Translator
import json
import openai
from dotenv import load_dotenv
import os
import re

unicode_ranges: dict = {}

# Read the JSON file
with open('unicode_ranges.json', 'r') as file:
    unicode_ranges = json.load(file)

# Load environment variables from .env
load_dotenv()

# Access API keys from the environment variables
chat_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_TRANS_KEY")

# Creating variables to store base and work folders
base_folder = os.getcwd()
work_folder = os.path.join(base_folder,"WORK")

# Translate text using chatGPT api
def translate_text_chat(userprompt: str):
    def parse_brackets(response_string):
        # Define a regular expression pattern to match substrings inside curly braces
        pattern = r'\{([^}]+)\}'
    
        # Use re.findall to find all matches in the input string
        matches = re.findall(pattern, response_string)
    
        return matches
    
    # Create OpenAI client
    chatclient = openai.OpenAI(api_key=chat_key)

    chatprompt = '''
    Translate the following text. Translated text should be inside of {} brackets, 
    eg: Input: hello! Output: hola!
    '''

    past_messages = [
        {"role": "system", "content": chatprompt},
        {"role": "user", "content": "Translate to english: hola!"},
        {"role": "assistant", "content": '{hello!}'},
        {"role": "user", "content": userprompt},
    ]
    
    asking = True

    completion = chatclient.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=past_messages
    )

    chat_output = completion.choices[0].message.content
    parse_chat_output = parse_brackets(chat_output)

    return chat_output

# Translate text using local "translate" library
def translate_text_pytranslate(text, source_language='ja',target_language='en'):
    print("translating")
    print(text)
    try:
        print(text)
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
   
