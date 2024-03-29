#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     tests the code with a known fractal
#
# Author:      Richard Li
#
# Created:     11/02/2021
# Copyright:   (c) Richard Li 2021
# Licence:     MIT License (see LICENSE file)
#-------------------------------------------------------------------------------
import random
import math
import time
import numpy
from PIL import Image

start = time.time()

#this code was taken from stack exchange, and creates a koch snowflake
def kochenize(a,b):
    HFACTOR = (3**0.5)/6
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    mid = ( (a[0]+b[0])/2, (a[1]+b[1])/2 )
    p1 = ( a[0]+dx/3, a[1]+dy/3 )
    p3 = ( b[0]-dx/3, b[1]-dy/3 )
    p2 = ( mid[0]-dy*HFACTOR, mid[1]+dx*HFACTOR )
    return p1, p2, p3

def koch(steps, width):
    arraysize = 4**steps + 1
    points = [(0.0,0.0)]*arraysize
    points[0] = (-width/2., 0.0)
    points[-1] = (width/2., 0.0)
    stepwidth = int(arraysize - 1)
    for n in range(steps):
        segment = int((arraysize-1)/stepwidth)
        for s in range(segment):
            st = int(s*stepwidth)
            a = (points[st][0], points[st][1])
            b = (points[int(st+stepwidth)][0], points[int(st+stepwidth)][1])
            index1 = int(st + (stepwidth)/4)
            index2 = int(st + (stepwidth)/2)
            index3 = int(st + ((stepwidth)/4)*3)
            result = kochenize(a,b)
            points[index1], points[index2], points[index3] = result
        stepwidth /= 4
    return points

TOTALWIDTH = 16384

#the rest of the code was not taken from stack exchange

notpointlist = koch(10, TOTALWIDTH)
pointlist = []
for a in notpointlist:
    bruh0 = a[0]
    bruh1 = a[1]
    pointlist.append([bruh0+8192, bruh1])

framesize = [32768, 32768]

#boxsize is distance from center to edges
def checkboxes(boxsize, pointlist):
    #number of boxes which will be created in each direction
    xboxnum = int(framesize[0]/(boxsize*2))
    yboxnum = int(framesize[1]/(boxsize*2))
    boxlist = []
    #creates boxes
    for i in range (xboxnum):
        addtoboxlist = [2*i*boxsize+boxsize]
        for j in range (yboxnum):
            addtoboxlist.append([2*j*boxsize+boxsize, False])
        boxlist.append(addtoboxlist)
    #initializes previousx and previousy (purpose of these variables is in a later comment)
    previousx = 0
    previousy = 0
    #looks through points, and checks to see if they are in a box
    for a in pointlist:
        for b in range ((previousx-2), (previousx+3)):
            for c in range ((previousy-2), (previousy+3)):
                #makes sure nothing weird is happening with b and c
                if b >= 0  and b <= xboxnum:
                    if c >= 1 and c <= yboxnum:
                        x = boxlist[b][0]
                        y = boxlist[b][c][0]
                        #checks if point is in box
                        if a[0] >= (x-boxsize):
                            if a[0] <= (x+boxsize):
                                if a[1] >= (y-boxsize):
                                    if a[1] <= (y+boxsize):
                                        #marks the box the point is in as being "True"
                                        boxlist[b][c][1] = True
                                        break
            else:
                continue
            break
        #we know that the next point of the random walk will be near the current point, which means that we only have to check boxes relatively near the current point in order to have checked all boxes possible for the next point to be in; this significantly improves the speed of the program, instead of checking if the point is in every single box
        previousx = b
        previousy = c

    #counts how many boxes there are points in, and returns a list of points to be highlighted
    highlightedpointlist = []
    counter = 0
    for b in boxlist:
        for c in b:
            if isinstance(c, float):
                pass
            else:
                if c[1] == True:
                    counter += 1
    return [counter, highlightedpointlist]

#delogged data to analyze
boxnumlist = []
for i in range (2, 13):
    boxsize = 32768/(2**i)
    #we take log base 2 of all the numbers, then do a linear regression, in order to find an exponential regression of the data as a whole
    #this means that we can just use i as the x axis, instead of messing around with exponents and logs here
    boxscale = i
    numberofboxestouched = checkboxes(boxsize, pointlist)
    boxnumlist.append([boxscale, math.log2(numberofboxestouched[0])])

#linear regression on delogged data
#see Griswold's notes on linear regression
#this part of the code finds the SSR, and creates the first quadratic equation
linearTerm = 0
aCoefficient = 0
bCoefficient = 0
abCoefficient = 0
a2Coefficient = 0
b2Coefficient = 0
for i in boxnumlist:
    x = i[0]
    y = i[1]
    linearTerm += y**2
    aCoefficient += 2*(-x)*y
    bCoefficient += 2*(-y)
    abCoefficient += 2*x
    a2Coefficient += x**2
    b2Coefficient += 1
#solve with a variable, b constant
aCoefficient1 = 2*a2Coefficient
bCoefficient1 = abCoefficient
linearTerm1 = -aCoefficient
#solve with b variable, a constant
aCoefficient2 = abCoefficient
bCoefficient2 = 2*b2Coefficient
linearTerm2 = -bCoefficient
#solve system of equations
LCM = numpy.lcm(aCoefficient1, aCoefficient2)
aMultiplier1 = LCM/aCoefficient1
aMultiplier2 = LCM/aCoefficient2
newBCoefficient1 = bCoefficient1*aMultiplier1
newBCoefficient2 = bCoefficient2*aMultiplier2
newLinearTerm1 = linearTerm1*aMultiplier1
newLinearTerm2 = linearTerm2*aMultiplier2
newereBCoefficient = newBCoefficient1-newBCoefficient2
newerLinearTerm = newLinearTerm1-newLinearTerm2
b = newerLinearTerm/newereBCoefficient

extranewLinearTerm1 = bCoefficient1*b
extranewACoefficient = aCoefficient1
extranewLinearTerm2 = linearTerm1
a = (extranewLinearTerm2-extranewLinearTerm1)/extranewACoefficient

print("Fractal dimension: ", a)
print(boxnumlist)
print("Time taken: ", time.time()-start)












