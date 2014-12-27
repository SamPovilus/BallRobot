from Adafruit_I2C import Adafruit_I2C as I2C
import threading
from time import sleep
import Queue


class ReadIMU(threading.Thread):
    myACC = None
    myGyro = None
    myPeriod = None
    myXQueue = None
    myYQueue = None
    myMaxIMUVal = None
    myDebug = None
    myTelemQueue = None
    myNotificationQueue = None

    def __init__(self,ACCAddress,GyroAddress,XQueue,YQueue,TlmQueue,NotificationQueue,period=0.02,maxIMUVal=512.0,debug=False):
        print "IMU thread started"
        self.myACC = I2C(ACCAddress)
        #initalize acceleromoeter
        self.myACC.write8(0x31,0xB)
        self.myACC.write8(0x2d,0x8)
        self.myACC.write8(0x2e,0x80)
        self.myPeriod=period
	super(ReadIMU, self).__init__()
        self.daemon = True
        self.myXQueue = XQueue
        self.myYQueue = YQueue
	self.myMaxIMUVal = maxIMUVal
        self.myDebug = debug
        self.myTelemQueue = TlmQueue
        self.myNotificationQueue = NotificationQueue
        
    def run(self):
	while 1:
            lowerACCBitsX = self.myACC.readU8(0x32)
            upperACCBitsX = self.myACC.readU8(0x33)
            accValX = (upperACCBitsX << 8) + lowerACCBitsX
            accValX = self.twos_comp(accValX,16)
            lowerACCBitsY = self.myACC.readU8(0x34)
            upperACCBitsY = self.myACC.readU8(0x35)
            accValY = (upperACCBitsY << 8) + lowerACCBitsY
            accValY = self.twos_comp(accValY,16)
            lowerACCBitsZ = self.myACC.readU8(0x34)
            upperACCBitsZ = self.myACC.readU8(0x35)
            accValZ= (upperACCBitsZ << 8) + lowerACCBitsZ
            accValZ = self.twos_comp(accValZ,16)
            self.myXQueue.put(accValX/self.myMaxIMUVal)
            self.myYQueue.put(accValY/self.myMaxIMUVal)
            self.myTelemQueue.put(Struct.pack('\f\f\f\l\f',(accValX/self.myMaxIMUVal),(accValY/self.myMaxIMUVal),(accValZ/self.myMaxIMUVal),self.myMaxIMUVal))
            self.myNotificationQueue.put(IMU_ID_ACC+IMU_NOTIFICATION_OFFSET)
            if(self.myDebug):
                print "ReadIMU X: " + '%10f' % (accValX/self.myMaxIMUVal) + " Y: " + '%10f' % (accValY/self.myMaxIMUVal) + " Z: " +  '%10f' % (accValZ/self.myMaxIMUVal)
            sleep(self.myPeriod)

    def twos_comp(self,val, bits):
        """compute the 2's compliment of int value val"""
        if( (val&(1<<(bits-1))) != 0 ):
            val = val - (1<<bits)
        return val
