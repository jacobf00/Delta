from common.Delta import db
from common.points import points
import os
import time
from common.lock_print import *

'''contains initialized objects vital for the program along with general methods used by program'''



ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['serverMessageHandlerRunning'] = True
ns['commRunning'] = True
ns['encryptionEnabled'] = True



f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)
speed = 5 #bot speed (in/s)

Delta1 = db(f,rf,re,r,botSpeed=speed,servo_velocity_control=True)

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

