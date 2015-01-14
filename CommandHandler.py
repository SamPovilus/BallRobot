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
            command = self.myConn.recv(COMMAND_SIZE)
            print str(command)
