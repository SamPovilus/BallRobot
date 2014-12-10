import Adafruit_BBIO.PWM as motor
class Motor:
def __init__(self, port, inverted,motorNumber,freq)
    motor.start(port,50,freq,inverted)

def set_speed(speed)
