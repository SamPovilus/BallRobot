import threading
import Queue
import Globals
import socket

TCP_IP = '192.168.1.141'
TCP_PORT = 5005
BUFFER_SIZE = 50

class TelemetryHandler(threading.Thread):
    myMotor1Q = None
    myMotor2Q = None
    myMotor3Q = None
    myIMUQ = None
    myNotificationQ = None
    s = None
    conn = None
    
    def __init__(self,motor1q,motor2q,motor3q,imuq,notificationq):
        self.myMotor1Q = motor1q
        self.myMotor2Q = motor2q
        self.myMotor3Q = motor3q
        self.myIMUQ = imuq
        self.myNotificationQ = notificationq
        super(TelemetryHandler, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((TCP_IP, TCP_PORT))
        self.s.listen(1)

    def run(self):
        queues = { Globals.MOTOR_NOTIFICATION_OFFSET + 0:self.Motor1Queue,
                   Globals.MOTOR_NOTIFICATION_OFFSET + 1:self.Motor2Queue,
                   Globals.MOTOR_NOTIFICATION_OFFSET + 2:self.Motor3Queue,
                   Globals.IMU_NOTIFICATION_OFFSET + Globals.IMU_ID_ACC:self.AccQueue}
        self.conn, addr = self.s.accept()
        print 'Connection address:', addr
        while 1:
            queueNum = self.myNotificationQ.get()
            print "Got message from notification queue: " + str(queueNum)
            queues.setdefault(queueNum,self.DefaultMsg)
            queues[queueNum]()

            
    def Motor1Queue(self):
        msg = self.myMotor1Q.get()
        print "got message from motor 1" + str(msg)
        self.conn.send(msg)
        
    def Motor2Queue(self):
        print "got message from motor 2" + str(self.myMotor2Q.get())
                   
    def Motor3Queue(self):
        print "got message from motor 3" + str(self.myMotor3Q.get())
                   
    def AccQueue(self):
        print "got message from acc" + str(self.myIMUQ.get())
                   
    def DefaultMsg(self):
        print "unrecognised queue"
