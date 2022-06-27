# Code by Daniel Kukiela (https://twitter.com/daniel_kukiela)

import ctypes
from threading import Thread
from time import time, sleep
from queue import Queue


# main keys class
class Keys(object):

    common = None
    standalone = False

    # instance of worker class
    keys_worker = None
    keys_process = None

    # key constants
    direct_keys      = 0x0008
    virtual_keys     = 0x0000
    key_press        = 0x0000
    key_release      = 0x0002

    # mouse constants
    mouse_move       = 0x0001
    mouse_lb_press   = 0x0002
    mouse_lb_release = 0x0004
    mouse_rb_press   = 0x0008
    mouse_rb_release = 0x0010
    mouse_mb_press   = 0x0020
    mouse_mb_release = 0x0040

    # direct keys
    dk = {
        "1":            0x02,
        "2":            0x03,
        "3":            0x04,
        "4":            0x05,
        "5":            0x06,
        "6":            0x07,
        "7":            0x08,
        "8":            0x09,
        "9":            0x0A,
        "0":            0x0B,

        "NUMPAD1":      0x4F,       "NP1":      0x4F,
        "NUMPAD2":      0x50,       "NP2":      0x50,
        "NUMPAD3":      0x51,       "NP3":      0x51,
        "NUMPAD4":      0x4B,       "NP4":      0x4B,
        "NUMPAD5":      0x4C,       "NP5":      0x4C,
        "NUMPAD6":      0x4D,       "NP6":      0x4D,
        "NUMPAD7":      0x47,       "NP7":      0x47,
        "NUMPAD8":      0x48,       "NP8":      0x48,
        "NUMPAD9":      0x49,       "NP9":      0x49,
        "NUMPAD0":      0x52,       "NP0":      0x52,
        "DIVIDE":       0xB5,       "NPDV":     0xB5,
        "MULTIPLY":     0x37,       "NPM":      0x37,
        "SUBSTRACT":    0x4A,       "NPS":      0x4A,
        "ADD":          0x4E,       "NPA":      0x4E,
        "DECIMAL":      0x53,       "NPDC":     0x53,
        "NUMPADENTER":  0x9C,       "NPE":      0x9C,

        "A":            0x1E,
        "B":            0x30,
        "C":            0x2E,
        "D":            0x20,
        "E":            0x12,
        "F":            0x21,
        "G":            0x22,
        "H":            0x23,
        "I":            0x17,
        "J":            0x24,
        "K":            0x25,
        "L":            0x26,
        "M":            0x32,
        "N":            0x31,
        "O":            0x18,
        "P":            0x19,
        "Q":            0x10,
        "R":            0x13,
        "S":            0x1F,
        "T":            0x14,
        "U":            0x16,
        "V":            0x2F,
        "W":            0x11,
        "X":            0x2D,
        "Y":            0x15,
        "Z":            0x2C,

        "F1":           0x3B,
        "F2":           0x3C,
        "F3":           0x3D,
        "F4":           0x3E,
        "F5":           0x3F,
        "F6":           0x40,
        "F7":           0x41,
        "F8":           0x42,
        "F9":           0x43,
        "F10":          0x44,
        "F11":          0x57,
        "F12":          0x58,

        "UP":           0xC8,
        "LEFT":         0xCB,
        "RIGHT":        0xCD,
        "DOWN":         0xD0,

        "ESC":          0x01,
        "SPACE":        0x39,       "SPC":      0x39,
        "RETURN":       0x1C,       "ENT":      0x1C,
        "INSERT":       0xD2,       "INS":      0xD2,
        "DELETE":       0xD3,       "DEL":      0xD3,
        "HOME":         0xC7,
        "END":          0xCF,
        "PRIOR":        0xC9,       "PGUP":     0xC9,
        "NEXT":         0xD1,       "PGDN":     0xD1,
        "BACK":         0x0E,
        "TAB":          0x0F,
        "LCONTROL":     0x1D,       "LCTRL":    0x1D,
        "RCONTROL":     0x9D,       "RCTRL":    0x9D,
        "LSHIFT":       0x2A,       "LSH":      0x2A,
        "RSHIFT":       0x36,       "RSH":      0x36,
        "LMENU":        0x38,       "LALT":     0x38,
        "RMENU":        0xB8,       "RALT":     0xB8,
        "LWIN":         0xDB,
        "RWIN":         0xDC,
        "APPS":         0xDD,
        "CAPITAL":      0x3A,       "CAPS":     0x3A,
        "NUMLOCK":      0x45,       "NUM":      0x45,
        "SCROLL":       0x46,       "SCR":      0x46,

        "MINUS":        0x0C,       "MIN":      0x0C,
        "LBRACKET":     0x1A,       "LBR":      0x1A,
        "RBRACKET":     0x1B,       "RBR":      0x1B,
        "SEMICOLON":    0x27,       "SEM":      0x27,
        "APOSTROPHE":   0x28,       "APO":      0x28,
        "GRAVE":        0x29,       "GRA":      0x29,
        "BACKSLASH":    0x2B,       "BSL":      0x2B,
        "COMMA":        0x33,       "COM":      0x33,
        "PERIOD":       0x34,       "PER":      0x34,
        "SLASH":        0x35,       "SLA":      0x35,
    }

    # virtual keys
    vk = {
        "1":            0x31,
        "2":            0x32,
        "3":            0x33,
        "4":            0x34,
        "5":            0x35,
        "6":            0x36,
        "7":            0x37,
        "8":            0x38,
        "9":            0x39,
        "0":            0x30,

        "NUMPAD1":      0x61,       "NP1":      0x61,
        "NUMPAD2":      0x62,       "NP2":      0x62,
        "NUMPAD3":      0x63,       "NP3":      0x63,
        "NUMPAD4":      0x64,       "NP4":      0x64,
        "NUMPAD5":      0x65,       "NP5":      0x65,
        "NUMPAD6":      0x66,       "NP6":      0x66,
        "NUMPAD7":      0x67,       "NP7":      0x67,
        "NUMPAD8":      0x68,       "NP8":      0x68,
        "NUMPAD9":      0x69,       "NP9":      0x69,
        "NUMPAD0":      0x60,       "NP0":      0x60,
        "DIVIDE":       0x6F,       "NPDV":     0x6F,
        "MULTIPLY":     0x6A,       "NPM":      0x6A,
        "SUBSTRACT":    0x6D,       "NPS":      0x6D,
        "ADD":          0x6B,       "NPA":      0x6B,
        "DECIMAL":      0x6E,       "NPDC":     0x6E,
        "NUMPADENTER":  0x0D,       "NPE":      0x0D,

        "A":            0x41,
        "B":            0x42,
        "C":            0x43,
        "D":            0x44,
        "E":            0x45,
        "F":            0x46,
        "G":            0x47,
        "H":            0x48,
        "I":            0x49,
        "J":            0x4A,
        "K":            0x4B,
        "L":            0x4C,
        "M":            0x4D,
        "N":            0x4E,
        "O":            0x4F,
        "P":            0x50,
        "Q":            0x51,
        "R":            0x52,
        "S":            0x53,
        "T":            0x54,
        "U":            0x55,
        "V":            0x56,
        "W":            0x57,
        "X":            0x58,
        "Y":            0x59,
        "Z":            0x5A,

        "F1":           0x70,
        "F2":           0x71,
        "F3":           0x72,
        "F4":           0x73,
        "F5":           0x74,
        "F6":           0x75,
        "F7":           0x76,
        "F8":           0x77,
        "F9":           0x78,
        "F10":          0x79,
        "F11":          0x7A,
        "F12":          0x7B,

        "UP":           0x26,
        "LEFT":         0x25,
        "RIGHT":        0x27,
        "DOWN":         0x28,

        "ESC":          0x1B,
        "SPACE":        0x20,       "SPC":      0x20,
        "RETURN":       0x0D,       "ENT":      0x0D,
        "INSERT":       0x2D,       "INS":      0x2D,
        "DELETE":       0x2E,       "DEL":      0x2E,
        "HOME":         0x24,
        "END":          0x23,
        "PRIOR":        0x21,       "PGUP":     0x21,
        "NEXT":         0x22,       "PGDN":     0x22,
        "BACK":         0x08,
        "TAB":          0x09,
        "LCONTROL":     0xA2,       "LCTRL":    0xA2,
        "RCONTROL":     0xA3,       "RCTRL":    0xA3,
        "LSHIFT":       0xA0,       "LSH":      0xA0,
        "RSHIFT":       0xA1,       "RSH":      0xA1,
        "LMENU":        0xA4,       "LALT":     0xA4,
        "RMENU":        0xA5,       "RALT":     0xA5,
        "LWIN":         0x5B,
        "RWIN":         0x5C,
        "APPS":         0x5D,
        "CAPITAL":      0x14,       "CAPS":     0x14,
        "NUMLOCK":      0x90,       "NUM":      0x90,
        "SCROLL":       0x91,       "SCR":      0x91,

        "MINUS":        0xBD,       "MIN":      0xBD,
        "LBRACKET":     0xDB,       "LBR":      0xDB,
        "RBRACKET":     0xDD,       "RBR":      0xDD,
        "SEMICOLON":    0xBA,       "SEM":      0xBA,
        "APOSTROPHE":   0xDE,       "APO":      0xDE,
        "GRAVE":        0xC0,       "GRA":      0xC0,
        "BACKSLASH":    0xDC,       "BSL":      0xDC,
        "COMMA":        0xBC,       "COM":      0xBC,
        "PERIOD":       0xBE,       "PER":      0xBE,
        "SLASH":        0xBF,       "SLA":      0xBF,
    }

    # setup object
    def __init__(self, common = None):
        self.keys_worker = KeysWorker(self)
        # Thread(target=self.keys_worker.processQueue).start()
        self.common = common
        if common is None:
            self.standalone = True

    # parses keys string and adds keys to the queue
    def parseKeyString(self, string):

        # print keys
        if not self.standalone:
            self.common.info("Processing keys: %s" % string)

        key_queue = []
        errors = []

        # defaults to direct keys
        key_type = self.direct_keys

        # split by comma
        keys = string.upper().split(",")

        # translate
        for key in keys:

            # up, down or stroke?
            up = True
            down = True
            direction = key.split("_")
            subkey = direction[0]
            if len(direction) >= 2:
                if direction[1] == 'UP':
                    down = False
                else:
                    up = False

            # switch to virtual keys
            if subkey == "VK":
                key_type = self.virtual_keys

            # switch to direct keys
            elif subkey == "DK":
                key_type = self.direct_keys

            # key code
            elif subkey.startswith("0x"):
                subkey = int(subkey, 16)
                if subkey > 0 and subkey < 256:
                    key_queue.append({
                        "key":  int(subkey),
                        "okey": subkey,
                        "time": 0,
                        "up":   up,
                        "down": down,
                        "type": key_type,
                    })
                else:
                    errors.append(key)

            # pause
            elif subkey.startswith("-"):
                time = float(subkey.replace("-", ""))/1000
                if time > 0 and time <= 10:
                    key_queue.append({
                        "key":  None,
                        "okey": "",
                        "time": time,
                        "up":   False,
                        "down": False,
                        "type": None,
                    })
                else:
                    errors.append(key)

            # direct key
            elif key_type == self.direct_keys and subkey in self.dk:
                key_queue.append({
                    "key":  self.dk[subkey],
                    "okey": subkey,
                    "time": 0,
                    "up":   up,
                    "down": down,
                    "type": key_type,
                })

            # virtual key
            elif key_type == self.virtual_keys and subkey in self.vk:
                key_queue.append({
                    "key":  self.vk[subkey],
                    "okey": subkey,
                    "time": 0,
                    "up":   up,
                    "down": down,
                    "type": key_type,
                })

            # no match?
            else:
                errors.append(key)

        # if there are errors, do not process keys
        if len(errors):
            return errors

        # create new thread if there is no active one
        if self.keys_process is None or not self.keys_process.isAlive():
            self.keys_process = Thread(target=self.keys_worker.processQueue)
            self.keys_process.start()

        # add keys to queue
        for i in key_queue:
            self.keys_worker.key_queue.put(i)
        self.keys_worker.key_queue.put(None)

        return True

    # direct key press
    def directKey(self, key, direction = None, type = None):
        if type is None:
            type = self.direct_keys
        if direction is None:
            direction = self.key_press
        if key.startswith("0x"):
            key = int(key, 16)
        else:
            key = key.upper()
            lookup_table = self.dk if type == self.direct_keys else self.vk
            key = lookup_table[key] if key in lookup_table else 0x0000

        self.keys_worker.sendKey(key, direction | type)

    # direct mouse move or button press
    def directMouse(self, dx = 0, dy = 0, buttons = 0):
        self.keys_worker.sendMouse(dx, dy, buttons)


