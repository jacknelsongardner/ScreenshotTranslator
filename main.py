import time
from screenshot import *
from translation import *
from PIL import Image
import pygetwindow as gw
import keyboard

import multiprocessing

# When this button is pressed, a screenshot will be taken and translated
SHOT_BUTTON = 'esc'

# Location to save screenshot images
SHOT_LOCATION = "screenshot.png"

# Addresses for text-image tuples
TXT_LOCAL = 0
TXT_CONT = 1
TXT_CONF = 2

# Main function, waits for keyboard input and takes screenshots
def main():
    print("Starting main process")
    

    running = True
    while running:
        print("\nWaiting for keypress...\n")

        keyboard.wait(SHOT_BUTTON)

        chat_translated_text_list = []
        python_translated_text_list = []
        google_translated_text = []

        extracted_text = []

        print("\n\nTaking Screenshot")
        screenshot: Image = take_screenshot()
        screenshot.save(SHOT_LOCATION)

        print("\n\nGetting Text from Screenshot")
        extracted_text = extract_text_from_image(SHOT_LOCATION, ['en'])
        print(extracted_text)

        print("\n\nTranslating Text from Screenshot with CHATgpt")
        for text_tuple in extracted_text:

            trans_text = translate_text_chat(text_tuple[1], 'hawaiin', 'english')
            chat_translated_text_list = translate_text_chat(text_tuple[1], 'hawaiin', 'english')

        print("\nTranslated Text: ")
        print(chat_translated_text_list)

        print("\n\nTranslating Text from Screenshot with python translate library")
        for text_tuple in extracted_text:

            trans_text = translate_text_pytranslate(text_tuple[1], 'haw', 'en')
            python_translated_text_list.append(trans_text)

        print("\nTranslated Text: ")
        print(python_translated_text_list)

if __name__ == "__main__":
    main()