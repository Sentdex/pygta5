# create_training_data.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
from PYXInput.read_state import get_state
import os


def old_keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array

    [A,W,D] boolean values.
    '''

    output = [0, 0, 0]

    if 'A' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1
    return output


def keys_to_output(controller_id):
    '''
    Convert controller state in to a ...multi-hot... array

    [%Left,%RightTrigger,%Right] boolean values.
    '''

    state = get_state(controller_id)
    output = [0, 0, 0]
    deadzone = 4000

    if state.left_trigger < -deadzone:
        output[0] = round(state.thumb_lx / -32768, 2)
    elif state.left_trigger > deadzone:
        output[2] = round(state.thumb_lx / 32767, 2)
    else:
        output[1] = round(state.thumb_lx / 255, 2)

    return output


file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():

    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False

    # Integer ID of controller (1 to 4)
    controller_id = 0

    while(True):

        if not paused:
            # 800x600 windowed mode
            screen = grab_screen(region=(0, 40, 800, 640))
            last_time = time.time()
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (160, 120))
            # resize to something a bit more acceptable for a CNN
            keys = key_check()
            output = keys_to_output(controller_id)
            training_data.append([screen, output])

            if len(training_data) % 1000 == 0:
                print(len(training_data))
                np.save(file_name, training_data)

        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)


main()
