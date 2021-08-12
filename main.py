import common.motion
import time
import multiprocessing
from common.points import points
from common.delta import db
from common.config import *
from common.comm import comm



#manager = multiprocessing.Manager()



# def checkServerMessage():
#     '''checks for incoming server messages until one appears and return the message'''
#     while com.currentServerMessage == "":
#         time.sleep(.1)
#     with lock:
#         clientData = com.currentServerMessage 
#         com.currentServerMessage = ""
#     return clientData




if __name__ == '__main__':
    
    f = 6.25 #fixed base radius (in)
    rf = 7.98 #Bicep length (in)
    re = 25 #Forearm length (in)
    r = 2.3125  #end effector radius (in)
    speed = 24 #bot speed (in/s)

    Delta1 = db(f,rf,re,r,botSpeed=speed,servo_velocity_control=True)

    Delta1.home()

    length = 18
    width = 15
    xpoints = 7
    ypoints = 3
    z0 = -23.25

    ps = points()
    ps.pointField(length,width,xpoints,ypoints,z0)
    ps.pfShift(-length/2,-width/2,0)

    retpoint = (12,0,-18)
    lprint('points generated, delta object created')

    com = comm(Inet=ns['serverAdr'],send_port=ns['serverPort'],listen_port=ns['listenPort'],delta=Delta1)
    listenThread = threading.Thread(target=com.listen)
    senderThread = threading.Thread(target=com.messageSender)
    listenThread.start()
    senderThread.start()
    lprint("comm threads started")
    listenThread.join()
    senderThread.join()
    lprint("Program finished...")
    Delta1.disableTorque()




