import Adafruit_BBIO.PWM as PWMoutput
import Queue
from time import sleep
import threading
import collections
import numpy
import InvertPort

class Motor(threading.Thread):
    pastSpeeds = None
    myDesiredSpeed = 0
    myInvertPort = None
    myPWMPort = None
    def __init__(self, pwmPort, invertPortNumber, inverted,motorNumber,freq,filterDepth = 10):
        print "Motor thread started" + str(type(invertPortNumber))
        self.myInvertPort = InvertPort.InvertPort(str(invertPortNumber))
        self.pastSpeeds =  collections.deque(maxlen=filterDepth)
        self.myPWMPort = pwmPort
        PWMoutput.start(self.myPWMPort,50,freq,inverted)
        super(Motor, self).__init__()
        self.daemon = True

    def set_speed(self,speed):
        self.myDesiredSpeed = speed

    def run(self):
        while 1:
            #TODO: better filter design
            self.pastSpeeds.append(self.myDesiredSpeed)
            currentSpeed = numpy.mean(self.pastSpeeds)
            if(abs(currentSpeed)):
              print "ERROR current speed out of range" + str(currentSpeed)
              currentSpeed=0
            print currentSpeed
            PWMoutput.set_duty_cycle(self.myPWMPort,abs(currentSpeed))
            if(currentSpeed < 0.0):
                self.myInvertPort.invert()
            else:
                self.myInvertPort.not_invert()
            sleep(0.02)
