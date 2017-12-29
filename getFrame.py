from threading import Thread
from grabscreen import grab_screen
import time

class getFrameThread:
    def __init__(self, x, y, w, h, window_title_substring):

        self.stop = False
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.window_title_substring = window_title_substring
        self.printscreen = grab_screen(window_title=self.window_title_substring,
                               region=(self.x,self.y,self.w,self.h))
        self.image = None
        self.render_frame_times = []
        self.render_last_time = time.time()

        
    def start(self):
        Thread(target=self.getFrame, args=()).start()
        return self
    
    def getFrame(self):
        self.image = self.printscreen.getFrame()
        self.render_frame_times.append(time.time()-self.render_last_time)
        self.render_frame_times = self.render_frame_times[-20:]
        self.render_last_time = time.time()
        while True:
            if self.stop == True:
                self.printscreen.clear()
                break
            if time.time() - self.render_last_time > 0.0125:
                self.image = self.printscreen.getFrame()
                self.render_frame_times.append(time.time()-self.render_last_time)
                self.render_frame_times = self.render_frame_times[-20:]
                self.render_last_time = time.time()
            
    def returnFrame(self):
        return self.image

    def stopNow(self):
        self.stop = True

    def getFPS(self):
        print('FPS: {}'.format(len(self.render_frame_times) / sum(self.render_frame_times)))
