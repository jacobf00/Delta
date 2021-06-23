import os
from Delta import db
from adafruit_servokit import ServoKit
import time
import csv

class TableError(Exception):
    '''The csv file for holding the ranges did not exist'''
    pass

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

def createServoRanges(filePath):
    header = ['min','max']
    with open(filePath,'w') as newFile:
        writer = csv.writer(newFile,lineterminator='\n')
        for i in range(4):
            if i == 0:
                writer.writerow(header)
            else:
                writer.writerow([0,180])

        

servoNum = int(input("Which Servo are you calibrating?(0-2) "))
minOrMax = input("Are you finding the min or max?(no capitals) ")

mainLoop = True
while mainLoop:

    thetas = input("MAKE SURE YOU EXIT WHEN MIN/MAX IS FOUND\ninput theta: ")
    thetas = thetas.split(sep=" ")
    #print(thetas)
    if len(thetas) == 3:
        theta1 = thetas[0]
        theta2 = thetas[1]
        theta3 = thetas[2]
        try:
            kit.servo[ServoAdr0].angle = float(thetas[0])
        except:
            print(f"Servo {ServoAdr0} is unaddressable")
        try:
            kit.servo[ServoAdr1].angle = float(thetas[0])
        except:
            print(f"Servo {ServoAdr1} is unaddressable")
        try:
            kit.servo[ServoAdr2].angle = float(thetas[0])
        except:
            print(f"Servo {ServoAdr2} is unaddressable")
    elif thetas[0] == "exit":
        mainLoop = False
    else:
        try:
            kit.servo[ServoAdr0].angle = float(thetas[0])
        except:
            print(f"Servo {ServoAdr0} is unaddressable")
        try:
            kit.servo[ServoAdr1].angle = float(thetas[0])
        except:
            print(f"Servo {ServoAdr1} is unaddressable")
        try:
            kit.servo[ServoAdr2].angle = float(thetas[0])
        except:
            print(f"Servo {ServoAdr2} is unaddressable")
        lastTheta = float(thetas[0])

#will order servos 0 through 2 ranges on lines 2-4 of csv

try:
    rowNum = 0
    filePath = "data/servo_ranges.csv"
    newFilePath = "data/servo_rangesnew.csv"
    with open(filePath,'r') as servoRanges:
        reader = csv.DictReader(servoRanges)
        header = reader.fieldnames
        with open(newFilePath,'w') as writeFile:
            writer = csv.DictWriter(writeFile,fieldnames=header,lineterminator='\n')
            writer.writeheader()
            for row in reader:
                rowNum += 1
                #print(row)
                if rowNum-1 == servoNum:
                    row[minOrMax] = str(lastTheta)
                    print(f"Servo {servoNum} {minOrMax} was updated")
                writer.writerow(row)
    os.remove(filePath)
    os.rename(newFilePath,filePath)

except FileNotFoundError:
    createServoRanges(filePath=filePath)
    print("Table created, nothing updated.\nTry again")
    #raise TableError()

