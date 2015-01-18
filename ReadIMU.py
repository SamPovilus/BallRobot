try:
    from Adafruit_I2C import Adafruit_I2C as I2C
except ImportError:
    print "*************** Using stubbed I2C ***************"
    from I2CStubs import I2CStubs as I2C
    
import threading
from time import sleep
import Queue
import struct
import Globals

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

    xOverride = 0
    yOverride = 0
    zOverride = 0

    xOverrideAxis = False
    yOverrideAxis = False
    zOverrideAxis = False


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
            if(self.xOverrideAxis == False):
                accValX = self.getAxis(0)
            else:
                accValX = self.xOverride
            if(self.yOverrideAxis == False):
                accValY = self.getAxis(1)
            else:
                accValY = self.yOverride
            if(self.zOverrideAxis == False):
                accValZ = self.getAxis(2)
            else:
                accValZ = self.zOverride
                
            self.myXQueue.put(accValX/self.myMaxIMUVal)
            self.myYQueue.put(accValY/self.myMaxIMUVal)
            self.myTelemQueue.put(struct.pack('>LLfff',0xdeadbeef,Globals.IMU_ID_ACC+Globals.IMU_NOTIFICATION_OFFSET,(accValX/self.myMaxIMUVal),(accValY/self.myMaxIMUVal),(accValZ/self.myMaxIMUVal)))
            self.myNotificationQueue.put(Globals.IMU_ID_ACC+Globals.IMU_NOTIFICATION_OFFSET)
            if(self.myDebug):
                print " ReadIMU X: " + '%10f' % (accValX/self.myMaxIMUVal) + " Y: " + '%10f' % (accValY/self.myMaxIMUVal) + " Z: " +  '%10f' % (accValZ/self.myMaxIMUVal)
            sleep(self.myPeriod)

    def twos_comp(self,val, bits):
        """compute the 2's compliment of int value val"""
        if( (val&(1<<(bits-1))) != 0 ):
            val = val - (1<<bits)
        return val

    def getAxis(self,axis):
        lowerACCBits = self.myACC.readU8(0x32 + axis*2)
        upperACCBits = self.myACC.readU8(0x33 + axis*2)
        accVal = (upperACCBits << 8) + lowerACCBits
        accVal = self.twos_comp(accVal,16)
        return accVal

    def setOverrideValues(self,x,y,z):
        print "Values x: " + str(x) + " y: " +  str(y) + " z: " + str(z)
        self.xOverride = x
        self.yOverride = y
        self.zOverride = z

    def setOverrideAxis(self,x,y,z):
        if(x):
            print "overriding x"
        if(y):
            print "overriding y"
        if(z):
            print "pverriding z"    

        self.xOverrideAxis = x
        self.yOverrideAxis = y
        self.zOverrideAxis = z
        
    def setAccDivisor(self,divisor):
        self.myMaxIMUVal = divisor
