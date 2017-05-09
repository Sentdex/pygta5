# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api

def grab_screen(region=None, title=None):

    if region:
        hwin = win32gui.GetDesktopWindow()
        left,top,x2,y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    elif title:
        hwin = win32gui.FindWindow(None, title)
        if not hwin:
            raise Exception('window title not found')
        #get the bounding box of the window
        win_left, win_top, win_x2, win_y2 = win32gui.GetWindowRect(hwin)
        # get the box of the client part, left and top are always 0,0 so x2,y2
        # are always height and width
        left, top, width, height = win32gui.GetClientRect(hwin)
        win_width = win_x2 - win_left +1
        win_height = win_y2 - win_top +1
        # differnce in the H and W are the bounding of the title bar and window
        left = win_width - width
        top = win_height - height
    else:
        hwin = win32gui.GetDesktopWindow()
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
