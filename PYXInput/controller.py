"""Virtual Controller Object for Python

Python Implepentation of vXbox from http://vjoystick.sourceforge.net/site/index.php/vxbox"""
from ctypes import *

xinput = WinDLL('vXboxInterface-x64\\vXboxInterface.dll')

DPAD_UP = 1
DPAD_DOWN = 2
DPAD_LEFT = 4
DPAD_RIGHT = 8


class MaxInputsReachedError(Exception):
    """Exception when no inputs are available.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class Controller(object):
    """Virtual Controller Object"""
    available_ids = [1, 2, 3, 4]
    unavailable_ids = []

    def __init__(self):
        if len(Controller.available_ids):
            self.PlugIn()
        else:
            raise MaxInputsReachedError('Max Inputs Reached')

    def __del__(self):
        """Unplug self if object is cleaned up"""
        self.UnPlug()

    def PlugIn(self):
        """Obtain next available controller id and plug in to Virtual USB Bus"""
        self.id = Controller.available_ids.pop(0)
        Controller.unavailable_ids.append(self.id)
        xinput.PlugIn(c_uint(self.id))
        print('This ID:', self.id)
        print('Available:', Controller.available_ids)

    def UnPlug(self, force=False):
        """Unplug controller from Virtual USB Bus and free up ID"""
        if force:
            xinput.UnPlugForce(c_uint(self.id))
        else:
            xinput.UnPlug(c_uint(self.id))

        Controller.unavailable_ids.remove(self.id)
        Controller.available_ids.append(self.id)
        Controller.available_ids = sorted(Controller.available_ids)
        print('Available:', Controller.available_ids)

    def SetValue(self, control, value=None):
        """Set a value on the controller
        All controls will accept a value between -1.0 and 1.0

        Control List:
            AxisRx      , Right Stick X-Axis
            AxisRy      , Right Stick Y-Axis
            AxisX       , Left Stick X-Axis
            AxisY       , Left Stick Y-Axis
            BtnA        , A Button
            BtnB        , B Button
            BtnX        , X Button
            BtnY        , Y Button
            BtnBack     , Menu Button
            BtnStart    , Start Button
            BtnLB       , Left Bumper
            BtnRB       , Right Bumper
            BtnLT       , Left Trigger (Same as TriggerL = 1)
            BtnRT       , Right Trigeer (Same as TriggerR = 1)
            DpadOff     , Clear Dpad value
            DpadUp      , Clear Dpad and Set Up
            DpadDown    , Clear Dpad and Set Down
            DpadLeft    , Clear Dpad and Set Left
            DpadRight   , Clear Dpad and Set Right
            DpadInt     , Set custom Dpad; refer DPAD contants

        """
        func = getattr(xinput, 'Set' + control)

        if 'Dpad' in control and control != 'DpadInt':
            target_type = c_byte
            func(c_uint(self.id))
        else:
            if 'Axis' in control:
                target_type = c_short
                target_value = int(32767 * value)
            elif 'Btn' in control:
                target_type = c_bool
                target_value = bool(value)
            elif 'Trigger' in control:
                target_type = c_byte
                target_value = int(255 * value)
            elif 'DpadInt' in control:
                target_type = c_int
                target_value = int(value)

            func(c_uint(self.id), target_type(target_value))


def main():
    import time
    con = Controller()
    time.sleep(1)
    con.SetValue('BtnA', 1)
    time.sleep(10)
    con.SetValue('BtnA', 0)
    time.sleep(5)


if __name__ == '__main__':
    main()
