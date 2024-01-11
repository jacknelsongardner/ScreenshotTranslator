import time
from screenshot import *
from translation import *
from PIL import Image
import pygetwindow as gw
import keyboard

import multiprocessing

import tkinter as tk

# When this button is pressed, a screenshot will be taken and translated
SHOT_KEY = 'Escape'

# Location to save screenshot images
SHOT_LOCATION = "screenshot.png"

# Addresses for text-image tuples
TXT_LOCATION = 0
TXT_CONTENT = 1
TXT_CONFIDENCE = 2

# Main function, waits for keyboard input and takes screenshots
def main():
    print("Starting main process")
    

    running = True
    while running:
        print("\nWaiting for keypress...\n")

        keyboard.wait(SHOT_KEY)

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

            trans_text = translate_text_chat(text_tuple[TXT_CONTENT], 'hawaiin', 'english')
            chat_translated_text_list = translate_text_chat(text_tuple[1], 'hawaiin', 'english')

        print("\nTranslated Text: ")
        print(chat_translated_text_list)

        print("\n\nTranslating Text from Screenshot with python translate library")
        for text_tuple in extracted_text:

            trans_text = translate_text_pytranslate(text_tuple[TXT_CONTENT], 'haw', 'en')
            python_translated_text_list.append(trans_text)

        print("\nTranslated Text: ")
        print(python_translated_text_list)

def make_popup(text_content, text_location, popup_root):
    popup = tk.Toplevel(popup_root)

    # Setting size of popup
    def calculate_popup_geometry(text_corner_coordinates: list):
        X = 0
        Y = 1

        top_left: list = text_corner_coordinates[0]
        top_right: list = text_corner_coordinates[1]
        bottom_right: list = text_corner_coordinates[2]
        bottom_left: list = text_corner_coordinates[3]

        popup_width = top_left[X] - top_right[X]
        popup_height = top_left[Y] - bottom_left[Y]

        popup_x = top_left[X]
        popup_y = top_left[Y]

        tk_coordinates = f"{popup_width}x{popup_height}+{popup_x}+{popup_y}"
        return tk_coordinates

    popup.geometry(calculate_popup_geometry(text_location))

    # Set initial transparency (0.5 for semi-transparency)
    def set_transparency(window, alpha):
        window.attributes("-alpha", alpha)
        
    set_transparency(popup, 0.5)

    # Create a label inside the window
    label = tk.Label(popup, text=f"{text_content}")
    label.pack(padx=20, pady=20)

    # Binding <KeyPress> event to on_key_press method
    def on_key_press(event):
        # Check if the pressed key is the 'Screenshot key'
        if event.keysym == SHOT_KEY:
            # Destroy self
            popup.destroy()

    popup.bind("<KeyPress>", on_key_press)  

def make_root():
    root = tk.Tk()
    root.title("Screenshot Translator")
    root.geometry("300x200+100+400")

    # Binding <KeyPress> event to on_key_press method
    def on_key_press(event):
        # Check if the pressed key is the 'Screenshot key'
        if event.keysym == SHOT_KEY:
            # Destroy self
            make_popup("popup",[[10,10],[100,10],[100,100],[100,10]], root)


    # Bind the key press event to the function
    root.bind("<KeyPress>", on_key_press)

    return root


if __name__ == "__main__":
    # Creating root for all popups to belong to
    root = make_root()
    root.mainloop()
    