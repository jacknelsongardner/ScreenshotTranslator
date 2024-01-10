import time
from screenshot import *
from translation import *
from PIL import Image
import pygetwindow as gw
import keyboard

import multiprocessing

# When this button is pressed, a screenshot will be taken and translated
SHOT_BUTTON = 'esc'

def main():
    print("Starting main process")
    

    running = True
    while running:
        keyboard.wait(SHOT_BUTTON)

        print("\nTaking Screenshot")
        screenshot: Image = take_screenshot()

        print("\nGetting Text from Screenshot")
        extracted_text = extract_text_from_image(screenshot, ['en'])

        print("\nTranslating Text from Screenshot")
        translated_text = translate_text_chat(extracted_text)

        print(translated_text)

if __name__ == "__main__":
    main()