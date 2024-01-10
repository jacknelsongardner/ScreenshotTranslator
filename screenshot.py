import time
from PIL import Image
import pyautogui

def take_screenshot():
    # Get the current timestamp to use as part of the screenshot filename
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Specify the filename with the timestamp
    filename = f"screenshot_{timestamp}.png"
    image: Image = pyautogui.screenshot(filename)
    image.save(filename, format='PNG')
    # Take a screenshot and save it with the specified filename
    return filename
