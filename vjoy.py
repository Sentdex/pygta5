# step 1: https://sourceforge.net/projects/vjoystick/files/latest/download
# step 2: SDK: http://vjoystick.sourceforge.net/site/index.php/component/weblinks/weblink/13-uncategorised/11-redirect-vjoy2sdk?task=weblink.go
# step 3: CONST_DLL_VJOY = "vJoyInterface.dll" ...KEEP .DLL local? 
# step 4: http://www.x360ce.com/, 64 bit download
# step 5: extract, copy to gtav directory
# step 6: run, should auto-detect vjoy, test with example make sure it works.
# step 7: CLOSE the app, run game. Test with example to see if works. 


import ctypes
import struct, time
import numpy as np

CONST_DLL_VJOY = "vJoyInterface.dll"

class vJoy(object):
    def __init__(self, reference = 1):
        self.handle = None
        self.dll = ctypes.CDLL( CONST_DLL_VJOY )
        self.reference = reference
        self.acquired = False
        
    def open(self):
        if self.dll.AcquireVJD( self.reference ):
            self.acquired = True
            return True
        return False
    def close(self):
        if self.dll.RelinquishVJD( self.reference ):
            self.acquired = False
            return True
        return False
    def generateJoystickPosition(self, 
        wThrottle = 0, wRudder = 0, wAileron = 0, 
        wAxisX = 0, wAxisY = 0, wAxisZ = 0,
        wAxisXRot = 0, wAxisYRot = 0, wAxisZRot = 0,
        wSlider = 0, wDial = 0, wWheel = 0,
        wAxisVX = 0, wAxisVY = 0, wAxisVZ = 0,
        wAxisVBRX = 0, wAxisVBRY = 0, wAxisVBRZ = 0,
        lButtons = 0, bHats = 0, bHatsEx1 = 0, bHatsEx2 = 0, bHatsEx3 = 0):
        """
        typedef struct _JOYSTICK_POSITION
        {
            BYTE    bDevice; // Index of device. 1-based
            LONG    wThrottle;
            LONG    wRudder;
            LONG    wAileron;
            LONG    wAxisX;
            LONG    wAxisY;
            LONG    wAxisZ;
            LONG    wAxisXRot;
            LONG    wAxisYRot;
            LONG    wAxisZRot;
            LONG    wSlider;
            LONG    wDial;
            LONG    wWheel;
            LONG    wAxisVX;
            LONG    wAxisVY;
            LONG    wAxisVZ;
            LONG    wAxisVBRX;
            LONG    wAxisVBRY;
            LONG    wAxisVBRZ;
            LONG    lButtons;   // 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
            DWORD   bHats;      // Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
                        DWORD   bHatsEx1;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx2;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx3;   // 16-bit of continuous HAT switch
        } JOYSTICK_POSITION, *PJOYSTICK_POSITION;
        """
        joyPosFormat = "BlllllllllllllllllllIIII"
        pos = struct.pack( joyPosFormat, self.reference, wThrottle, wRudder,
                                   wAileron, wAxisX, wAxisY, wAxisZ, wAxisXRot, wAxisYRot,
                                   wAxisZRot, wSlider, wDial, wWheel, wAxisVX, wAxisVY, wAxisVZ,
                                   wAxisVBRX, wAxisVBRY, wAxisVBRZ, lButtons, bHats, bHatsEx1, bHatsEx2, bHatsEx3 )
        return pos
    def update(self, joystickPosition):
        if self.dll.UpdateVJD( self.reference, joystickPosition ):
            return True
        return False
    #Not working, send buttons one by one
    def sendButtons( self, bState ):
        joyPosition = self.generateJoystickPosition( lButtons = bState )
        return self.update( joyPosition )
    def setButton( self, index, state ):
        if self.dll.SetBtn( state, self.reference, index ):
            return True
        return False
                

vj = vJoy()

# valueX, valueY between -1.0 and 1.0
# scale between 0 and 16000
def setJoy(valueX, valueY, scale):
    xPos = int(valueX*scale)
    yPos = int(valueY*scale)
    joystickPosition = vj.generateJoystickPosition(wAxisX = 16000+xPos, wAxisY = 16000+yPos)
    vj.update(joystickPosition)


def test():
    vj.open()
    print("vj opening", flush=True)
    btn = 1
    time.sleep(2)
    print("sending axes", flush=True)
    for i in range(0,1000,1):
        #vj.sendButtons( btn << i )
        xPos = int(10000.0*np.sin(2.0*np.pi*i/1000))
        yPos = int(10000.0*np.sin(2.0*np.pi*i/100))
        print(xPos, flush=True)
        joystickPosition = vj.generateJoystickPosition(wAxisX = 16000+xPos, wAxisY = 16000+yPos)
        vj.update(joystickPosition)
        time.sleep( 0.01 )
    joystickPosition = vj.generateJoystickPosition(wAxisX = 16000, wAxisY = 16000)
    vj.update(joystickPosition)
    vj.sendButtons(0)
    print("vj closing", flush=True)
    vj.close()


if __name__ == '__main__':
    test()

