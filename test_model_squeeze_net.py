# test_model.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey, W, A, S, D
from SqueezeNet.SqueezeNet import *
from getkeys import key_check

import random

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 1000
CLASSES = 3
MODEL_NAME = 'pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(LR, 'squeezenet',EPOCHS)

t_time = 0.09

def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(W)
##    else:
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    #ReleaseKey(W)
    ReleaseKey(D)
    #ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(A)

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    #ReleaseKey(W)
    #ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32,(None,WIDTH,HEIGHT,1))
y = tf.placeholder(tf.float32,(None,CLASSES)) # Not used
keep_prob = tf.placeholder(tf.float32) # Set to 1

model,_,_ = getSqueezeNetModel(x,y,keep_prob,LR)
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
saver.restore(sess,'./SqueezeNet/'+MODEL_NAME)

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    while(True):
        
        if not paused:
            # 800x600 windowed mode
            #screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
            screen = grab_screen(region=(0,40,800,640))
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160,120))

            #prediction = model.predict([screen.reshape(160,120,1)])[0]
            prediction = model.eval({x:screen.reshape(1,160,120,1),keep_prob:1})[0]
            decision = np.argmax(prediction)
            print(decision,prediction)
            
            '''turn_thresh = .75
            fwd_thresh = 0.70

            if prediction[1] > fwd_thresh:
                straight()
            elif prediction[0] > turn_thresh:
                left()
            elif prediction[2] > turn_thresh:
                right()
            else:
                straight()'''

            if decision == 0:
                left()
            elif decision == 1:
                straight()
            else:
                right()

            

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

main()       
