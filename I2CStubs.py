class I2CStubs():
    def __init__(self,addr):
        print "addr: " + str(addr)

    def write8(self,addr,val):
        print "write8 addr: " + str(addr) + " val: " + str(val)

    def readU8(self,addr):
        print "read8 addr: " + str(addr)
