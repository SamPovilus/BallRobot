import threading
import Queue
import Globals
import socket
import errno
import binascii

TCP_IP = '192.168.1.51'
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
        while 1:
            self.conn, addr = self.s.accept()
            print 'Connection address:', addr
            self.Connection()
            print 'Closing connection from:', addr
            #self.conn.close()
        
    def Connection(self):
        while 1:
            queueNum = self.myNotificationQ.get()
            print "Got message from notification queue: " + str(queueNum)
            activeQueue = self.QueueLookup(queueNum)
            msg = activeQueue.get()
            if(queueNum > 99 and queueNum < 250):
                try:
                    print "msg is: ", binascii.hexlify(msg)
                    self.conn.send(msg)
                except socket.error, e:
                    if isinstance(e.args, tuple):
                        print "errno is %d" % e[0]
                        if e[0] == errno.EPIPE:
                    # remote peer disconnected
                            print "Detected remote disconnect"
                        else:
                    # determine and handle different error
                            pass
                    else:
                        print "socket error ", e
                        self.conn.close()
                    break
                except IOError, e:
            # Hmmm, Can IOError actually be raised by the socket module?
                    print "Got IOError: ", e
                    break
            
    def QueueLookup(self,id):
        if(id == Globals.MOTOR_NOTIFICATION_OFFSET + 0):
            print "Motor 1 queue"
            return self.myMotor1Q
        if(id == Globals.MOTOR_NOTIFICATION_OFFSET + 1):
            print "Motor 2 queue"
            return self.myMotor2Q
        if(id == Globals.MOTOR_NOTIFICATION_OFFSET + 2):
            print "Motor 3 queue"
            return self.myMotor3Q
        if(id == Globals.IMU_NOTIFICATION_OFFSET + Globals.IMU_ID_ACC):
            print "IMU ACC QUEUE"
            return self.myIMUQ
