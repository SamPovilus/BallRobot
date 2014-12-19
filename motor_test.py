import Motor
import ReadIMU
import TransformXYRotZToMotor
import Queue
from time import sleep

XQueue = Queue.Queue(maxsize=2)
YQueue = Queue.Queue(maxsize=2)

myMotor0 = Motor.Motor("P9_14","P9_12",True,0,5000,period = 0.02,filterDepth = 2)
myMotor1 = Motor.Motor("P9_22","P9_18",True,1,5000,period = 0.02,filterDepth = 2)
myMotor2 = Motor.Motor("P8_13","P8_11",True,2,5000,period = 0.02,filterDepth = 2)

myIMU = ReadIMU.ReadIMU(0x53,"FAKE",XQueue,YQueue,period=0.02)

myMotor0.start()
myMotor1.start()
myMotor2.start()
myIMU.start()

i = 0 
while 1:
#    speed = input('Enter motor speeds seperated by commas: ')
#    speedList = str(speed).split(",")
    speedList = TransformXYRotZToMotor.TransformXYRotZToMotor(XQueue.get(),XQueue.get(),0,debug=True)
    myMotor0.set_speed((speedList[0]))
    myMotor1.set_speed((speedList[1]))
    myMotor2.set_speed((speedList[2]))
#    print "setting speeds to " + str(speedList[0]) + "," + str(speedList[1]) + "," + str(speedList[2])
    i = i + 1    
