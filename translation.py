from translate import Translator

# Translate with the local python "translate" library
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