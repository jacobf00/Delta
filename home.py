from Delta import db
import time
#from adafruit_servokit import ServoKit


f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)


Delta1 = db(f,rf,re,r,botSpeed=5)

Delta1.home()