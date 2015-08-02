import datetime
import collections
import numpy

class PID():
    myP = 1.0
    myD = 1.0
    myI = 1.0

    gyro = 0.0
    acc = 0.0

    lastGyro = 0.0
    lastAcc = 0.0

    dGyro = 0.0
    dAcc = 0.0

    lasttime = 0

    times = None
    cycleCount = 0
    
    def __init__(self):
        self.times = collections.deque(maxlen=100) 
    
    def set_PID(self,P,I,D):
        self.myP = P;
        self.myI = I;
        self.myD = D;


    def process(self, acc, gyro):
        self.cycleCount = self.cycleCount + 1
        ms = datetime.datetime.now().microsecond
        self.times.append(ms-self.lasttime)
        if(self.cycleCount%100 == 0):
            print numpy.mean(self.times)
            print self.times
        self.lasttime = ms
        self.lastGyro = gyro
        self.dGyro = gyro - self.lastGyro

        self.lastAcc = acc
        self.dAcc = acc - self.lastAcc

        return self.myP * acc + self.myD * gyro
