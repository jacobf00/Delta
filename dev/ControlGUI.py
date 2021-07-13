from math import exp
import tkinter as tk
from tkinter.ttk import *
#from Delta import db
"""
f = 6.25 #fixed base radius (in)
rf = 7.98 #Bicep length (in)
re = 25 #Forearm length (in)
r = 2.3125  #end effector radius (in)
speed = 24 #bot speed (in/s)

Delta = db(f,rf,re,r,speed)
"""
root = tk.Tk()
root.title('Delta Control')

window_width = 700
window_height = 500

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

def home():
    print("Delta homed")
    #Delta.home()

def move():
    print("Delta moved")
    #Delta.move()

btn1 = Button(root,text="Home",command=home)
btn1.pack(ipadx=100,ipady=40,expand=False)

btn2 = Button(root,text="Move",command=move)
btn2.pack(ipadx=100,ipady=40,pady=20,expand=False)



x = tk.StringVar()
entx = Entry(root,text="x",textvariable=x)
entx.pack(ipadx=5,ipady=5,side='left',expand=True)
entx.insert(0,"X")

y = tk.StringVar()
enty = Entry(root,text="y",textvariable=y)
enty.pack(ipadx=5,ipady=5,side='left',expand=True)
enty.insert(0,"Y")

z = tk.StringVar()
entz = Entry(root,text="z",textvariable=z)
entz.pack(ipadx=5,ipady=5,side='left',expand=True)
entz.insert(0,"Z")

root.mainloop()