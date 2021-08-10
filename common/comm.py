from queue import Empty
import time
import socket
import threading
from pathlib import Path
import csv
import multiprocessing
from cryptography.fernet import Fernet
from common.config import *
from common.delta import db
from common.motion import motion
import sys

class comm:
    '''Class for streamlining communication with server application. Input Inet address and port to establish connection.
    Class also contains various methods necessary for controlling pi/robot that are relevant to communication with java server'''

    with open('data/key.key','rb') as file:
        key = file.read()

    crypt = Fernet(key)
    #commands = ('move','remember','kill','updateProperty','reboot')

    def __init__(self,Inet:str,send_port:int,listen_port:int,delta:db,encryption_enabled=True):
        self.inet = Inet
        self.sendPort = send_port
        self.listenPort = listen_port
        self.encrytionEnabled = encryption_enabled
        self.currentServerMessage = ""
        self.Delta1 = delta

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
                response = self.serverMessageHandler(clientData)
                # if clientData[0] in comm.commands:
                #     lprint("received valid command")
                # else:
                #     lprint("received invalid command")
                #return clientData
                #time.sleep(.1)
            except Exception as e:
                lprint('data could not be retrieved/decoded')
                lprint(e)
                return 'error'
            finally:
                if ns['encryptionEnabled']:
                    toSend = comm.crypt.encrypt(response.encode('UTF-8'))
                else:
                    toSend = response.encode('UTF-8')
                toSend += b'\n'
                c.send(toSend)
                c.close()

        
    def serverMessageHandler(self,clientMessage:str):
        '''handles incoming server messages'''
        #try:
        #while ns['serverMessageHandlerRunning']:
        clientData = clientMessage
        clientData = clientData.split(sep=':')
        args = clientData[1]
        args = args.split(sep=',')
        toSend = 'ok'
        if clientData[0] == 'kill':
            lprint("Kill command received...shutting down comms")
            toServerQueue.put("Shutting down pi's comms...")
            time.sleep(.1)
            comm.updateProperty('commRunning',False)
            time.sleep(.5)
            toServerQueue.put(None)
        elif clientData[0] == 'reboot':
            threading.Thread(target=comm.reboot).start()
        elif clientData[0] == 'hello':
            toSend = 'hello'
        elif clientData[0] == 'home':
            threading.Thread(target=self.Delta1.home).start()
        elif clientData[0] == 'move':
            newargs = []
            for i in args:
                newargs.append(float(i))
            threading.Thread(target=self.Delta1.move,args=(newargs)).start()
        elif clientData[0] == 'trays':
            newargs = []
            for arg in args:
                newargs.append(float(arg))
            threading.Thread(target=motion.trays,args=(self.Delta1,*newargs)).start()
        elif clientData[0] == 'remember':
            toSend = 'remember:'
            translationTable = dict.fromkeys(map(ord,'() '),None)
            currentPosition = str(self.Delta1.getCurrentPosition())
            currentPosition = currentPosition.translate(translationTable)
            toSend += currentPosition
            coords = currentPosition.split(',')
            comm.rememberPoint(coords)
        elif clientData[0] == 'updateProperty':
            threading.Thread(target=comm.updateProperty,args=(args)).start()
        else:
            toSend = 'error'
        return toSend
        # except Exception as e:
        #     lprint("serverMessageHandler exception occured")
        #     lprint(e.with_traceback)

    def messageSender(self):
        while ns['commRunning']:
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    toServer = str(toServerQueue.get())
                    if toServer != None:
                        s.connect((self.inet,self.sendPort))
                        if ns['encryptionEnabled']:
                            toServer = comm.crypt.encrypt(toServer.encode('UTF-8'))
                        else:
                            toServer = toServer.encode('UTF-8')
                        s.sendall(toServer)
            except :
                lprint(f"Oops!  + {sys.exc_info()[0]} occurred.")
            finally:
                time.sleep(.1)




    @staticmethod
    def updateProperty(propertyName:str,newValue):
        lprint("updating property: " + propertyName + " to: " + str(newValue))
        toServerQueue.put("updating property: " + propertyName + " to: " + str(newValue))
        with lock:
            ns[propertyName] = newValue

    @staticmethod
    def reboot():
        lprint("reboot command received from server, rebooting...")
        toServerQueue.put("Reboot command received...rebooting")
        time.sleep(1)
        with lock:
            time.sleep(3)
            os.system('sudo reboot')

    @staticmethod
    def rememberPoint(coords:tuple):
        newPoint = [] #need to turn str to float first
        for i in coords:
            newPoint.append(float(i))
        path = Path(os.path.dirname(__file__))
        path = path.parent.absolute()
        newPath = path.joinpath('data','calibration_point.csv')
        with open(newPath,'w') as file:
            header = ['x','y','z']
            writer = csv.writer(file,lineterminator='\n')
            writer.writerow(header)
            writer.writerow(newPoint)
        toServerQueue.put(f"Saved point x: {coords[0]}, y: {coords[1]}, z: {coords[2]} locally on pi")

        



