import os
import time

import keyboard as kb
import tensorflow as tf

import tf2_processing
from grabscreen import grab_screen

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# model = tf.keras.models.load_model("./models/model_alexnet_V0_500e_500i")
model = tf.keras.models.load_model("./models/alexnet10")



def prediction_to_keys(prediction):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    if prediction.argmax() == 0:
        output = "up"
    elif prediction.argmax() == 1:
        output = "down"
    elif prediction.argmax() == 2:
        output = "right"
    elif prediction.argmax() == 3:
        output = "left"
    elif prediction.argmax() == 4:
        output = "right+up"
    elif prediction.argmax() == 5:
        output = "left+up"
    else:
        output = "up"

    print(prediction, output)
    return output


def main():

    for i in list(range(1))[::-1]:
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    while (True):

        if not paused:
            screen = grab_screen(region=(0, 40, 800, 640))

            screen = tf2_processing.process_image(screen)
            prediction = model.predict(screen)
            keys = prediction_to_keys(prediction)
            kb.press(keys)
            time.sleep(0.20)
            kb.press("up")
            time.sleep(0.15)
            kb.release(keys)

main()