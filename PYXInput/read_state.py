import ctypes

buttons = {
    'DPAD_UP': 0x0001,
    'DPAD_DOWN': 0x0002,
    'DPAD_LEFT': 0x0004,
    'DPAD_RIGHT': 0x0008,
    'START': 0x0010,
    'BACK': 0x0020,
    'LEFT_THUMB': 0x0040,
    'RIGHT_THUMB': 0x0080,
    'LEFT_SHOULDER': 0x0100,
    'RIGHT_SHOULDER': 0x0200,
    'A': 0x1000,
    'B': 0x2000,
    'X': 0x4000,
    'Y': 0x8000
}

xinput = ctypes.windll.xinput1_4


class xinput_gamepad(ctypes.Structure):
    _fields_ = [("wButtons", ctypes.c_ushort), ("left_trigger", ctypes.c_ubyte),
                ("right_trigger", ctypes.c_ubyte), ("thumb_lx", ctypes.c_short),
                ("thumb_ly", ctypes.c_short), ("thumb_rx", ctypes.c_short),
                ("thumb_ry", ctypes.c_short)]


class xinput_state(ctypes.Structure):
    _fields_ = [("dwPacketNumber", ctypes.c_uint),
                ("XINPUT_GAMEPAD", xinput_gamepad)]


class xinput_vibration(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]


def get_state(ControllerID):
    state = xinput_state()
    xinput.XInputGetState(ControllerID - 1, ctypes.pointer(state))
    return state


def button_to_dict(state_value):
    return([name for name, value in buttons.items()
            if state_value & value == value])


def main():
    con = get_state(1)

    print(button_to_dict(con.XINPUT_GAMEPAD.wButtons))


if __name__ == '__main__':
    main()
