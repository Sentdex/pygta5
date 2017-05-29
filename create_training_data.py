# create_training_data.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
from settings import TRAINING_DATA_PATH, RESIZE_WIDTH, RESIZE_HEIGHT, PAUSE_KEY

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''
    output = [0,0,0]

    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1
    return output

if os.path.isfile(TRAINING_DATA_PATH):
    print('File exists, loading previous data!')
    training_data = list(np.load(TRAINING_DATA_PATH))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main(countdown=4, save_every=1000):

    for i in reversed(range(countdown)):
        print(i+1)
        time.sleep(1)


    paused = False
    while(True):

        if not paused:
            # 800x600 windowed mode
            screen = grab_screen()
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (RESIZE_WIDTH, RESIZE_HEIGHT))
            # resize to something a bit more acceptable for a CNN
            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen,output])

            if len(training_data) % save_every == 0:
                print(len(training_data))
                np.save(TRAINING_DATA_PATH,training_data)

        keys = key_check()
        if PAUSE_KEY in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main()