# threaded sending keys class
class KeysWorker():

    # keys object
    keys = None

    # queue of keys
    key_queue = Queue()

    # init
    def __init__(self, keys):
        self.keys = keys

    # main function, process key's queue in loop
    def processQueue(self):

        # endless loop
        while True:

            # get one key
            key = self.key_queue.get()

            # terminate process if queue is empty
            if key is None:
                self.key_queue.task_done()
                if self.key_queue.empty():
                    return
                continue
            # print key
            elif not self.keys.standalone:
                self.keys.common.info("Key: \033[1;35m%s/%s\033[0;37m, duration: \033[1;35m%f\033[0;37m, direction: \033[1;35m%s\033[0;37m, type: \033[1;35m%s" % (
                    key["okey"] if key["okey"] else "None",
                    key["key"], key["time"],
                    "UP" if key["up"] and not key["down"] else "DOWN" if not key["up"] and key["down"] else "BOTH" if key["up"] and key["down"] else "NONE",
                    "None" if key["type"] is None else "DK" if key["type"] == self.keys.direct_keys else "VK"), "\033[0;35mKEY:    \033[0;37m"
                )

            # if it's a key
            if key["key"]:

                # press
                if key["down"]:
                    self.sendKey(key["key"], self.keys.key_press | key["type"])

                # wait
                sleep(key["time"])

                # and release
                if key["up"]:
                    self.sendKey(key["key"], self.keys.key_release | key["type"])

            # not an actual key, just pause
            else:
                sleep(key["time"])

            # mark as done (decrement internal queue counter)
            self.key_queue.task_done()

    # send key
    def sendKey(self, key, type):
        self.SendInput(self.Keyboard(key, type))

    # send mouse
    def sendMouse(self, dx, dy, buttons):
        if dx != 0 or dy != 0:
            buttons |= self.keys.mouse_move
        self.SendInput(self.Mouse(buttons, dx, dy))

    # send input
    def SendInput(self, *inputs):
        nInputs = len(inputs)
        LPINPUT = INPUT * nInputs
        pInputs = LPINPUT(*inputs)
        cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
        return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

    # get input object
    def Input(self, structure):
        if isinstance(structure, MOUSEINPUT):
            return INPUT(0, _INPUTunion(mi=structure))
        if isinstance(structure, KEYBDINPUT):
            return INPUT(1, _INPUTunion(ki=structure))
        if isinstance(structure, HARDWAREINPUT):
            return INPUT(2, _INPUTunion(hi=structure))
        raise TypeError('Cannot create INPUT structure!')

    # mouse input
    def MouseInput(self, flags, x, y, data):
        return MOUSEINPUT(x, y, data, flags, 0, None)

    # keyboard input
    def KeybdInput(self, code, flags):
        return KEYBDINPUT(code, code, flags, 0, None)

    # hardware input
    def HardwareInput(self, message, parameter):
        return HARDWAREINPUT(message & 0xFFFFFFFF,
                             parameter & 0xFFFF,
                             parameter >> 16 & 0xFFFF)

    # mouse object
    def Mouse(self, flags, x=0, y=0, data=0):
        return self.Input(self.MouseInput(flags, x, y, data))

    # keyboard object
    def Keyboard(self, code, flags=0):
        return self.Input(self.KeybdInput(code, flags))

    # hardware object
    def Hardware(self, message, parameter=0):
        return self.Input(self.HardwareInput(message, parameter))


