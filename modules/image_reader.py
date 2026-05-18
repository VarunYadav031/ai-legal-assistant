from PIL import Image
import pytesseract
import cv2
import numpy as np


def extract_text_from_image(image_file):

    image = Image.open(image_file)

    # convert to numpy
    img = np.array(image)

    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR
    text = pytesseract.image_to_string(gray)

    return text