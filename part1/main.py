import numpy as np
import cv2
from getFrame import getFrameThread
import time

def screen_record():
    frameThread = getFrameThread().start()
    last_time = time.time()
    counter = 0
    
    while(True):
        printscreen = np.array(frameThread.returnFrame())
        
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            frameThread.stopNow()
            cv2.destroyAllWindows()
            break
        counter+=1
    print('Process is running at {} FPS'.format(counter /(time.time()-last_time))) #to get FPS
    
screen_record()
