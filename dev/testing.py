import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

point  = np.array([0, 0, -20])
normal = np.array([0, 0, 1])

point2 = np.array([10, 50, 50])

# a plane is a*x+b*y+c*z+d=0
# [a,b,c] is the normal. Thus, we have to calculate
# d and we're set
d = -point.dot(normal)

lengthStart = -22
lengthEnd = 22
widthStart = -12
widthEnd = 12

xx,yy = np.meshgrid(range(lengthStart,lengthEnd+1),range(widthStart,widthEnd+1))

# calculate corresponding z
z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]

fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')


ax.plot_surface(xx,yy,z,alpha=.2)

plt.show()

print('xs = \n',xx,'\n')
print('ys = \n',yy,'\n')
print('zs = \n',z)