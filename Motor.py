import Adafruit_BBIO.PWM as PWMoutput
from time import sleep
import threading
import collections
import numpy
import InvertPort
import Queue
import Struct


class Motor(threading.Thread):
    pastSpeeds = None
    myMotorNumber = None
    myDesiredSpeed = 0
    myInvertPort = None
    myPWMPort = None
    myPeriod = None
    myDirInverted = None
    myMotorDeadband = 0.0
    myDebug = None
    myTelemQueue = None
    myNotificationQueue = None

    def __init__(self, pwmPort, invertPortNumber, inverted, motorNumber, PWMFreq, telemQueue, notifcationQueue ,period=0.02,filterDepth = 10, debug=False):
        self.myMotorNumber = motorNumber
	print "Motor " + str(self.myMotorNumber) + " thread started"
        self.myInvertPort = InvertPort.InvertPort(str(invertPortNumber),debug)
        self.pastSpeeds =  collections.deque(maxlen=filterDepth)
        self.myPWMPort = pwmPort
        PWMoutput.start(self.myPWMPort,50,PWMFreq,inverted)
        super(Motor, self).__init__()
        self.daemon = True 
        self.myPeriod=period
        self.myDebug = debug
	self.myTelemQueue = telemQueue
	self.myNotificationQueue = notificationQueue
	if dirInverted:
	    self.myDirInverted = -1
	else:
            self.myDirInverted = 1
    def set_speed(self,speed):
        #from open office f(x) =  - 58.2750582751x^4 + 221.8337218337x^3 - 321.3286713287x^2 + 258.7140637141x - 0.8391608392
        #self.myDesiredSpeed = (speed*(100.0-self.myMotorDeadband))
        self.myDesiredSpeed = -58.2750582751*(speed**4) + 221.8337218337*(speed**3) - 321.3286713287*(speed**2) + 258.7140637141*speed - 0.8391608392
        self.myTelemQueue.put(Struct.pack('\f\f\l\l',self.myDesiredSpeed,float(speed),\xdeadbeef,\xdeadbeef))
        self.myNotificationQueue.put(self.myMotorNumber+MOTOR_NOTIFICATION_OFFSET)
        
    def run(self):
        while 1:
            #TODO: better filter design
            self.pastSpeeds.append(self.myDesiredSpeed)
#            currentSpeed = numpy.mean(self.pastSpeeds)
            currentSpeed = self.myDesiredSpeed
            if(abs(currentSpeed)>100.0):
              print "ERROR current speed out of range" + str(currentSpeed)
              currentSpeed=0
            if(abs(currentSpeed)>5.0):
                PWMoutput.set_duty_cycle(self.myPWMPort,abs(currentSpeed)+self.myMotorDeadband)
            if(currentSpeed < 0.0):
                self.myInvertPort.invert()
            else:
                self.myInvertPort.not_invert()
            if(self.myDebug):
                print "Motor: " + str(self.myMotorNumber) + " current speed: " + '%+10f' % currentSpeed
            sleep(self.myPeriod)
