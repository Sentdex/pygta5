#!/usr/bin/env python
"""This is a fully controller input setup can be used with the training data set easily for capturing gamepad data and utizile it for training AI,
this approach will pave way for successfully designing a bot that can drive vehicle like real life scenarios.""" 
from inputs import get_gamepad
import math

def read():
    max_trig = math.pow(2, 8)
    max_joy = math.pow(2, 15)
    joy=0
    events = get_gamepad()
    #These are the options we can use for recognising which key has been pressed.
    for event in events:
      #All types of input and how to capture then are given below within curly braces. 
        {if event.code == 'ABS_X':
        elif event.code == 'ABS_X':
        elif event.code == 'ABS_RY':
        elif event.code == 'ABS_RX':
        elif event.code == 'ABS_Z':
        elif event.code == 'ABS_RZ':
        elif event.code == 'BTN_TL':
        elif event.code == 'BTN_TR':
        elif event.code == 'BTN_SOUTH':
        elif event.code == 'BTN_NORTH':
        elif event.code == 'BTN_WEST':
        elif event.code == 'BTN_EAST':
        elif event.code == 'BTN_THUMBL':
        elif event.code == 'BTN_THUMBR':
        elif event.code == 'BTN_SELECT':
        elif event.code == 'BTN_START':
        elif event.code == 'BTN_TRIGGER_HAPPY1':
        elif event.code == 'BTN_TRIGGER_HAPPY2':
        elif event.code == 'BTN_TRIGGER_HAPPY3':
        elif event.code == 'BTN_TRIGGER_HAPPY4':}
            joy = event.state / max_joy# normalize between -1 and 1 only applicable for "ABS_value"
            joy=event.state#for "BTN_value"
#This apporach has can be combined with Xbox 360ce controller emulation softwares and the output can also be presented using simmilar approach.
return joy
