import Motor
import ReadIMU
import TransformXYRotZToMotor
import PID
import Queue
from time import sleep
import Globals
import TelemetryHandler
import CommandHandler
import socket
import threading

TCP_IP = ""
TCP_PORT = 5005

Motor1TlmQueue = Queue.Queue(maxsize=100)
Motor2TlmQueue = Queue.Queue(maxsize=100)
Motor3TlmQueue = Queue.Queue(maxsize=100)
IMUTlmQueue = Queue.Queue(maxsize=100)
NotificationQueue = Queue.Queue(maxsize=200)
CommandQueue = Queue.Queue(maxsize=100)
XAccQueue = Queue.Queue(maxsize=40)
YAccQueue = Queue.Queue(maxsize=40)
XGyroQueue = Queue.Queue(maxsize=40)
YGyroQueue = Queue.Queue(maxsize=40)

myMotor0 = Motor.Motor("P9_14","P9_12",True,0,10000,Motor1TlmQueue,NotificationQueue,period = 0.02,filterDepth = 10, debug= False)
myMotor1 = Motor.Motor("P9_22","P9_18",True,1,10000,Motor2TlmQueue,NotificationQueue,period = 0.02,filterDepth = 10, debug= False)
myMotor2 = Motor.Motor("P8_13","P8_11",True,2,10000,Motor3TlmQueue,NotificationQueue,period = 0.02,filterDepth = 10, debug= False)

myPIDX = PID.PID()
myPIDY = PID.PID()
myPIDX.set_PID(1.0,0.0,0.0)
myPIDY.set_PID(1.0,0.0,0.0)

myIMU = ReadIMU.ReadIMU(0x53,0x68,XAccQueue,YAccQueue,XGyroQueue,YGyroQueue,IMUTlmQueue,NotificationQueue,maxAccVal = 256.0, maxGyroVal = 128.0,period=0.01,debug = False)

def TcpHandler():
    while 1:
        print "Entered tcp handler"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print 'Connection address:', addr
        myTelemetryHandler = TelemetryHandler.TelemetryHandler(Motor1TlmQueue, Motor2TlmQueue, Motor3TlmQueue, IMUTlmQueue , NotificationQueue, conn,debug=False)
        myCommandHandler= CommandHandler.CommandHandler(CommandQueue,myIMU,myPIDX,myPIDY,conn)
        myTelemetryHandler.daemon = True
        myCommandHandler.daemon = True
        myTelemetryHandler.start()
        myCommandHandler.start()
        while(myTelemetryHandler.isAlive() and myCommandHandler.isAlive()):
            sleep(2)
        

tcpThread = threading.Thread(target=TcpHandler)
tcpThread.daemon = True
tcpThread.start()

myMotor0.daemon = True
myMotor1.daemon = True
myMotor2.daemon = True
myIMU.daemon = True

myMotor0.start()
myMotor1.start()
myMotor2.start()
myIMU.start()

i = 0

xval = 0.0
yval = 0.0

while 1:
    #    speed = input('Enter motor speeds seperated by commas: ')
    #    speedList = str(speed).split(",")
    #    for i in speedList.length():
    #        speedList[i] = float(speedList[i])
    #try:
    xval = myPIDX.process(XAccQueue.get(),XGyroQueue.get());
    yval = myPIDY.process(YAccQueue.get(),YGyroQueue.get());

    speedList = TransformXYRotZToMotor.TransformXYRotZToMotor(xval,yval,0,debug = False)
    myMotor0.set_speed((speedList[0]))
    myMotor1.set_speed((speedList[1]))
    myMotor2.set_speed((speedList[2]))
        #    print "setting speeds to " + str(speedList[0]) + "," + str(speedList[1]) + "," + str(speedList[2])
    i = i + 1    
    #except KeyboardInterrupt:
    #s.close()
    #    print "done"
    #    exit()
