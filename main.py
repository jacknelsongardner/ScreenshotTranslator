import time
#from screenshot import *
#from translation import *
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
        print("gotcha")

if __name__ == "__main__":
    
    main()