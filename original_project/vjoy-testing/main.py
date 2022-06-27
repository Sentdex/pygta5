import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey, W, A, S, D
from models import inception_v3 as googlenet
from getkeys import key_check
from collections import deque, Counter
import random
from statistics import mode,mean
import numpy as np
from vjoy import vJoy, ultimate_release

vj = vJoy()

GAME_WIDTH = 1920
GAME_HEIGHT = 1080

how_far_remove = 800
rs = (20,15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen=log_len)

WIDTH = 160
HEIGHT = 90
LR = 1e-3
EPOCHS = 10

DELTA_COUNT_THRESHOLD = 1000

def delta_images(t0, t1, t2):
    d1 = cv2.absdiff(t2, t0)
    return d1

choices = deque([], maxlen=5)

hl_hist = 250
choice_hist = deque([], maxlen=hl_hist)


w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

model = googlenet(WIDTH, HEIGHT, 3, LR, output=9)
MODEL_NAME = 'trained_models/googlenet/pygta5-FPV-color-googlenet_color-0.001-LR-171-files-balanced-v12.model'
model.load(MODEL_NAME)

print('We have loaded a previous model!!!!')

def main():
    '''
with the z axis, your %s are out of 32,786
with the x and y, your %s are out of 16393
...so left = 16393 - (some % of 16393) ... right = 16393 + (some % of 16393)
    '''
    ################
    XYRANGE = 16393
    ZRANGE = 32786
    
    wAxisX = 16393
    wAxisY = 16393
    wAxisZ = 0
    wAxisXRot = 16393
    wAxisYRot = 16393
    wAxisZRot = 0

    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)


    #how_long_since_move = 0
    paused = False
    mode_choice = 0

    screen = grab_screen(region=(0,40,GAME_WIDTH,GAME_HEIGHT+40))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    prev = cv2.resize(screen, (160,90))

    t_minus = prev
    t_now = prev
    t_plus = prev

    while(True):
        
        if not paused:
            screen = grab_screen(region=(0,40,GAME_WIDTH,GAME_HEIGHT+40))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

            last_time = time.time()
            screen = cv2.resize(screen, (160,90))

            delta_view = delta_images(t_minus, t_now, t_plus)
            retval, delta_view = cv2.threshold(delta_view, 16, 255, 3)
            cv2.normalize(delta_view, delta_view, 0, 255, cv2.NORM_MINMAX)
            img_count_view = cv2.cvtColor(delta_view, cv2.COLOR_RGB2GRAY)
            delta_count = cv2.countNonZero(img_count_view)
            dst = cv2.addWeighted(screen,1.0, delta_view,0.6,0)

            now=time.time()
            delta_count_last = delta_count

            t_minus = t_now
            t_now = t_plus
            t_plus = screen
            t_plus = cv2.blur(t_plus,(4,4))

            o_prediction = model.predict([screen.reshape(160,90,3)])[0]
            #                                              w     s     a    d    wa    wd    sa   sd    nk
            prediction = np.array(o_prediction) * np.array([4.5, 0.1, 0.1, 0.1,  1.8,   1.8, 0.5, 0.5, 0.2])


            ##                                               w     s     a   d    wa   wd   sa   sd   nk 
            joy_choices = np.array(o_prediction) * np.array([4.5, 2.0, 1.0, 1.0, 1.8, 1.8, 1.0, 1.0, 1.0])
            # could in theory be a negative.
            
            #            w                s                sa             sd                    nk
            throttle = joy_choices[0] - joy_choices[1] - joy_choices[6] - joy_choices[7] - joy_choices[8]

            # - is left.. .+ is right.  (16393 + (-/+ up to 16393))
            #            a                  wa                       sa                 d            wd                  sd
            turn = (-1*joy_choices[2]) +(-1*joy_choices[4]) +(-1*joy_choices[6]) + joy_choices[3] + joy_choices[5]  + joy_choices[7]


            if throttle < -1 : throttle = -1
            elif throttle > 1 : throttle = 1

            if turn < -1 : turn = -1
            elif turn > 1 : turn = 1


            motion_log.append(delta_count)
            motion_avg = round(mean(motion_log),3)
            fps  = 1 / round(time.time()-last_time, 3)
            
            if throttle > 0:
                vj.open()
                joystickPosition = vj.generateJoystickPosition(wAxisZ=int(ZRANGE*throttle),wAxisX=int(XYRANGE + (turn*XYRANGE)))
                vj.update(joystickPosition)
                time.sleep(0.001)
                vj.close()
                print('FPS {}. Motion: {}. ThumbXaxis: {}. Throttle: {}. Brake: {}'.format(fps , motion_avg, int(XYRANGE + (turn*XYRANGE)), int(ZRANGE*throttle),0))  

            else:
                vj.open()
                joystickPosition = vj.generateJoystickPosition(wAxisZRot=int(-1*(ZRANGE*throttle)),wAxisX=int(XYRANGE + (turn*XYRANGE)))
                vj.update(joystickPosition)
                time.sleep(0.001)
                vj.close()
                print('FPS {}. Motion: {}. ThumbXaxis: {}. Throttle: {}. Brake: {}'.format(fps , motion_avg, int(XYRANGE + (turn*XYRANGE)), 0, int(-1*(ZRANGE*throttle))))  

            mode_choice = np.argmax(prediction)

            if motion_avg < motion_req and len(motion_log) >= log_len:
                print('WERE PROBABLY STUCK FFS, initiating some evasive maneuvers.')
                # 0 = reverse straight, turn left out
                # 1 = reverse straight, turn right out
                # 2 = reverse left, turn right out
                # 3 = reverse right, turn left out

                quick_choice = random.randrange(0,4)
                
                if quick_choice == 0:
                    reverse()
                    time.sleep(random.uniform(1,2))
                    forward_left()
                    time.sleep(random.uniform(1,2))

                elif quick_choice == 1:
                    reverse()
                    time.sleep(random.uniform(1,2))
                    forward_right()
                    time.sleep(random.uniform(1,2))

                elif quick_choice == 2:
                    reverse_left()
                    time.sleep(random.uniform(1,2))
                    forward_right()
                    time.sleep(random.uniform(1,2))

                elif quick_choice == 3:
                    reverse_right()
                    time.sleep(random.uniform(1,2))
                    forward_left()
                    time.sleep(random.uniform(1,2))


                for i in range(log_len-2):
                    del motion_log[0]
                    

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            ultimate_release()
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
