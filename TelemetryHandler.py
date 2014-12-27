import threading
import Queue
import Globals

class TelemetryHandler(threading.Thread):
    myMotor1Q = None
    myMotor2Q = None
    myMotor3Q = None
    myIMUQ = None
    myNotificationQ = None
        

    def __init__(self,motor1q,motor2q,motor3q,imuq,notificationq):
        self.myMotor1Q = motor1q
        self.myMotor2Q = motor2q
        self.myMotor3Q = motor3q
        self.myIMUQ = imuq
        self.myNotificationQ = notificationq
        super(TelemetryHandler, self).__init__()

    def run(self):
        queues = { Globals.MOTOR_NOTIFICATION_OFFSET + 0:self.Motor1Queue,
                   Globals.MOTOR_NOTIFICATION_OFFSET + 1:self.Motor2Queue,
                   Globals.MOTOR_NOTIFICATION_OFFSET + 2:self.Motor3Queue,
                   Globals.IMU_NOTIFICATION_OFFSET + Globals.IMU_ID_ACC:self.AccQueue}
        while 1:
            queueNum = self.myNotificationQ.get()
            print "Got message from notification queue: " + str(queueNum)
            queues.setdefault(queueNum,self.DefaultMsg)

    def Motor1Queue(self):
        print "$$$got message from motor 1" + str(self.myMotor1Q.get())
                   
    def Motor2Queue(self):
        print "$$$got message from motor 2" + str(self.myMotor2Q.get())
                   
    def Motor3Queue(self):
        print "$$$got message from motor 3" + str(self.myMotor3Q.get())
                   
    def AccQueue(self):
        print "$$$got message from acc" + str(self.myIMUQ.get())
                   
    def DefaultMsg(self):
        print "$$$unrecognised queue"
        
