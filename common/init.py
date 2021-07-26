from Delta import db
from points import points
from common.tools import *
from comm import comm
import os
import time

'''contains initialized objects vital for the program along with general methods used by program'''


def updateProperty(propertyName,newValue):
    lprint("updating property: " + propertyName + " to: " + str(newValue))
    with lock:
        ns[propertyName] = newValue

def reboot():
    lprint("reboot command received from server, rebooting...")
    with lock:
        time.sleep(3)
    os.system('sudo reboot')

ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['serverMessageHandlerRunning'] = True
ns['commRunning'] = True

com = comm(Inet=ns['serverAdr'],send_port=ns['serverPort'],listen_port=ns['listenPort'])


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

