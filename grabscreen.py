# Done by Frannecklp

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api

bbox_coefficient_4k=np.array([3,3,2.5,2.5])
# this coefficient works for my hp omen laptop (4k screen)

def hwindow_check(window_name):
    hwnd=win32gui.GetDesktopWindow()
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)

    titles = [ title for hwnd, title in winlist ]
    apps= [title for title in titles if window_name in title.lower() ]
    if len(apps)==0:
        print('could not find window:{}'.format(window_name))
        print("return all windows' title")
        return titles
    else :
        return apps

def grab_window_region( window_name ):
    hwnd=win32gui.GetDesktopWindow()
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)
    app = [(hwnd, title) for hwnd, title in winlist if window_name in title.lower()]
    try:
        appfirst = app[0]
        hwnd = appfirst[0]
    except:
        hwindow_check(window_name)

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)

    bbox=np.array( bbox )
    bbox= bbox*bbox_coefficient_4k

    return  tuple( bbox.astype(int) )

def grab_screen(region=None):

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

if __name__=='__main__':
    import time
    def count_down():
        for i in range(5):
            print(5-i)
            time.sleep(1)
    count_down()
    bbox=grab_window_region('blizzard') # for gta5 the window_name should be 'gta5' or somewhat
    # hwindow_check(window_name='gta5')
    # you could use this method to check the window title of the gta5. Nothing print out means okay.
    img=grab_screen( bbox )
    img = cv2.resize(img,None,fx=1/3, fy=1/3, interpolation = cv2.INTER_CUBIC)
    cv2.imshow('window',cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    cv2.waitKey()
