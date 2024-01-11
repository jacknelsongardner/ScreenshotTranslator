import time
from screenshot import *
from translation import *
from PIL import Image
import pygetwindow as gw
import multiprocessing
import tkinter as tk
from pynput import keyboard
from screeninfo import get_monitors

# Screen width and height 
SCREEN_WIDTH = 0 #get_monitors()[0].width
SCREEN_HEIGHT = 0 #get_monitors()[0].height

# When this button is pressed, a screenshot will be taken and translated
SCREENSHOT_KEY = keyboard.Key.esc

# Location to save screenshot images
SHOT_LOCATION = "screenshot.png"

# Colors for printing to terminal
RED = "\033[91"
BLUE = "\033[94"
YELLOW = "\033[93"
GREEN = "\033[92"
WHITE = "\033[97"

# Addresses for text-image tuples
TXT_LOCATION = 0
TXT_CONTENT = 1
TXT_CONFIDENCE = 2

# Addresses for tranlsated text tuples
TRANS_LOCATION = 0
TRANS_CONTENT = 1

# Setting up base files
example_screenshot: Image = take_screenshot()
example_screenshot.save(SHOT_LOCATION)

# Real screen size
REAL_SCREEN_WIDTH = example_screenshot.width
REAL_SCREEN_HEIGHT = example_screenshot.height


def perform_translation():
    chat_translated_text_list = []

    extracted_text = []

    # Taking and saving screenshot
    print("\n\nTaking Screenshot")
    screenshot: Image = take_screenshot()
    screenshot.save(SHOT_LOCATION)

    # Extracting text from screenshot
    print("\n\nGetting Text from Screenshot")
    extracted_text = extract_text_from_image(SHOT_LOCATION, ['en'])
    print(extracted_text)

    # Translating extracted text using openAI
    print("\n\nTranslating Text from Screenshot with openAI api")
    for text_tuple in extracted_text:

        translated_content = translate_text_chat(text_tuple[TXT_CONTENT], 'hawaiin', 'english')
        chat_translated_text_list.append(( text_tuple[TXT_LOCATION], translated_content))

    print("\nTranslated Text: ")
    print(chat_translated_text_list)

    return chat_translated_text_list

def make_popup(text_content, text_location, popup_root):
    popup = tk.Toplevel(popup_root)

    # Setting size of popup
    def calculate_popup_geometry(text_corner_coordinates: list):
        X = 0
        Y = 1

        # Convert pixel coordinates to tkinter coordinates
        def convert_pixel_to_tk_coordinates(pixel_coordinates: int):
        
            pixel_width_ratio: float = pixel_coordinates[X] / REAL_SCREEN_WIDTH 
            pixel_height_ratio: float = pixel_coordinates[Y] / REAL_SCREEN_HEIGHT

            tk_screen_width: int = root.winfo_screenwidth()
            tk_screen_height: int = root.winfo_screenheight()

            tk_x = int(pixel_width_ratio * tk_screen_width)
            tk_y = int(pixel_height_ratio * tk_screen_height)

            tk_coordinates = (tk_x,tk_y)

            return tk_coordinates

        bottom_left: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[0])
        bottom_right: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[1])
        top_right: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[2])
        top_left: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[3])

        popup_width = int(top_right[X]) - int(top_left[X])
        popup_height = int(top_left[Y]) - int(bottom_left[Y])

        popup_x = int(top_left[X]) 
        popup_y = int(top_left[Y])

        tk_coordinates = f"{popup_width}x{popup_height}+{popup_x}+{popup_y}"
        return tk_coordinates

    popup_geo = calculate_popup_geometry(text_location)
    print(popup_geo)

    popup.geometry(popup_geo)

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
        if event.keysym == SCREENSHOT_KEY:
            # Destroy self
            popup.destroy()

    popup.bind("<KeyPress>", on_key_press)  

def make_root():
    root = tk.Tk()
    root.title("Screenshot Translator")
    root.geometry("300x200+100+400")

    '''
    # Binding <KeyPress> event to on_key_press method
    def on_key_press(event):
        # Check if the pressed key is the 'Screenshot key'
        if event.keysym == SCREENSHOT_KEY:
            # Take screenshot, translate, etc...
            translated_tuples = perform_translation()

            # Cycling through translated_tuples and making popups for each one
            for trans_tuple in translated_tuples:
                make_popup(trans_tuple[TRANS_CONTENT], 
                           trans_tuple[TRANS_LOCATION], 
                           root)
    

    # Bind the key press event to the function
    root.bind_all("<KeyPress>", on_key_press)
    '''
    
    return root

def on_key_pressed(key, make_popups: bool, popups: list):
    print("key was pressed")
    try:
        # Making sure key pressed was the SCREENSHOT_KEY
        if key == SCREENSHOT_KEY:
            print("screenshot key was pressed")

            # If popups HAVE NOT been made, perform translation and create popups
            if make_popups == True: 
                print("making popups")
                

                # Take screenshot, translate, etc...
                translated_tuples = perform_translation()

                # Cycling through translated_tuples and making popups for each one
                for trans_tuple in translated_tuples:
                    new_popup = make_popup( trans_tuple[TRANS_CONTENT], 
                                            trans_tuple[TRANS_LOCATION], 
                                            root)
                    
                    popups.append(new_popup)  

                return make_popups      

            # If popups HAVE been made, delete previously created popups
            elif make_popups == False:
                print("deleting popups")
                print(popups)
                  
                # Destroy all popups
                for pop in popups:
                    pop.destroy()

                popups.clear()

                return popups
            
            return popups
        
    except AttributeError:
        print(f"{RED}Attribute error : key does not exist")

if __name__ == "__main__":
    # List for storing popups on screen
    popups: list = []   

    # Whether the screenshot key has already been pressed and acted upon
    make_popups = False

    # Function to allow access to local variables when a key is pressed
    def pass_pressed(key):
        # Importing popups and reversing popups on screen
        global popups, make_popups 
        make_popups = not make_popups

        popups = on_key_pressed(key=key, make_popups=make_popups, popups=popups)

    # Creating listener to listen for keyboard input
    listener = keyboard.Listener(on_press=pass_pressed)
    listener.start()

    # Creating root for all popups to belong to
    root = make_root()
    root.mainloop()
    