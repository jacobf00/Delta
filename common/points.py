import math
#import matplotlib.pyplot as plt

class points:

    def __init__(self):
        self.pf = []
        self.c = []
        
    def pointfield(self,length,width,xpoints,ypoints,z0):
        points = []
        for y in range(ypoints):
            for x in range(xpoints):
                xcoord = x*(length/(xpoints-1))
                ycoord = y*(width/(ypoints-1))
        
                points.append([xcoord,ycoord,z0])
        self.pf = points
        return points

    def pfShift(self,xshift,yshift,zshift):
        newpf = []
        for p in self.pf:
            p[0] += xshift
            p[1] += yshift
            p[2] += zshift
            newpf.append([p[0],p[1],p[2]])
        self.pf = newpf
        return self.pf

    def circle(self,r,x0,y0,z0):
        points = []
        z = z0
        numpoints = 200
        step  = (2*math.pi)/numpoints

        for p in range(numpoints):
            x = r*math.cos(p*step) + x0
            y = r*math.sin(p*step) + y0

            points.append([x,y,z])

        self.c = points
        return points



