import time
import pyautogui as pgui
import pygame
from Delta import db

f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)

Delta1 = db(f,rf,re,r)


xsize,ysize = pgui.size()

def trans(xp,yp,length,width):
    #find specified xy range allowed of bot movement
    botxmin = -length/2
    botymin = -width/2
    #find slopes to linearly interpolate
    xslope = length/xsize
    yslope = width/ysize

    xf = xslope*xp + botxmin
    yf = yslope*yp + botymin

    return xf, yf
    


def MouseTracking(length,width):

    pygame.init()
    window = pygame.display.set_mode((1367, 730))
    pygame.display.set_caption("Delta Mouse Control")

    zpos = -20

    mloop = True
    while mloop:

        for event in pygame.event.get():
            
            #map cursor position to equivalent delta position
            xp,yp = pgui.position()
            print(pgui.position())
            xpos,ypos = trans(xp,yp,length,width)
            



            if event.type==pygame.QUIT:

                mloop=False

            if event.type == pygame.KEYDOWN:

                print(pygame.key.name(event.key))
                if event.key == pygame.K_e:
                    mloop=False
                
                if event.key == pygame.K_q:
                    print("Up")
                    zpos +=.5

                if event.key == pygame.K_z:
                    print("down")
                    zpos -=.5


            if event.type==pygame.MOUSEBUTTONDOWN:
                print("Mouse Button is pressed")
                Delta1.drop()
                

            Delta1.fmove(xpos,ypos,zpos)
        time.sleep(.01)

    pygame.quit()
                
MouseTracking(36,36)

