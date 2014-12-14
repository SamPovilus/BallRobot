#import Adafruit_BBIO.PWM as motor
import Queue
from time import sleep
import threading

class Motor(threading.Thread):
    
    mySpeedsQueue = Queue.Queue(2)
    def __init__(self, port, inverted,motorNumber,freq):
        print "Motor thread started"
        #motor.start(port,50,freq,inverted)
        super(Motor, self).__init__()

    def set_speed(self,speed):
        self.mySpeedsQueue.put(speed)

    def run(self):
        while 1:
            if not self.mySpeedsQueue.empty():
                print "Speed set to: " + str(self.mySpeedsQueue.get())
                self.mySpeedsQueue.task_done()
            
            else:
                print "Speed not changed"
            sleep(0.5)
