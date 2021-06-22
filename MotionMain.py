from Delta import db
import time
from PointField import points
#from adafruit_servokit import ServoKit


f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)
speed = 24 #bot speed (in/s)

Delta1 = db(f,rf,re,r,speed)

def fast(Delta,points,delay):
    for p in points:
        x,y,z = p[0],p[1],p[2]
        Delta.fmove(x,y,z)
        time.sleep(delay)

def controlled(Delta,points):
    for p in points:
        x,y,z = p[0],p[1],p[2]
        Delta.move(x,y,z)

def trays(Delta,points,returnpoint):
    Delta.setSpeed(20)
    for p in points:
        x,y,z = p[0],p[1],p[2]
        Delta.move(x,y,z)
        Delta.retract(5)
        #Delta.retract(-1)
        time.sleep(.1)
        Delta.move(returnpoint[0],returnpoint[1],returnpoint[2])
        Delta.drop()
        #time.sleep(.5)

if __name__ == '__main__':

    length = 18
    width = 15
    xpoints = 7
    ypoints = 3
    z0 = -25

    ps = points()
    ps.pointfield(length,width,xpoints,ypoints,z0)
    ps.pfShift(-length/2,-width/2,0)

    retpoint = (8,0,-18)

    trays(Delta1,ps.pf,retpoint)


