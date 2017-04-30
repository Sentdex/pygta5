# Done by Colton-Bryce
from PIL import ImageGrab
import win32gui

class Camera(object):# Pass the window title e.g. 'Grand Theft Auto V'
    # Make sure the window is on your main monitor or you will get a black screen.

    def __init__(self, title):
        self.hwnd = win32gui.FindWindow(None, title)
        win32gui.SetForegroundWindow(self.hwnd)

    def screenshot(self):
        while 1:
            bbox = win32gui.GetWindowRect(self.hwnd)
            img = ImageGrab.grab(bbox)
            if img.size[0] > 1:
                break
                
        return img
