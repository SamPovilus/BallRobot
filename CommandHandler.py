import threading
import Queue
import Globals
import socket
import errno
import binascii
import struct

COMMAND_SIZE = 20

class CommandHandler(threading.Thread):
    myCommandQueue = None
    myConn = None
    myReadIMU = None
    
    def __init__(self,commandQ,ReadIMU,conn):
        self.myCommandQueue = commandQ
        super(CommandHandler, self).__init__()
        self.myConn = conn
        self.myReadIMU = ReadIMU
        
    def run(self):
        while 1:
            try:
                command = self.myConn.recv(COMMAND_SIZE)
            except socket.error, e:
                if isinstance(e.args, tuple):
                    print "errno is %d" % e[0]
                    if e[0] == errno.EPIPE:
                        # remote peer disconnected
                        print "Detected remote disconnect"
                        return
                    else:
                        # determine and handle different error
                        pass
                else:
                    print "socket error ", e
                    return
                return
            except IOError, e:
            # Hmmm, Can IOError actually be raised by the socket module?
                print "Got IOError: ", e
                return
            commandUnpacked = struct.unpack('>L12s',command)
            if commandUnpacked[0] == Globals.ACC_OVERRIDE_VALUES:
                dataUnpacked = struct.unpack('>hhhhl',commandUnpacked[1])
                print "Acceleromoter values x: " + str(dataUnpacked[0]) + " y: " +  str(dataUnpacked[1]) + " z: " + str(dataUnpacked[2])
                self.myReadIMU.setOverrideValuesAcc(dataUnpacked[0],dataUnpacked[1],dataUnpacked[2])
            if commandUnpacked[0] == Globals.ACC_OVERRIDE_AXIS:
                dataUnpacked = struct.unpack('>BBBBLL',commandUnpacked[1])
                print "Accelerometer overrides x: " + str(dataUnpacked[0]) + " y: " +  str(dataUnpacked[1]) + " z: " + str(dataUnpacked[2])
                self.myReadIMU.setOverrideAxisAcc(dataUnpacked[0],dataUnpacked[1],dataUnpacked[2])
            if commandUnpacked[0] == Globals.ACC_SET_DIVISOR:
                dataUnpacked = struct.unpack('>fLL',commandUnpacked[1])
                print "Accelrometer divisor set to: " + str(dataUnpacked[0])
                self.myReadIMU.setAccDivisorAcc(dataUnpacked[0])
            if commandUnpacked[0] == Globals.GYRO_OVERRIDE_VALUES:
                dataUnpacked = struct.unpack('>hhhhl',commandUnpacked[1])
                print "Gyro values x: " + str(dataUnpacked[0]) + " y: " +  str(dataUnpacked[1]) + " z: " + str(dataUnpacked[2])
                self.myReadIMU.setOverrideValuesGyro(dataUnpacked[0],dataUnpacked[1],dataUnpacked[2])
            if commandUnpacked[0] == Globals.GYRO_OVERRIDE_AXIS:
                dataUnpacked = struct.unpack('>BBBBLL',commandUnpacked[1])
                print "Gyro overrides x: " + str(dataUnpacked[0]) + " y: " +  str(dataUnpacked[1]) + " z: " + str(dataUnpacked[2])
                self.myReadIMU.setOverrideAxisGyro(dataUnpacked[0],dataUnpacked[1],dataUnpacked[2])
            if commandUnpacked[0] == Globals.GYRO_SET_DIVISOR:
                dataUnpacked = struct.unpack('>fLL',commandUnpacked[1])
                print "Gyro accelrometer divisor set to: " + str(dataUnpacked[0])
                self.myReadIMU.setAccDivisorGyro(dataUnpacked[0])
