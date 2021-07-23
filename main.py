import motion
from Delta import db
from points import points
import time
import multiprocessing
from comm import comm
from common.tools import *


#manager = multiprocessing.Manager()
ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['serverMessageHandlerRunning'] = True
com = comm(Inet=ns['serverAdr'],send_port=ns['serverPort'],listen_port=ns['listenPort'])



def serverMessageHandler():
    '''checks for incoming server messages and handles them'''
    #try:
    while ns['serverMessageHandlerRunning']:
        clientData = checkServerMessage()
        clientData = clientData.split(sep=':')
        args = clientData[1]
        args = args.split(sep=',')
        if clientData[0] == 'move':
            newargs = []
            for i in args:
                i = float(i)
                newargs.append(i)
            Delta1.move(*newargs)
        elif clientData[0] == 'remember':
            print('remember' + args)
        elif clientData[0] == 'updateProperty':
            updatePropertyThread = threading.Thread(target=updateProperty,args=(args))
            updatePropertyThread.start()
        time.sleep(.1)
    # except Exception as e:
    #     lprint("serverMessageHandler exception occured")
    #     lprint(e.with_traceback)




def checkServerMessage():
    '''checks for incoming server messages until one appears and return the message'''
    while com.currentServerMessage == "":
        time.sleep(.1)
    with lock:
        clientData = com.currentServerMessage 
        com.currentServerMessage = ""
    return clientData

def updateProperty(propertyName,newValue):
    with lock:
        ns[propertyName] = newValue


if __name__ == '__main__':
    commThread = threading.Thread(target=com.listen)
    commThread.start()

    lprint("commThread started")

    f = 6.25 #fixed base radius (in)
    rf = 7.98 #Bicep length (in)
    re = 25 #Forearm length (in)
    r = 2.3125  #end effector radius (in)
    speed = 24 #bot speed (in/s)

    Delta1 = db(f,rf,re,r,botSpeed=speed)

    length = 18
    width = 15
    xpoints = 7
    ypoints = 3
    z0 = -23.25

    ps = points()
    ps.pointfield(length,width,xpoints,ypoints,z0)
    ps.pfShift(-length/2,-width/2,0)

    retpoint = (12,0,-18)
    lprint('points generated, delta object created')
    serverMessageHandler()




