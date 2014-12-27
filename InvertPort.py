try:
    import Adafruit_BBIO.GPIO as GPIO
except ImportError:
    print "*********** Using stubbed GPIO module ************"
    import GPIOStubs as GPIO
from time import sleep

class InvertPort():
    myPortNumber = ""
    inverted = False
    valueFile = None
    invertedString = "1"
    notInvertedString = "0"
    myDebug = None
    def __init__(self,invertPortNumber,debug=False):
        self.myPortNumber = invertPortNumber
	self.myDebug = debug
        GPIO.setup(self.myPortNumber,GPIO.OUT)
#        exportFile = open('/sys/class/gpio/export','wa')
#        exportFile = open('./export','a')
#        exportFile.write(str(self.myPortNumber))
#        exportFile.write('\n')
#        exportFile.close()
        sleep(0.1)
        baseFileString =  "/sys/class/gpio/gpio" + str(self.myPortNumber) 
        dirFileString = baseFileString + "/direction" 
#        dirFile =  open(dirFileString,'a')
#        dirFile.write('high\n')
#        dirFile.close()
        valueFileString = baseFileString + "/value" 
#        self.valueFile = open(valueFileString)
        #TODO: Close strings on delete

    def invert(self):
        if self.inverted:
            return
        else:
            if(self.myDebug):
                print "inverting port " + str(self.myPortNumber)
            GPIO.output(self.myPortNumber,GPIO.HIGH)
            self.inverted = True
#            self.valueFile.write(self.invertedString)
            
    def not_invert(self):
        if not self.inverted:
            return
        else:
            if(self.myDebug):
                print "uninverting port :" + str(self.myPortNumber)
            GPIO.output(self.myPortNumber,GPIO.LOW)
            self.inverted = False
 #           self.valueFile.write(self.notInvertedString)
