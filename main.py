import time
from screenshot import *
from translation import *
from PIL import Image
import pygetwindow as gw
import multiprocessing
import tkinter as tk
from pynput import keyboard
from screeninfo import get_monitors

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

# Variables for width, height, x, and y correction
POPUP_WIDTH_CORRECTION = 15
POPUP_HEIGHT_CORRECTION = 15
POPUP_X_CORRECTION = 0
POPUP_Y_CORRECTION = -60

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

        translated_content = translate_text_pytranslate(text_tuple[TXT_CONTENT], 'haw', 'en')
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

            tk_x = int(pixel_width_ratio * tk_screen_width) + POPUP_X_CORRECTION
            tk_y = int(pixel_height_ratio * tk_screen_height) + POPUP_Y_CORRECTION

            tk_coordinates = (tk_x,tk_y)

            return tk_coordinates

        bottom_left: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[0])
        bottom_right: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[1])
        top_right: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[2])
        top_left: list = convert_pixel_to_tk_coordinates(text_corner_coordinates[3])

        popup_width = int(top_right[X]) - int(top_left[X]) + POPUP_WIDTH_CORRECTION
        popup_height = int(top_left[Y]) - int(bottom_left[Y]) + POPUP_HEIGHT_CORRECTION

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

    # Bringing tkinter windows to front of page
    popup_root.attributes('-topmost', 1)
    popup_root.attributes('-topmost', 0)

    # Setting focus to the root
    popup_root.focus_set()

    # Binding <KeyPress> event to on_key_press method
    # Binding <KeyPress> event to on_key_press method
    def key_pressed(event):
        print("key pressed")
        root.after(1, kill_children())

    def kill_children():
        print("destroying")
        # Destroy self
        for widget in popup_root.winfo_children():
            widget.destroy()
    
    popup.bind("<KeyPress>", key_pressed)  

def make_main_root():
    root = tk.Tk()
    root.title("Screenshot Translator")
    root.geometry("380x220+50+200")
    
    user_instructions = '''
                        Press ESC to take a screenshot 
                        and translate contents found
                        
                        Press any button afterwords 
                        to make popups disappear
                        ''' 

    # Create a label inside the window with user instructions
    label = tk.Label(root, text=f"{user_instructions}")
    label.pack(pady=20, anchor='w')

    # Binding <KeyPress> event to on_key_press method
    def key_pressed(event):
        print("key pressed")
        root.after(1, kill_children())

    def kill_children():
        print("destroying")
        # Destroy self
        for widget in root.winfo_children():
            widget.destroy()


    root.bind("<KeyPress>", key_pressed)  

    return root

def create_popups(popups_root):
    
    print("Creating popups")

    # Take screenshot, translate, etc...
    translated_tuples = perform_translation()

    # Cycling through translated_tuples and making popups for each one
    for trans_tuple in translated_tuples:

        # Checking if content is null
        if trans_tuple[TRANS_CONTENT] != None:
            make_popup( trans_tuple[TRANS_CONTENT], 
                        trans_tuple[TRANS_LOCATION], 
                        popups_root)

if __name__ == "__main__":

    # Creating root window for user options, etc
    root = make_main_root()

    # Function to allow access to local variables when a key is pressed
    def on_key_press(key):
        try: 
            # If key pressed was screenshot key
            if key == SCREENSHOT_KEY:
                # Spawn popups
                create_popups(popups_root=root)

        except AttributeError:
            print(f"{RED}Attribute error : key does not exist")

    # Creating listener to listen for keyboard input
    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()

    root.mainloop()
    