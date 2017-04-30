# Done by Colton-Bryce
from PIL import ImageGrab
from win32gui import FindWindow, SetForegroundWindow, GetWindowRect

class Camera(object):#Pass the window title e.g. 'Grand Theft Auto V'
    #Make sure the window is on your main monitor or you will get a black screen

    def __init__(self, title):
        self.hwnd = FindWindow(None, title)
        SetForegroundWindow(self.hwnd)

    def screenshot(self):
        while 1:
            self.bbox = GetWindowRect(self.hwnd)
            img = ImageGrab.grab(self.bbox)

            if img.size[0] > 1:
                break

        return img
