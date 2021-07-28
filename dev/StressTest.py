import time
import csv
import numpy as np
import threading
from common.Delta import db

f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)
speed = 24 #bot speed (in/s)

Delta1 = db(f,rf,re,r,botSpeed=speed)

def moveServo(deg):

    thetas = (deg,deg,deg)

    Delta1.setAngles(thetas)

    
seconds = 0
upTime = 5 #minutes
downTime = 3 #minutes
while 1:
    thread1 = threading.Thread(target=moveServo,args=(-90,))
    thread1.start()
    time.sleep(1)
    thread1.join()

    thread2 = threading.Thread(target=moveServo,args=(90,))
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