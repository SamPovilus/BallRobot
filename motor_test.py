import Motor
from time import sleep

myMotor0 = Motor.Motor("P9_14","P9_12",True,0,5000,20)
myMotor1 = Motor.Motor("P9_22","P9_18",True,1,5000,20)
myMotor2 = Motor.Motor("P8_13","P8_11",True,2,5000,20)

myMotor0.start()
myMotor1.start()
myMotor2.start()

i = 0 
while 1:
    speed = input('Enter motor speeds seperated by commas: ')
    speedList = str(speed).split(",")
    myMotor0.set_speed(int(speedList[0]))
    myMotor1.set_speed(int(speedList[1]))
    myMotor2.set_speed(int(speedList[2]))
    print "setting speeds to " + str(int(speedList[0])) + "," + str(int(speedList[1])) + "," + str(int(speedList[2]))
    i = i + 1    
