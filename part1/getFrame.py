from threading import Thread
from PIL import ImageGrab

class getFrameThread:

    def __init__(self):

        self.printscreen = ImageGrab.grab(bbox=(0,40,800,640))
        self.stop=False
        
    def start(self):
        Thread(target=self.getFrame, args=()).start()
        return self
    
    def getFrame(self):
        while True:
            if self.stop == True:
                break
            self.printscreen = ImageGrab.grab(bbox=(0,40,800,640))

    def returnFrame(self):

        return self.printscreen

    def stopNow(self):

        self.stop = True
