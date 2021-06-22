from Delta import db
from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

ServoAdr0 = 0
ServoAdr1 = 1
ServoAdr2 = 2

f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)
speed = 24 #bot speed (in/s)

Delta = db(f,rf,re,r)

mainLoop = True
while mainLoop:

    thetas = input("input theta1 theta2 theta3: ")

    thetas = thetas.split(sep=" ")
    print(thetas)
    if len(thetas) == 3:
        theta1 = thetas[0]
        theta2 = thetas[1]
        theta3 = thetas[2]

        kit.servo[ServoAdr0].angle = float(theta1)
        kit.servo[ServoAdr1].angle = float(theta2)
        kit.servo[ServoAdr2].angle = float(theta3)
    elif thetas[0] == "exit":
        mainLoop = False
    else:
        kit.servo[ServoAdr0].angle = float(thetas[0])
        kit.servo[ServoAdr1].angle = float(thetas[0])
        kit.servo[ServoAdr2].angle = float(thetas[0])