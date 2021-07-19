import time
import socket
import threading
import multiprocessing
from cryptography.fernet import Fernet

class comm:
    '''Class for streamlining communication with server application. Input Inet address and port to establish connection'''

    with open('data/key.key','rb') as file:
        key = file.read()

    lock = threading.Lock()
    crypt = Fernet(key)

    def __init__(self,Inet:str,send_port:int,listen_port:int,encryption_enabled=True):
        self.inet = Inet
        self.sendPort = send_port
        self.listenPort = listen_port
        self.encrytionEnabled = encryption_enabled
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def listen(self):
        '''listens on comm's listenPort and returns the received data as a string'''
        addr = ("",self.listenPort)
        s = socket.create_server(addr)
        run = True
        while(run):
            try:
                c,ServerAdr = s.accept()
                clientData = c.recv(1024)
                if self.encrytionEnabled:
                    clientData = comm.crypt.decrypt(clientData).decode('UTF-8')
                else:
                    clientData = clientData.decode('UTF-8')
                print('received from ' + ServerAdr + ':' + clientData)
                return clientData
            except Exception as e:
                print('data could not be retrieved/decoded')
                print(e)





