"""
based on work by Frannecklp
changes by dandrews
revised and optimized by Werseter
"""

import win32ui
import win32gui
import win32con
import numpy as np

class grab_screen:
    def __init__(self, region=None, window_title='Game', window_handle=None):
        self.region = region
        self.window_title = window_title
        self.window_handle = window_handle
        self.screen = windows_screen_grab(window_title=self.window_title, region=self.region, window_handle=self.window_handle)


    def getFrame(self):
        bits = self.screen.get_screen_bits()
        rgb = self.screen.get_rgb_from_bits(bits)
        if self.window_handle is None:
            self.window_handle = self.screen.getHandle()
        return rgb

    def clear(self):
        self.screen.cleanup()
            
class windows_screen_grab:
    _hwnd = 0
    
    def enumHandler(self, hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)            
            if self._search_str in title:                
                self._hwnd = hwnd 
##                print(self._search_str + ' found in hwnd ' + str(hwnd))
##                print(title)

    def __init__(self, window_title: str, region = None, window_handle = None):
        self._search_str = window_title
        if window_handle:        
            self._hwnd = window_handle
        else:
            win32gui.EnumWindows(self.enumHandler, None)
            if self._hwnd == 0:
                message = "window_title '{}' not found.".format(window_title)
                raise ValueError(message)
        
        hwnd = self._hwnd
             
        if region is None:
            rect = win32gui.GetWindowRect(hwnd)
        else:
            rect = region

        t = rect[0]
        l = rect[1]
        w = rect[2]
        h = rect[3]
        
        dataBitMap = win32ui.CreateBitmap()        
        w_handle_DC = win32gui.GetWindowDC(hwnd)
        windowDC = win32ui.CreateDCFromHandle(w_handle_DC)
        memDC = windowDC.CreateCompatibleDC()
        dataBitMap.CreateCompatibleBitmap(windowDC, w, h)
        memDC.SelectObject(dataBitMap)
        self._w_handle_DC = w_handle_DC
        self._dataBitMap = dataBitMap
        self._memDC = memDC
        self._windowDC = windowDC
        self._height = h
        self._width = w
        self._top  = t
        self._left = l
        self._rgb = np.zeros((3, h, w), dtype=np.int)
    
    def get_screen_bits(self):        
        self._memDC.StretchBlt((0,0), (self._width, self._height), self._windowDC, (self._top, self._left), (self._width, self._height), win32con.SRCCOPY)        
        bits = np.fromstring(self._dataBitMap.GetBitmapBits(True), np.uint8)
        bits = np.delete(bits, slice(3, None, 4))
        return bits
    
    def get_rgb_from_bits(self, bits):
        bits.shape = (self._height, self._width, 3)
        self._rgb = bits
        return self._rgb
    
    def cleanup(self):     
        self._windowDC.DeleteDC()
        self._memDC.DeleteDC()
        win32gui.ReleaseDC(self._hwnd, self._w_handle_DC)
        win32gui.DeleteObject(self._dataBitMap.GetHandle())    

    def getHandle(self):
        return self._hwnd
   
