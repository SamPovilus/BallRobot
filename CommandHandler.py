import threading
import Queue
import Globals
import socket
import errno
import binascii

COMMAND_SIZE = 20

class CommandHandler(threading.Thread):
    myCommandQueue = None
    myConn = None
    
    def __init__(self,commandQ,conn):
        self.myCommandQueue = commandQ
        super(CommandHandler, self).__init__()
        self.myConn = conn

    def run(self):
        while 1:
            try:
                command = self.myConn.recv(COMMAND_SIZE)
                print str(command)
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
