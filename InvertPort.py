import Adafruit_BBIO.GPIO as GPIO

class InvertPort():
    myPortNumber = "";
    inverted = False;
    def __init__(self,invertPortNumber):
        self.myPortNumber = invertPortNumber
        GPIO.setup(self.myPortNumber,GPIO.OUT)
        
    def invert(self):
        if self.inverted:
            return
        else:
            print "inverting port " + str(self.myPortNumber)
            GPIO.output(self.myPortNumber,GPIO.HIGH)
            self.inverted = True
            
    def not_invert(self):
        if not self.inverted:
            return
        else:
            print "uninverting port :" + str(self.myPortNumber)
            GPIO.output(self.myPortNumber,GPIO.LOW)
            self.inverted = False
