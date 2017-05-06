# Done by Colton-Bryce
from PIL import ImageGrab
from win32gui import FindWindow, SetForegroundWindow, GetWindowRect, ShowWindow
from win32con import SW_SHOWNOACTIVATE

class Camera(object):#Pass the window title e.g. 'Grand Theft Auto V'
    #Make sure the window is on your main monitor or you will get a black screen

    def __init__(self, title):
        self.hwnd = FindWindow(None, title)
         if not self.hwnd:
            raise Exception('Invalid window title')
        SetForegroundWindow(self.hwnd)
        ShowWindow(self.hwnd, SW_SHOWNOACTIVATE)

    def screenshot(self):
        self.bbox = GetWindowRect(self.hwnd)
        img = ImageGrab.grab(self.bbox)

        return img
