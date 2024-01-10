import time
from PIL import Image
import pyautogui
import easyocr

# Takes a screenshot of the entire screen
def take_screenshot():
    # Get the current timestamp to use as part of the screenshot filename
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Specify the filename with the timestamp
    filename = f"screenshot_{timestamp}.png"
    image: Image = pyautogui.screenshot(filename)
    image.save(filename, format='PNG')
    # Take a screenshot and save it with the specified filename
    return filename

# Extracts text from a image object using easyOCR
def extract_text_from_image(image: Image, languages: list[str]):

    reader = easyocr.Reader(languages)
    
    try:
        # Use pytesseract to do OCR on the image
        text = reader.readtext(image)

        return text

    except Exception as e:
        print(f"Error: {e}")
        return None