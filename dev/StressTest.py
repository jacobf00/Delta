import time
import threading
from common.delta import db

f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)
speed = 24 #bot speed (in/s)

Delta1 = db(f,rf,re,r,botSpeed=speed)

def moveServo(deg):

    thetas = (deg,deg,deg)
    threshold = .8 #10 pulse, roughly .8 deg
    Delta1.setAngles(thetas)
    notPrecise = True
    while notPrecise:
        positions = Delta1.getCurrentAngles()
        for pos in positions:
            if abs(pos-deg) < threshold:
                print("Goal is met at: " + str(thetas) + ", current angles are " + str(positions))
                notPrecise = False


    
seconds = 0
upTime = 5 #minutes
downTime = 3 #minutes
curTime = 0
while 1:
    startTime1 = time.time()
    moveServo(-90)
    moveTime = time.time() - startTime1

    startTime2 = time.time()
    moveServo(90)
    moveTime += time.time()-startTime2

    if moveTime > (upTime*60):
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