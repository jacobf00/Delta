from common.delta import db
import os
import time
from common.points import points
from pathlib import Path
import csv
#from adafruit_servokit import ServoKit

class motion:

    path = Path(os.path.dirname(__file__))
    path = path.parent.absolute()
    path = path.joinpath('data','calibration_point.csv')
        
    def fast(Delta:db,points,delay):
        for p in points:
            x,y,z = p[0],p[1],p[2]
            Delta.fmove(x,y,z)
            time.sleep(delay)

    def controlled(Delta:db,points):
        for p in points:
            x,y,z = p[0],p[1],p[2]
            Delta.move(x,y,z)

    def trays(Delta:db,tray_length:float,tray_width:float,xpoints:float,ypoints:float,z0:float,
              returnpointx:float,returnpointy:float,returnpointz:float,
              calibrationx:float,calibrationy:float,calibrationz:float,
              retraction_distance:float=4,delta_speed:float=0,local_calibration:bool=False
              ):
        #calibration point needs to be coordinates of first bottle that would be picked up in trays program
        if local_calibration:
            with open(motion.path) as file:
                reader = csv.DictReader(file)
                for row in reader:
                    x,y,z = float(row['x']),float(row['y']),float(row['z'])
                    calibrationPoint = (x,y,z)
        else:
            calibrationPoint = (calibrationx,calibrationy,calibrationz)
        ps = points()
        ps.pointField(tray_length,tray_width,xpoints,ypoints,z0)
        #this is assuming robot is mounted exactly in the center of the tray
        ps.pfShift(-tray_length/2,-tray_width/2,0)
        first_point = ps.pf[0]
        xdiff,ydiff,zdiff = calibrationPoint[0] - first_point[0],calibrationPoint[1] - first_point[1],calibrationPoint[2] - first_point[2]
        ps.pfShift(xdiff,ydiff,zdiff)
        if delta_speed > 0:
            Delta.setSpeed(delta_speed)
        for p in ps.pf:
            x,y,z = p[0],p[1],p[2]
            Delta.move(x,y,z)
            Delta.retract(retraction_distance)
            #Delta.retract(-1)
            time.sleep(.1)
            Delta.move(returnpointx,returnpointy,returnpointz)
            Delta.drop()
            #time.sleep(.5)

if __name__ == '__main__':
    
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
    ps.pointField(length,width,xpoints,ypoints,z0)
    ps.pfShift(-length/2,-width/2,0)

    retpoint = (12,0,-18)

    motion.trays(Delta1,length,width,xpoints,ypoints,z0,retpoint[0],retpoint[1],retpoint[2])


