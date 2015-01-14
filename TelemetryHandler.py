import threading
import Queue
import Globals
import socket
import errno
import binascii

BUFFER_SIZE = 50

class TelemetryHandler(threading.Thread):
    myMotor1Q = None
    myMotor2Q = None
    myMotor3Q = None
    myIMUQ = None
    myNotificationQ = None
    myConn = None
    myDebug = None
    
    def __init__(self,motor1q,motor2q,motor3q,imuq,notificationq,conn,debug=False):
        self.myMotor1Q = motor1q
        self.myMotor2Q = motor2q
        self.myMotor3Q = motor3q
        self.myIMUQ = imuq
        self.myNotificationQ = notificationq
        super(TelemetryHandler, self).__init__()
        self.myConn = conn
        self.myDebug = debug
        
    def run(self):
        while 1:
            queueNum = self.myNotificationQ.get()
            if self.myDebug:
                print "Got message from notification queue: " + str(queueNum)
            activeQueue = self.QueueLookup(queueNum)
            msg = activeQueue.get()
            if(queueNum > 99 and queueNum < 250):
                try:
                    if self.myDebug:
                        print "msg is: ", binascii.hexlify(msg)
                    self.myConn.send(msg)
                except socket.error, e:
                    if isinstance(e.args, tuple):
                        print "errno is %d" % e[0]
                        if e[0] == errno.EPIPE:
                    # remote peer disconnected
                            print "Detected remote disconnect"
                            return
                        else:
                    # determine and handle different error
                            pass
                    else:
                        print "socket error ", e
                        return
                    return
                except IOError, e:
            # Hmmm, Can IOError actually be raised by the socket module?
                    print "Got IOError: ", e
                    return
            
    def QueueLookup(self,id):
        if(id == Globals.MOTOR_NOTIFICATION_OFFSET + 0):
            if self.myDebug:
                print "Motor 1 queue"
            return self.myMotor1Q
        if(id == Globals.MOTOR_NOTIFICATION_OFFSET + 1):
            if self.myDebug:
                print "Motor 2 queue"
            return self.myMotor2Q
        if(id == Globals.MOTOR_NOTIFICATION_OFFSET + 2):
            if self.myDebug:
                print "Motor 3 queue"
            return self.myMotor3Q
        if(id == Globals.IMU_NOTIFICATION_OFFSET + Globals.IMU_ID_ACC):
            if self.myDebug:
                print "IMU ACC QUEUE"
            return self.myIMUQ
