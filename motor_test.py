import Motor
from time import sleep

myMotor = Motor.Motor(1,2,3,4)

myMotor.start()

i = 0 
while 1:
    print "Motor_test i:" + str(i)
    myMotor.set_speed(i)
    i = i + 1
    sleep(1.9)
    
