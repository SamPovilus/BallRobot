import Motor
from time import sleep

myMotor = Motor.Motor(1,2,3,4,5,100)

myMotor.start()

i = 0 
while 1:
    speed = input('Enter motor speeds seperated by commas: ')
    speedList = str(speed).split(",")
    myMotor.set_speed(int(speedList[0]))
    i = i + 1
    sleep(1.9)
    
