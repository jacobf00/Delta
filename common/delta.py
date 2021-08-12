#author: Jacob Foulds
import math
import numpy as np
import time
import piplates.RELAYplate as RELAY
#from dev.ServoTest import filePath
#import csv
import threading
from common.servo_service import servo
from common.config import *

#Set custom Delta exception(s)
class SpeedError(Exception):
    pass

class ServoAdrError(Exception):
    pass

#construct deltabot class
class db:

    def __init__(self, FixedBaseRadius, Bicep, Forearm, EndEffectorRadius,
                 botSpeed:float=12,servo_velocity_control=True,servo_ids:tuple=(1,2,3),angle_range:float=90
                ):
        self.f = FixedBaseRadius
        self.rf = Bicep
        self.re = Forearm
        self.r = EndEffectorRadius
        self.servoVelocityControl = servo_velocity_control
        self.servoIds = servo_ids
        #position increment in inches
        self.inc = .2 #in
        self.setSpeed(botSpeed) #in/s
        self.dlay = self.inc/self.speed #time delay between points
        self.thetaDiff = 0 #deg
        self.theta0 = [180,180,180] #deg
        self.angle_range = angle_range
        #initialize servos
        # self.minServo = 0
        # self.maxServo = 180
        self.updateServoRange()
        self.createServos()

    def createServos(self):
        try:
            self.servo1 = servo(Dynamixel_ID=self.servoIds[0])
        except:
            print("servo 1 could not be connected successfully")
        try:
            self.servo2 = servo(Dynamixel_ID=self.servoIds[1])
        except:
            print("servo 2 could not be connected successfully")
        try:
            self.servo3 = servo(Dynamixel_ID=self.servoIds[2])
        except:
            print("servo 3 could not be connected successfully")
        self.servo1.setProfileVelocity(0)
        self.servo2.setProfileVelocity(0)
        self.servo3.setProfileVelocity(0)
            
            
    def updateServoRange(self):
        #list is ordered servos 0-2 on indices 0-2
        self.minServos = []
        self.maxServos = []
        self.minServos = [0,0,0]
        self.maxServos = [4095,4095,4095]
        # with open(filePath,'r') as servoRanges:
        #     reader = csv.DictReader(servoRanges)
        #     for row in reader:
        #         self.minServos.append(int(row['min']))
        #         self.maxServos.append(int(row['max']))

    def enableTorque(self):
        self.servo1.enableTorque()
        self.servo2.enableTorque()
        self.servo3.enableTorque()

    def disableTorque(self):
        self.servo1.disableTorque()
        self.servo2.disableTorque()
        self.servo3.disableTorque()


    def setServoAdr(self,servo,adr):
        try:
            servo = int(servo)
            adr = int(adr)
        except:
            raise ServoAdrError(f"Seriously? what kind of address is {adr}?")

        if int(servo) == 0:
            self.ServoAdr0 = adr
        elif int(servo) == 1:
            self.ServoAdr1 = adr
        elif int(servo) == 2:
            self.ServoAdr2 = adr

    def setInc(self,newincrement):
        self.inc = newincrement
        try:
            self.dlay = self.inc/self.speed
        except:
            raise SpeedError(f"Seriously? what kind of increment is {newincrement}?")

    def setSpeed(self,newspeed):
        self.speed = newspeed
        try:
            self.dlay = self.inc/self.speed
            print(f"Delta speed set to {self.speed} in/s")
        except:
            raise SpeedError(f"Seriously? what kind of speed is {newspeed}?")

    @staticmethod
    def trans(thetaIn:float,realServoMin=0,realServoMax=360,toDegrees=False) -> float:
        if not toDegrees:
            slope = (servo.DXL_MAXIMUM_POSITION_VALUE-servo.DXL_MINIMUM_POSITION_VALUE)/(realServoMax-realServoMin)
            thetaOut = slope*thetaIn + servo.DXL_MINIMUM_POSITION_VALUE
            return thetaOut
        else:
            slope = (realServoMax-realServoMin)/(servo.DXL_MAXIMUM_POSITION_VALUE-servo.DXL_MINIMUM_POSITION_VALUE)
            thetaOut = slope*thetaIn + realServoMin
            return thetaOut

    @staticmethod
    def velTrans(x,y1=servo.DXL_MAXIMUM_VELOCITY_VALUE,y0=servo.DXL_MINIMUM_VELOCITY_VALUE,x1=servo.DXL_MAXIMUM_VELOCITY_VALUE_DEG,x0=servo.DXL_MINIMUM_VELOCITY_VALUE_DEG):
        slope = (y1-y0)/(x1-x0)
        y = slope*(x-x0) + y0
        return y

    @staticmethod
    def drop(seconds = .5):
        if seconds is None:
            RELAY.relayON(0,1)
        else:
            RELAY.relayON(0,1)
            time.sleep(seconds)
            RELAY.relayOFF(0,1)


    def calcAngleYZ(self, x0, y0, z0):

        #find linear constants for solution to circle intersections
        #make sure to choose solution that has more negative y
        y1 = -self.f
        y0 -= self.r
        a = (x0*x0 + y0*y0 + z0*z0 + self.rf*self.rf - self.re*self.re - y1*y1)/(2*z0)
        b = (y1-y0)/z0
        #calculate discriminant first to see if should continue
        d = -(a + b*y1)*(a + b*y1) + self.rf*(b*b*self.rf + self.rf)

        if d < 0:
            raise Exception("Point is outside of bot's reach")

        yj = (y1 - a*b - math.sqrt(d))/(b*b + 1)
        zj = a + b*yj
        #Now calculate theta from these values
        #In this case, theta is defined as the angle clockwise from the horizontal

        theta = (180/math.pi)*math.atan(-zj/(y1-yj)) #calculates theta in degrees
        if yj>y1:
            theta += 180.0
        return theta

    def reverse(self,x0,y0,z0):
        '''Takes x,y,z coordinates and calculates the corresponding theta values for the servo motors.
        returns (0,0,0) if point is not within reach.'''
        sin120 = math.sqrt(3)/2
        cos120 = -1/2 #also equals cos(-120)
        try:
            theta1 = self.calcAngleYZ(x0,y0,z0)
            theta2 = self.calcAngleYZ(x0*cos120 + y0*sin120, -x0*sin120 + y0*cos120,z0) #rotate +120 deg
            theta3 = self.calcAngleYZ(x0*cos120 - y0*sin120, x0*sin120 + y0*cos120,z0) #rotate -120 deg
                    
            return (theta1, theta2, theta3)
        except:
            print("The point is outside of the bot's reach")
            logging.warn(f"Servo angles cannot be calculated for the point given: X: {x0}, Y: {y0}, Z: {z0}")
            toServerQueue.put(f"Servo angles cannot be calculated for the point given: X: {x0}, Y: {y0}, Z: {z0}")
            return (0,0,0)

    def forward(self, theta1, theta2, theta3):
        ''' 
        Takes three servo angles in degrees.  Zero is horizontal.
        return (x,y,z) if point valid, None if not '''
        
        t = self.f-self.r

        theta1, theta2, theta3 = math.radians(theta1), math.radians(theta2), math.radians(theta3)

        # Calculate position of leg1's joint.  x1 is implicitly zero - along the axis
        y1 = -(t + self.rf*math.cos(theta1))
        z1 = -self.rf*math.sin(theta1)

        # Calculate leg2's joint position
        y2 = (t + self.rf*math.cos(theta2))*math.sin(math.pi/6)
        x2 = y2*math.tan(math.pi/3)
        z2 = -self.rf*math.sin(theta2)

        # Calculate leg3's joint position
        y3 = (t + self.rf*math.cos(theta3))*math.sin(math.pi/6)
        x3 = -y3*math.tan(math.pi/3)
        z3 = -self.rf*math.sin(theta3)

        # From the three positions in space, determine if there is a valid
        # location for the effector
        dnm = (y2-y1)*x3-(y3-y1)*x2
    
        w1 = y1*y1 + z1*z1
        w2 = x2*x2 + y2*y2 + z2*z2
        w3 = x3*x3 + y3*y3 + z3*z3

        # x = (a1*z + b1)/dnm
        a1 = (z2-z1)*(y3-y1)-(z3-z1)*(y2-y1)
        b1 = -((w2-w1)*(y3-y1)-(w3-w1)*(y2-y1))/2.0

        # y = (a2*z + b2)/dnm;
        a2 = -(z2-z1)*x3+(z3-z1)*x2
        b2 = ((w2-w1)*x3 - (w3-w1)*x2)/2.0

        # a*z^2 + b*z + c = 0
        a = a1*a1 + a2*a2 + dnm*dnm
        b = 2*(a1*b1 + a2*(b2-y1*dnm) - z1*dnm*dnm)
        c = (b2-y1*dnm)*(b2-y1*dnm) + b1*b1 + dnm*dnm*(z1*z1 - self.re*self.re)
 
        # discriminant
        d = b*b - 4.0*a*c
        if d < 0:
            print(f"Coordinates cannot be calculated for the servo angles given: theta1: {theta1}, theta2: {theta2}, theta3: {theta3}")
            logging.warn(f"Coordinates cannot be calculated for the servo angles given: theta1: {theta1}, theta2: {theta2}, theta3: {theta3}")
            toServerQueue.put(f"Coordinates cannot be calculated for the servo angles given: theta1: {theta1}, theta2: {theta2}, theta3: {theta3}")
            return None # non-existing point

        z0 = -0.5*(b+math.sqrt(d))/a
        x0 = (a1*z0 + b1)/dnm
        y0 = (a2*z0 + b2)/dnm
        return (x0,y0,z0)

    @staticmethod
    def setVelocities(velocities:list):
        vel1 = abs(round(db.velTrans(velocities[0])))
        vel2 = abs(round(db.velTrans(velocities[1])))
        vel3 = abs(round(db.velTrans(velocities[2])))
        servo.bulkWriteVelocities(vel1,vel2,vel3)
        lprint(f"setting servo goal velocities to 1: {round(velocities[0],2)}, 2: {round(velocities[1],2)}, 3: {round(velocities[2],2)} deg/sec")
        print(f"setting servo goal velocities to 1: {vel1}, 2: {vel2}, 3: {vel3} pulse")


    def setAngles(self,thetas:tuple):
        theta0 = round(db.trans(-thetas[0] + self.theta0[0] + self.thetaDiff,0))
        theta1 = round(db.trans(-thetas[1] + self.theta0[1] + self.thetaDiff,1))
        theta2 = round(db.trans(-thetas[2] + self.theta0[2] + self.thetaDiff,2))
        # self.servo1.setPosition(theta0)
        # self.servo2.setPosition(theta1)
        # self.servo3.setPosition(theta2)
        servo.bulkWritePositions(theta0,theta1,theta2)
        lprint(f"setting servo positions to 1: {round(thetas[0],2)}, 2: {round(thetas[1],2)}, 3: {round(thetas[2],2)} deg")

        #time.sleep(self.dlay)

    def setAnglesAndVelocities(self,thetas,velocities):
        db.setVelocities(velocities)
        self.setAngles(thetas)


    def getCurrentAngles(self,transform:bool=True) -> tuple:
        # theta0 = db.trans(thetaIn=self.servo1.readCurrentPosition(),toDegrees=True)
        # theta1 = db.trans(thetaIn=self.servo2.readCurrentPosition(),toDegrees=True)
        # theta2 = db.trans(thetaIn=self.servo3.readCurrentPosition(),toDegrees=True)
        theta0,theta1,theta2 = servo.syncReadPositions()
        newTheta0 = self.theta0[0] - db.trans(theta0,toDegrees=True)
        newTheta1 = self.theta0[1] - db.trans(theta1,toDegrees=True)
        newTheta2 = self.theta0[2] - db.trans(theta2,toDegrees=True)
        if transform:
            return (newTheta0,newTheta1,newTheta2)
        else:
            return (theta0,theta1,theta2)

    def getCurrentPosition(self):
        currentAngles = self.getCurrentAngles()
        currentPosition = self.forward(*currentAngles)
        return currentPosition


    @staticmethod
    def dist(point1,point2):
        distance = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)
        return distance

    def interp(self,point1,point2):
        '''interpolates points between two specified points in set distance increments'''
        points = []

        distance = db.dist(point1,point2) #find distance between points
        numpoints = round(distance/self.inc) #find number of inc dist between points
        if numpoints == 0:
            self.fmove(point2[0],point2[1],point2[2])
            return None
        else:

            #interpolate points between
            xpoints = np.linspace(point1[0],point2[0],numpoints)
            ypoints = np.linspace(point1[1],point2[1],numpoints)
            zpoints = np.linspace(point1[2],point2[2],numpoints)
            #add points to list
            for i in range(len(xpoints)):
                points.append([xpoints[i],ypoints[i],zpoints[i]])

            return points

    def home(self):
        '''Sets the servos to 45 degrees'''
        angle = 45
        # thetas = [self.theta0[0],self.theta0[1],self.theta0[2]]
        # for theta in thetas:
        #     theta += angle

        # self.setAngles(thetas)

        homeAngles = (angle,angle,angle)
        self.setAngles(homeAngles)
        


    def move(self,x:float,y:float,z:float,threshold:float=.5,velocity_multiplier:float=1.2): #threshold in in
        #find the current position from the servo motor angles
        origAngles = self.getCurrentAngles()
        origPos = self.forward(*origAngles)
        newPos = (x,y,z)
        newAngles = self.reverse(*newPos)
        if self.servoVelocityControl:
            diffAngles = [newAngles[0]-origAngles[0],newAngles[1]-origAngles[1],newAngles[2]-origAngles[2]] #angle sweep needed for each servo
            distance = db.dist(origPos,newPos) #distance between current and new position in inches
            dt = distance/self.speed #ideal time between original and new point
            angVelocities = [] #list that contains the ideal average angular velocity of each servo in deg/sec
            for ang in diffAngles:
                angVelocities.append(velocity_multiplier*(ang/dt))
            if (
                newAngles[0] < -self.angle_range or newAngles[1] < -self.angle_range or newAngles[2] < -self.angle_range
                or newAngles[0] > self.angle_range or newAngles[1] > self.angle_range or newAngles[2] > self.angle_range
                ):
                print("Angle is out of range")
                logging.warn(f"Calculated angle is out of defined servo range of {self.angle_range}")
                toServerQueue.put(f"Calculated angle is out of defined servo range of {self.angle_range}")
                thetas = (0,0,0)
                thread1 = threading.Thread(target=self.setAngles,args=(thetas,))
                thread1.start()
                time.sleep(self.dlay)
                thread1.join()
            else:
                t1 = threading.Thread(target=self.setAnglesAndVelocities,args=(newAngles,angVelocities))
                t1.start()
                time.sleep(dt)
                curPos = self.getCurrentPosition()
                if db.dist(curPos,newPos) > threshold:
                    print("servos have not met goal positions in time :(")
                    logging.warn("servos have not met goal positions in time :(")
                    toServerQueue.put(f"End effector did not reach accuracy threshold of {threshold} inches in time")
                elif t1.is_alive():
                    lprint("servo pos thread running when it shouldn't")
                t1.join()
                # self.setVelocities(angVelocities)
                # self.setAngles(newAngles)       
        else:
            points = self.interp(origPos,newPos)

            #now loop through interpolated points
            if points != None:

                for ps in points:
                    thetas = self.reverse(ps[0],ps[1],ps[2])
                    if (
                        thetas[0] < -self.angle_range or thetas[1] < -self.angle_range or thetas[2] < -self.angle_range
                        or thetas[0] > self.angle_range or thetas[1] > self.angle_range or thetas[2] > self.angle_range
                        ):
                        print("Angle is out of range")
                        thetas = (0,0,0)
                        thread1 = threading.Thread(target=self.setAngles,args=(thetas,))
                        thread1.start()
                        time.sleep(self.dlay)
                        thread1.join()
                    else:
                        try: #theta0 and thetaDiff shift angle into servo axes, trans function maps new angle onto calibrated servo range
                            thread1 = threading.Thread(target=self.setAngles,args=(thetas,))
                            thread1.start()
                            time.sleep(self.dlay)
                            thread1.join()
                        except ValueError:
                            print("shitty servo no go brrrrrr")


    def fmove(self,x,y,z):
        '''method for moving the servos to point instantly (fast move)'''
        thetas = self.reverse(x,y,z)
        try:
            self.setAngles(thetas)
        except:
            print("shitty servo no go brrrrrr")
            logging.warn("servo fast move failed")


    def retract(self,retraction_distance:float=4):
        ret = retraction_distance
        #find current position
        pos = self.forward(*self.getCurrentAngles())
        #add retraction distance to position
        newposz = pos[2] + ret
        self.move(pos[0],pos[1],newposz)

    
        





    