# types
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))



#example:
if __name__ == '__main__':
    sleep(3)
    keys = Keys()

    # mouse movement
    for i in range(100):
        keys.directMouse(-1*i, 0)
        sleep(0.004)

    # mouse keys
    keys.directMouse(buttons=keys.mouse_rb_press)
    sleep(0.5)
    keys.directMouse(buttons=keys.mouse_lb_press)
    sleep(2)
    keys.directMouse(buttons=keys.mouse_lb_release)
    sleep(0.5)
    keys.directMouse(buttons=keys.mouse_rb_release)
    
    # or
    keys.directMouse(buttons=keys.mouse_lb_press | keys.mouse_rb_press)
    sleep(2)
    keys.directMouse(buttons=keys.mouse_lb_release | keys.mouse_rb_release)
    
    # keyboard (direct keys)
    keys.directKey("a")
    sleep(0.04)
    keys.directKey("a", keys.key_release)
    
    # keyboard (virtual keys)
    keys.directKey("a", type=keys.virtual_keys)
    sleep(0.04)
    keys.directKey("a", keys.key_release, keys.virtual_keys)
    
    # queue of keys (direct keys, threaded, only for keybord input)
    keys.parseKeyString("a_down,-4,a_up,0x01")  # -4 - pause for 4 ms, 0x00 - hex code of Esc
    
    # queue of keys (virtual keys, threaded, only for keybord input)
    keys.parseKeyString("vk,a_down,-4,a_up")  # -4 - pause for 4 ms

