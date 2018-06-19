# Done by Frannecklp

import cv2
import numpy as np
import sys

if sys.paltform.startswith('win'):
    import win32gui, win32ui, win32con, win32api    
else:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')

    from gi.repository import Gdk, Gtk, GdkPixbuf
    from PIL import Image


def grab_screen(region=None):
    if sys.platform.startswith('win'):

        hwin = win32gui.GetDesktopWindow()

        if region:
                left,top,x2,y2 = region
                width = x2 - left + 1
                height = y2 - top + 1
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    
    else:
        window = Gdk.get_default_root_window()
        sz = window.get_geometry()[2:4]
        if region:
            (x, y, w, h) = region
        else:
            screen = Gtk.Window().get_screen()
            (x, y, w, h) = (0, 0, screen.get_width(), screen.get_height())
        
        pb = Gdk.pixbuf_get_from_window(window, x, y, w, h)
            
        pb = np.array(Image.frombytes("RGB", (w, h), pb.get_pixels()))
        
        return cv2.cvtColor(pb, cv2.COLOR_BGR2RGB)
 
