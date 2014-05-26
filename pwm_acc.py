from Adafruit_I2C import Adafruit_I2C as I2C
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.PWM as PWM2
temp = I2C(0x48)
acc = I2C(0x53)
acc.write8(0x31,0xB)
acc.write8(0x2d,0x8)
acc.write8(0x2e,0x80)
PWM.start("P9_22",50,20000,0)
PWM2.start("P9_14",50,20000,0)
PWM.set_duty_cycle("P9_22",10.0)
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
	PWM.set_duty_cycle("P9_22",avgVal)
	PWM2.set_duty_cycle("P9_14",avgValy)
	#print avgArray
	#print i
