from adafruit_servokit import ServoKit
import time
import csv
import numpy as np
import threading

class TableError(Exception):
    '''The csv file for holding the ranges did not exist'''
    pass

kit = ServoKit(channels=16)

ServoAdr0 = 0
ServoAdr1 = 1
ServoAdr2 = 2

def moveServo(deg):
    try:
        kit.servo[ServoAdr0].angle = deg
    except:
        print(f"Servo {ServoAdr0} is unaddressable")
    try:
        kit.servo[ServoAdr1].angle = deg
    except:
        print(f"Servo {ServoAdr1} is unaddressable")
    try:
        kit.servo[ServoAdr2].angle = deg
    except:
        print(f"Servo {ServoAdr2} is unaddressable")

    
seconds = 0
upTime = 5 #minutes
downTime = 3 #minutes
while True:
    thread1 = threading.Thread(target=moveServo(180))
    thread1.start()
    time.sleep(1)
    thread1.join()

    thread2 = threading.Thread(target=moveServo(9))
    thread2.start()
    time.sleep(1)

    thread2.join()

    seconds += 2

    if seconds > (upTime*60):
        time.sleep(downTime*60)
        seconds = 0


    
    
    
    # for ang in np.arange(9,180,.2):

    #     kit.servo[ServoAdr2].angle = ang
    #     #time.sleep(.00001)
    # for ang2 in np.arange(180,9,-.2):
    #     kit.servo[ServoAdr2].angle = ang2
    #     #time.sleep(.00001)
        

# with open('sample.csv','r') as file:
#     reader = csv.reader(file,delimiter=',')
#     count = 0
#     with open(r'data\test.csv','w') as newFile:
#         writer = csv.writer(newFile,lineterminator='\n')
#         for row in reader:
#             count += 1
#             if count > 1:
#                 row[0] = "John Stamos"
#             writer.writerow(row)