import cv2
import numpy as np
from PIL import ImageGrab

def grab_screen(region=None):

    if region:
            left, top, x2, y2 = region
            width = x2 - left + 1
            height = y2 - top + 1

    img = np.array(ImageGrab.grab(bbox=(0, 40, 800, 600)))

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
