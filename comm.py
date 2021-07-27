import time
import socket
import threading
import multiprocessing
from cryptography.fernet import Fernet
from common.init import *

class comm:
    '''Class for streamlining communication with server application. Input Inet address and port to establish connection'''

    with open('data/key.key','rb') as file:
        key = file.read()

    crypt = Fernet(key)
    #commands = ('move','remember','kill','updateProperty','reboot')

    def __init__(self,Inet:str,send_port:int,listen_port:int,encryption_enabled=True):
        self.inet = Inet
        self.sendPort = send_port
        self.listenPort = listen_port
        self.encrytionEnabled = encryption_enabled
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.currentServerMessage = ""

    def listen(self):
        '''listens on comm's listenPort and passes the received data to the message handler'''
        addr = ("",self.listenPort)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(100)
        lprint("listening on port " + str(self.listenPort) + "...")
        while ns['commRunning']:
            try:
                c,ServerAdr = s.accept()
                lprint("Connection established, receiving data...")
                clientData = c.recv(1024)
                if ns['encryptionEnabled']:
                    clientData = comm.crypt.decrypt(clientData).decode('UTF-8')
                else:
                    clientData = clientData.decode('UTF-8')
                lprint("received " + clientData + " from " + str(ServerAdr))
                threading.Thread(target=comm.serverMessageHandler,args=(clientData,)).start()
                # if clientData[0] in comm.commands:
                #     lprint("received valid command")
                # else:
                #     lprint("received invalid command")
                #return clientData
            except Exception as e:
                lprint('data could not be retrieved/decoded')
                lprint(e)
                return 'error'
            finally:
                c.close()

        
    def serverMessageHandler(clientMessage:str):
        '''handles incoming server messages'''
        #try:
        #while ns['serverMessageHandlerRunning']:
        clientData = clientMessage
        clientData = clientData.split(sep=':')
        args = clientData[1]
        args = args.split(sep=',')
        if clientData[0] == 'kill':
            lprint("Kill command received...shutting down comms")
            updateProperty('commRunning',False)
        elif clientData[0] == 'reboot':
            reboot()
        elif clientData[0] == 'home':
            Delta1.home()
        elif clientData[0] == 'move':
            newargs = []
            for i in args:
                i = float(i)
                newargs.append(i)
            Delta1.move(*newargs)
        elif clientData[0] == 'remember':
            print('remember' + args)
        elif clientData[0] == 'updateProperty':
            updateProperty(*args)
        time.sleep(.1)
        # except Exception as e:
        #     lprint("serverMessageHandler exception occured")
        #     lprint(e.with_traceback)





