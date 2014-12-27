import threading
import Queue


class TelemtryHandler(threading.Thread):
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
        

    def run(self):
        queues = { MOTOR_NOTIFICATION_OFFSET + 0:Motor1Queue,
                   MOTOR_NOTIFICATION_OFFSET + 1:Motor2Queue,
                   MOTOR_NOTIFICATION_OFFSET + 2:Motor3Queue,
                   IMU_NOTIFICATION_OFFSET + IMU_ID_ACC:AccQueue
        while 1:
            queueNum = self.myNotificationQ.get()
            queues.setdefault(queueNum,DefaultMsg)

    def Motor1Queue():
        puts "got message from motor 1" + str(self.myMotor1Q.get())
                   
    def Motor2Queue():
        puts "got message from motor 2" + str(self.myMotor2Q.get())
                   
    def Motor3Queue():
        puts "got message from motor 3" + str(self.myMotor3Q.get())
                   
    def AccQueue():
        puts "got message from acc" + str(self.myIMUQ.get())
                   
    def DefaultMsg():
        puts "unrecognised queue"
        
