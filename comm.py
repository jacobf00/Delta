import time
import socket
import threading
import multiprocessing
from cryptography.fernet import Fernet
from common.tools import *

class comm:
    '''Class for streamlining communication with server application. Input Inet address and port to establish connection'''

    with open('data/key.key','rb') as file:
        key = file.read()

    crypt = Fernet(key)
    commands = ('move','remember','kill','updateProperty')

    def __init__(self,Inet:str,send_port:int,listen_port:int,encryption_enabled=True):
        self.inet = Inet
        self.sendPort = send_port
        self.listenPort = listen_port
        self.encrytionEnabled = encryption_enabled
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.currentServerMessage = ""

    def listen(self):
        '''listens on comm's listenPort and returns the received data as a string'''
        addr = ("",self.listenPort)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(addr)
        s.listen(100)
        lprint("listening on port " + str(self.listenPort) + "...")
        run = True
        while(run):
            try:
                c,ServerAdr = s.accept()
                lprint("Connection established, receiving data...")
                clientData = c.recv(1024)
                if self.encrytionEnabled:
                    clientData = comm.crypt.decrypt(clientData).decode('UTF-8')
                else:
                    clientData = clientData.decode('UTF-8')
                lprint("received " + clientData + " from " + str(ServerAdr))
                with lock:
                    self.currentServerMessage = clientData
                clientData = clientData.split(sep=':')
                if clientData[0] == 'kill':
                    lprint("Kill command received...shutting down comms")
                    run = False
                if clientData[0] in comm.commands:
                    lprint("received valid command")
                else:
                    lprint("received invalid command")
                #return clientData
            except Exception as e:
                lprint('data could not be retrieved/decoded')
                lprint(e)
                return 'error'
            finally:
                c.close()





