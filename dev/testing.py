import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import threading
import time

point  = np.array([0, 0, -20])
normal = np.array([0, 0, 1])

point2 = np.array([10, 50, 50])

# a plane is a*x+b*y+c*z+d=0
# [a,b,c] is the normal. Thus, we have to calculate
# d and we're set
d = -point.dot(normal)

# lengthStart = -22
# lengthEnd = 22
# widthStart = -12
# widthEnd = 12

# xx,yy = np.meshgrid(range(lengthStart,lengthEnd+1),range(widthStart,widthEnd+1))

# # calculate corresponding z
# z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]

# fig = plt.figure()
# ax = fig.add_subplot(1,1,1, projection='3d')


# ax.plot_surface(xx,yy,z,alpha=.2)

# plt.show()

# print('xs = \n',xx,'\n')
# print('ys = \n',yy,'\n')
# print('zs = \n',z)

# ls = []
# sum = 0

# for i in range(1000):
#     if i % 3 == 0 or i % 5 == 0:
#         ls.append(i)
#         sum += i

# print(sum)

# curPath = os.path.dirname(__file__)

# newPath = os.path.relpath(r'C:\Users\function\Documents\Delta\data\key.key',curPath)

# def showNum(num=1) -> int:
#     with open(newPath,'rb') as file:
#         key = file.read()
#     print(key)
#     return num

# num = showNum(5)
# print(num)

# nums = '1,2,3'
# print(nums.split(sep=','))

# lock = threading.Lock()
    
# def lprint(*a,**b):
#     time.sleep(5)
#     with lock:
#         print(*a,**b)

# def showNums():
#     nums = 12414
#     lprint("numbers are" + str(nums) + " " + str(1))

# t1 = threading.Thread(target=lprint,args=("hello" + "world"))
# t1.start()

# with lock:
#     print("should print first")

# class test:

#     print("hello world")

#     def __init__(self) -> None:
#         print("hello init")

# #test1 = test()

nums = [[1,2,3],[3,2,1]]

def numPrint(num1,num2,num3):
    print(num1 + num2 + num3)

for num in nums:
    for i in num:
        i += 1
        print(i)

print(nums)
