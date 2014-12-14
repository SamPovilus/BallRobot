#import Adafruit_BBIO.PWM as motor
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
    def __init__(self, pwmPort, invertPortNumber, inverted,motorNumber,freq,filterDepth = 10):
        print "Motor thread started"
        self.myInvertPort = InvertPort.InvertPort(invertPortNumber)
        self.pastSpeeds =  collections.deque(maxlen=filterDepth)
        #motor.start(pwmPort,50,freq,inverted)
        super(Motor, self).__init__()
        self.daemon = True

    def set_speed(self,speed):
        self.myDesiredSpeed = speed

    def run(self):
        while 1:
            #TODO: better filter design
            self.pastSpeeds.append(self.myDesiredSpeed)
            currentSpeed = numpy.mean(self.pastSpeeds)
            print currentSpeed
            if(currentSpeed < 0.0):
                self.myInvertPort.invert()
            else:
                self.myInvertPort.not_invert()
            sleep(0.02)
