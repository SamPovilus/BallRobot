import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import time
ADC.setup()
PWM.start("P9_14",50,500,0)

while 1:
	value = ADC.read("P9_40")
	PWM.set_duty_cycle("P9_14",value*100.0)
	str(value)
	time.sleep(.01)

