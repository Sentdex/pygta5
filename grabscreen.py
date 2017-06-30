"""
based on work by Frannecklp
changes by dandrews
"""

import win32ui
import win32gui
import win32con
import numpy as np




def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(screen=None, _region=None, _scale=1.0)
def grab_screen(scale = 1.0, region=None, window_title='GameIP'):
    
    """
    Grabs screens from windows applications.
    
    Arguments:        
    :parameter scale: float to scale images by.            
    :parameter regions: tuple of (top, left, height, width). None grabs whole screen.   
    :parameter window_title: string to search title bars for. Defaults to 'Game'
    """
    
    if grab_screen.screen is None or grab_screen._region != region or grab_screen._scale != scale:
        # Cleanup old object and rebuild with new region.
        if grab_screen.screen is not None:
            grab_screen.screen.cleanup()
        
        if region is None:
            grab_screen.screen = windows_screen_grab(window_title=window_title, scale=scale)
        else:
            grab_screen.screen = windows_screen_grab(window_title=window_title, scale=scale, region=region)
    
    bits = grab_screen.screen.get_screen_bits()
    rgb = grab_screen.screen.get_rgb_from_bits(bits)
    grab_screen._region = region
    grab_screen._scale = scale
    return rgb



class windows_screen_grab:
    _hwnd = 0
    
    def enumHandler(self, hwnd, lParam):
        """
        Callback to find correct window handle.
        """
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)            
            if self._search_str in title:                
                self._hwnd = hwnd 
                print(self._search_str + ' found in hwnd ' + str(hwnd))
                print(title)

    def __init__(self, window_title: str, scale = 1.0, region = None):
        """
        :parameter window_title: substring to search for in titles bars. required.
        :parameter scale: float to scale images by.          
        :parameter regions: tuple of (top, left, height, width). None grabs whole screen.            
        """
        self._scale = scale
        self._search_str = window_title

        
        # Scan all windows for substring. TODO: check for ambigious substrings
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
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]    
    
        dest_w = int(w * self._scale)
        dest_h = int(h * self._scale)
        
        dataBitMap = win32ui.CreateBitmap()        
        w_handle_DC = win32gui.GetWindowDC(hwnd)
        windowDC = win32ui.CreateDCFromHandle(w_handle_DC)
        memDC = windowDC.CreateCompatibleDC()
        dataBitMap.CreateCompatibleBitmap(windowDC , dest_w, dest_h)
        memDC.SelectObject(dataBitMap)
        self._w_handle_DC = w_handle_DC
        self._dataBitMap = dataBitMap
        self._memDC = memDC
        self._windowDC = windowDC
        self._height = h
        self._width = w
        self._top  = t
        self._left = l
        self._dest_width = dest_w
        self._dest_height = dest_h
        self._rgb = np.zeros((3,dest_h, dest_w))
    

    """
    Get the raw screen bits.
    returns: a numpy array of the bits in the format (r, g, b, a, r, g, b, a, ...)
    """
    def get_screen_bits(self):        
        self._memDC.StretchBlt((0,0), (self._dest_width, self._dest_height), self._windowDC, (self._top, self._left), (self._width,self._height), win32con.SRCCOPY)        
        bits = np.fromstring(self._dataBitMap.GetBitmapBits(True), np.uint8)
        return bits
    
    
    def get_rgb_from_bits(self, bits):
        """
        Reshape to rgb and strip the alpha channel.
        :parameter bits: numpy array in the format (r, g, b, a, r, g, b, a, ...)
        """    
        bits.shape = (self._dest_height,self._dest_width,4)
        self._rgb[0] = bits[:,:,2]
        self._rgb[1] = bits[:,:,1]
        self._rgb[2] = bits[:,:,0]
        return self._rgb
    
    def cleanup(self):
        """
        Release resources.    
        """        
        self._windowDC.DeleteDC()
        self._memDC.DeleteDC()
        win32gui.ReleaseDC(self._hwnd, self._w_handle_DC)
        win32gui.DeleteObject(self._dataBitMap.GetHandle())    






    