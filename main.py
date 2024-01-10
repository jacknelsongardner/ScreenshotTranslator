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
    keyboard.hook(on_key_event)

    running = True
    while running:
        pass

def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN and e.name == SHOT_BUTTON:
        screenshot_and_translate()

def screenshot_and_translate():
    print("gotcha")


if __name__ == "__main__":
    
    process = multiprocessing.Process(target=main)
    process.start()