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
    myXAccQueue = None
    myYAccQueue = None
    myXGyroQueue = None
    myYGyroQueue = None
    myMaxAccVal = None
    myMaxGyroVal = None
    myDebug = None
    myTelemQueue = None
    myNotificationQueue = None

    xOverride = 0
    yOverride = 0
    zOverride = 0

    xOverrideAxisAcc = False
    yOverrideAxisAcc = False
    zOverrideAxisAcc = False

    xOverrideAxisGyro = False
    yOverrideAxisGyro = False
    zOverrideAxisGyro = False

    accXFilter = None
    accYFilter = None
    gyroXFilter = None
    gyroYFilter = None
    
    def __init__(self,ACCAddress,GyroAddress,XAccQueue,YAccQueue,XGyroQueue,YGyroQueue,TlmQueue,NotificationQueue,period=0.02,maxAccVal=512.0,maxGyroVal=512.0,debug=False):
        print "IMU thread started"
        self.myACC = I2C(ACCAddress)
        #initalize acceleromoeter
        self.myACC.write8(0x31,0xB)
        self.myACC.write8(0x2d,0x8)
        self.myACC.write8(0x2e,0x80)
        self.myGyro = I2C(GyroAddress)
        
        self.myPeriod=period
	super(ReadIMU, self).__init__()
        self.daemon = True
        self.myXAccQueue = XAccQueue
        self.myYAccQueue = YAccQueue
        self.myXGyroQueue = XGyroQueue
        self.myYGyroQueue = YGyroQueue
	self.myMaxAccVal = maxAccVal
        self.myMaxGyroVal = maxGyroVal
        self.myDebug = debug
        self.myTelemQueue = TlmQueue
        self.myNotificationQueue = NotificationQueue

        #TODO define this better
        filterDepth = 10
        self.accXFilter =  collections.deque(maxlen=filterDepth)
        self.accYFilter =  collections.deque(maxlen=filterDepth)
        self.gyroXFilter =  collections.deque(maxlen=filterDepth)
        self.gyroYFilter =  collections.deque(maxlen=filterDepth)
        
    def run(self):
        loopCount = 0
	while 1:
#Acc
            if(self.xOverrideAxisAcc == False):
                accValX = self.getAxisAcc(0)
            else:
                accValX = self.xOverrideAcc
            if(self.yOverrideAxisAcc == False):
                accValY = self.getAxisAcc(1)
            else:
                accValY = self.yOverrideAcc
            if(self.zOverrideAxisAcc == False):
                accValZ = self.getAxisAcc(2)
            else:
                accValZ = self.zOverrideAcc

            self.accXFilter.append(accValX/self.myMaxAccVal)
            self.accYFilter.append(accValY/self.myMaxAccVal)
            xAccAvg = numpy.mean(self.accXFilter)
            yAccAvg = numpy.mean(self.accYFilter)
            self.myXAccQueue.put(xAccAvg)
            self.myYAccQueue.put(xAccAvg)
            self.myTelemQueue.put(struct.pack('>LLfff',0xdeadbeef,Globals.IMU_ID_ACC+Globals.IMU_NOTIFICATION_OFFSET,xAccAvg,yAccAvg,(accValZ/self.myMaxAccVal)))
            
            self.myNotificationQueue.put(Globals.IMU_ID_ACC+Globals.IMU_NOTIFICATION_OFFSET)

# Gyro
            if(self.xOverrideAxisGyro == False):
                gyroValX = self.getAxisGyro(0)
            else:
                gyroValX = self.xOverrideGyro
            if(self.yOverrideAxisGyro == False):
                gyroValY = self.getAxisGyro(1)
            else:
                gyroValY = self.yOverrideGyro
            if(self.zOverrideAxisGyro == False):
                gyroValZ = self.getAxisGyro(2)
            else:
                gyroValZ = self.zOverrideGyro

            self.myXGyroQueue.put(gyroValX/self.myMaxGyroVal)
            self.myYGyroQueue.put(gyroValY/self.myMaxGyroVal)
            self.myTelemQueue.put(struct.pack('>LLfff',0xdeadbeef,Globals.IMU_ID_GYRO+Globals.IMU_NOTIFICATION_OFFSET,(gyroValX/self.myMaxGyroVal),(gyroValY/self.myMaxGyroVal),(gyroValZ/self.myMaxGyroVal)))
            self.myNotificationQueue.put(Globals.IMU_ID_GYRO+Globals.IMU_NOTIFICATION_OFFSET)

            if(self.myDebug):
                print " ReadAcc X: " + '%10f' % (accValX/self.myMaxAccVal) + " Y: " + '%10f' % (accValY/self.myMaxAccVal) + " Z: " +  '%10f' % (accValZ/self.myMaxAccVal)
                print " ReadGyro X: " + '%10f' % (gyroValX/self.myMaxGyroVal) + " Y: " + '%10f' % (gyroValY/self.myMaxGyroVal) + " Z: " +  '%10f' % (gyroValZ/self.myMaxGyroVal)
            sleep(self.myPeriod)

    def twos_comp(self,val, bits):
        """compute the 2's compliment of int value val"""
        if( (val&(1<<(bits-1))) != 0 ):
            val = val - (1<<bits)
        return val

    def getAxisAcc(self,axis):
        lowerACCBits = self.myACC.readU8(0x32 + axis*2)
        upperACCBits = self.myACC.readU8(0x33 + axis*2)
        accVal = (upperACCBits << 8) + lowerACCBits
        accVal = self.twos_comp(accVal,16)
        return accVal

    def getAxisGyro(self,axis):
        upperGyroBits = self.myGyro.readU8(0x1d + axis*2)
        lowerGyroBits = self.myGyro.readU8(0x1e + axis*2)
        gyroVal = (upperGyroBits << 8) + lowerGyroBits
        gyroVal = self.twos_comp(gyroVal,16)
        return gyroVal

    def setOverrideValuesAcc(self,x,y,z):
        print "Acc override values x: " + str(x) + " y: " +  str(y) + " z: " + str(z)
        self.xOverrideAcc = x
        self.yOverrideAcc = y
        self.zOverrideAcc = z

    def setOverrideValuesGyro(self,x,y,z):
        print "Gyro override values x: " + str(x) + " y: " +  str(y) + " z: " + str(z)
        self.xOverrideGyro = x
        self.yOverrideGyro = y
        self.zOverrideGyro = z

    def setOverrideAxisAcc(self,x,y,z):
        if(x):
            print "overriding x acc"
        if(y):
            print "overriding y acc"
        if(z):
            print "overriding z acc"    

        self.xOverrideAxisAcc = x
        self.yOverrideAxisAcc = y
        self.zOverrideAxisAcc = z

    def setOverrideAxisGyro(self,x,y,z):
        if(x):
            print "overriding x gyro"
        if(y):
            print "overriding y gyro"
        if(z):
            print "overriding z gyro"    

        self.xOverrideAxisGyro = x
        self.yOverrideAxisGyro = y
        self.zOverrideAxisGyro = z

    def setAccDivisor(self,divisor):
        self.myMaxAccVal = divisor

    def setGyroDivisor(self,divisor):
        self.myMaxGyroVal = divisor
