import Motor
import ReadIMU
import TransformXYRotZToMotor
import Queue
from time import sleep
MOTOR_NOTIFICATION_OFFSET = 100
IMU_NOTIFICATION_OFFSET = 200
IMU_ID_ACC = 10
IMU_ID_GYRO = 20
Motor1TlmQueue = Queue.Queue(maxsize=10)
Motor2TlmQueue = Queue.Queue(maxsize=10)
Motor3TlmQueue = Queue.Queue(maxsize=10)
IMUTlmQueue = Queue.Queue(maxsize=10)
NotificationQueue = Queue.Queue(maxsize=4)

XQueue = Queue.Queue(maxsize=2)
YQueue = Queue.Queue(maxsize=2)

myMotor0 = Motor.Motor("P9_14","P9_12",True,0,5000,Motor1TlmQueue,NotificationQueue,period = 0.02,filterDepth = 2, debug= True)
myMotor1 = Motor.Motor("P9_22","P9_18",True,1,5000,Motor3TlmQueue,NotificationQueue,period = 0.02,filterDepth = 2, debug= True)
myMotor2 = Motor.Motor("P8_13","P8_11",True,2,5000,Motor3TlmQueue,NotificationQueue,period = 0.02,filterDepth = 2, debug= True)

myIMU = ReadIMU.ReadIMU(0x53,"FAKE",XQueue,YQueue,IMUTlmQueue,NotificationQueue,period=0.02)

myMotor0.start()
myMotor1.start()
myMotor2.start()
myIMU.start()

i = 0 
while 1:
#    speed = input('Enter motor speeds seperated by commas: ')
#    speedList = str(speed).split(",")
#    for i in speedList.length():
#        speedList[i] = float(speedList[i])
    speedList = TransformXYRotZToMotor.TransformXYRotZToMotor(XQueue.get(),YQueue.get(),0,debug = True)
    myMotor0.set_speed((speedList[0]))
    myMotor1.set_speed((speedList[1]))
    myMotor2.set_speed((speedList[2]))
#    print "setting speeds to " + str(speedList[0]) + "," + str(speedList[1]) + "," + str(speedList[2])
    i = i + 1    
