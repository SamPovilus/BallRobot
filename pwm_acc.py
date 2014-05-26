from Adafruit_I2C import Adafruit_I2C as I2C
import Adafruit_BBIO.PWM as motor1
import Adafruit_BBIO.PWM as motor2
motor_1_port_string = "P9_22"
motor_2_port_string = "P9_14"
motor_3_port_string = "foo"

motor_1_invert = 0
motor_2_invert = 0
motor_3_invert = 0

pwm_freq = 20000
temp = I2C(0x48)
acc = I2C(0x53)
acc.write8(0x31,0xB)
acc.write8(0x2d,0x8)
acc.write8(0x2e,0x80)
motor1.start(motor_1_port_string,50,pwm_freq,motor_1_invert)
motor2.start(motor_2_port_string,50,pwm_freq,motor_2_invert)
motor3.start(motor_3_port_string,50,pwm_freq,motor_3_invert)

motor1.set_duty_cycle(motor_1_port_string,10.0)
motor2.set_duty_cycle(motor_2_port_string,10.0)
motor3.set_duty_cycle(motor_3_port_string,10.0)
i=0
avgArray = []
avgArrayy = []
for x in range(0,51):
	avgArray.append(7.0)
	avgArrayy.append(7.0)
while 1:
	value1 = acc.readU8(0x32)
	value2 = acc.readU8(0x33)
	valuex = (value2 << 8) + value1
	value1 = acc.readU8(0x34)
	value2 = acc.readU8(0x35)
	valuey = (value2 << 8) + value1
	if valuex > (1<<15):
		valuex = int(bin(valuex),2)-(1<<16)
	if valuey > (1<<15):
		valuey = int(bin(valuey),2)-(1<<16)
	#print (bin(value),2)
	i = i +1
	if i > 50:
		i = 0
	foo = ((valuex/1050.0)*20.0)+6.0
	goo = ((valuey/1050.0)*20.0)+6.0
	avgArray[i] = foo
	avgArrayy[i] = goo
	avgVal = sum(avgArray)/len(avgArray)
	avgValy = sum(avgArrayy)/len(avgArrayy)
	print "val %f, val1: %i, val2: %i\n" % (avgVal , value1, value2)
	motor1.set_duty_cycle("P9_22",avgVal)
	motor2.set_duty_cycle("P9_14",avgValy)
	#print avgArray
	#print i
