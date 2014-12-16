from Adafruit_I2C import Adafruit_I2C as I2C
import threading
from time import sleep

class ReadIMU(threading.Thread):
    myACC = None
    myGyro = None
    myPeriod = None
    def __init__(self,ACCAddress,GyroAddress,period=0.02):
        print "IMU thread started"
        self.myACC = I2C(ACCAddress)
        #initalize acceleromoeter
        self.myACC.write8(0x31,0xB)
        self.myACC.write8(0x2d,0x8)
        self.myACC.write8(0x2e,0x80)
        self.myPeriod=period
	super(ReadIMU, self).__init__()
        self.daemon = True

    def run(self):
	while 1:
            lowerACCBits = self.myACC.readU8(0x32)
            upperACCBits = self.myACC.readU8(0x33)
            accVal = (upperACCBits << 8) + lowerACCBits
            print(accVal)
            sleep(self.myPeriod)
