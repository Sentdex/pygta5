# test_model.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey, ReleaseKey, W, A, S, D
from alexnet import alexnet
from getkeys import key_check

from PYXInput.controller import Controller

import random

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'pygta5-car-fast-{}-{}-{}-epochs-300K-data.model'.format(
    LR, 'alexnetv2', EPOCHS)

t_time = 0.09


#
def straight(con, percent):
    con.SetValue('TriggerR', percent)


def left(con, percent):
    con.SetValue('AxisX', -percent)


def right(con, percent):
    con.SetValue('AxisX', percent)


def stop(con):
    con.SetValue('AxisX', 0)
    con.SetValue('TriggerR', 0)


def old_straight():
    # if random.randrange(4) == 2:
    # ReleaseKey(W)
    # else:
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def old_left():
    PressKey(W)
    PressKey(A)
    # ReleaseKey(W)
    ReleaseKey(D)
    # ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(A)


def old_right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    # ReleaseKey(W)
    # ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)


model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


def main():
    # Plug in virtual controller
    controller = Controller()

    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while(True):

        if not paused:
            # 800x600 windowed mode
            #screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
            screen = grab_screen(region=(0, 40, 800, 640))
            print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160, 120))

            prediction = model.predict([screen.reshape(160, 120, 1)])[0]
            print(prediction)

            # Lowered turn threshhold
            turn_thresh = 0.30
            fwd_thresh = 0.70

            # Set turn and forward to the prediction %
            if prediction[1] > fwd_thresh:
                straight(controller, prediction[1])
            elif prediction[0] > turn_thresh:
                left(controller, prediction[0])
            elif prediction[2] > turn_thresh:
                right(controller, prediction[2])
            else:
                straight(controller, 1)
                # or stop?? I'm not sure

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True

                # Stop on pause
                stop(controller)
                # ReleaseKey(A)
                # ReleaseKey(W)
                # ReleaseKey(D)
                time.sleep(1)


main()
