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
            lowerACCBitsX = self.myACC.readU8(0x32)
            upperACCBitsX = self.myACC.readU8(0x33)
            accValX = (upperACCBitsX << 8) + lowerACCBitsX
            lowerACCBitsY = self.myACC.readU8(0x34)
            upperACCBitsY = self.myACC.readU8(0x35)
            accValY = (upperACCBitsY << 8) + lowerACCBitsY
            lowerACCBitsZ = self.myACC.readU8(0x34)
            upperACCBitsZ = self.myACC.readU8(0x35)
            accValZ= (upperACCBitsZ << 8) + lowerACCBitsZ
            print "X: " + str(accValX) + " Y: " + str(accValY) + " Z: " + str(accValZ)
            sleep(self.myPeriod)
