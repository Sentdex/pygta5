import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os

up = [1, 0, 0, 0, 0, 0, 0, 0, 0]
down = [0, 1, 0, 0, 0, 0, 0, 0, 0]
right = [0, 0, 1, 0, 0, 0, 0, 0, 0]
left = [0, 0, 0, 1, 0, 0, 0, 0, 0]
up_right = [0, 0, 0, 0, 1, 0, 0, 0, 0]
up_left = [0, 0, 0, 0, 0, 1, 0, 0, 0]
down_right = [0, 0, 0, 0, 0, 0, 1, 0, 0]
down_left = [0, 0, 0, 0, 0, 0, 0, 1, 0]
nothing = [0, 0, 0, 0, 0, 0, 0, 0, 1]

starting_value = 1

while True:
    file_name = './collected_data/training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!', starting_value)

        break


def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    if 'up' in keys:
        output = up
    elif 'down' in keys:
        output = up
    elif 'right' in keys:
        output = right
    elif 'left' in keys:
        output = left
    elif 'right+down' in keys:
        output = down_right
    elif 'right+up' in keys:
        output = up_right
    elif 'left+down' in keys:
        output = down_left
    elif 'left+up' in keys:
        output = up_left
    else:
        output = nothing
    return output


def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while (True):

        if not paused:
            screen = grab_screen(region=(0, 40, 800, 640))
            last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            # screen = cv2.resize(screen, (480, 270))
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            keys = key_check()
            output = keys_to_output(keys)
            training_data.append([screen, output])

            last_time = time.time()
            cv2.imshow('window',cv2.resize(screen,(640,360)))
            if cv2.waitKey(25) & 0xFF == ord('q'):
               cv2.destroyAllWindows()
               break

            if len(training_data) % 100 == 0:
                print(len(training_data))

                if len(training_data) == 500:
                    np.save(file_name, training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = './collected_data/training_data-{}.npy'.format(starting_value)

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


main(file_name, starting_value)
