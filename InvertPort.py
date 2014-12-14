class InvertPort():
    myPortNumber = -1;
    inverted = False;
    def __init__(self,invertPortNumber):
        self.myPortNumber = invertPortNumber

    def invert(self):
        if self.inverted:
            return
        else:
            print "inverting port " + str(self.myPortNumber)
            self.inverted = True
            
    def not_invert(self):
        if not self.inverted:
            return
        else:
            print "uninverting port :" + str(self.myPortNumber)
            self.inverted = False
