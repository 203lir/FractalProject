#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
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

print("MIT License")
print("")
print("Copyright © 2021 Richard Li")
print("")
print("Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:")
print("")
print("The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.")
print("")
print("THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.")
print("")
print("")
print("Running...")

up = 400
down = 400
#center is the remaining probability

#generates random list of points
pointlist = []

x = 0
y = 32768

for i in range (0, 32768):
    where = random.randint(0, 1000)
    pointlist.append([x, y])
    if where <= down:
        y += 1
    elif where <= (up+down):
        y -= 1
    x += 1

framesize = [32768, 65536]

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
    previousy = int(yboxnum/2)
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
                    for i0 in range (int(b[0]-boxsize), int(b[0]+boxsize)):
                        for i1 in range (int(c[0]-boxsize), int(c[0]+boxsize)):
                            if i0+1 < 1024:
                                if i1 > 31745 and i1-1 < 33793:
                                    highlightedpointlist.append([i0+1, i1-31745])
    return [counter, highlightedpointlist]

#creates image
def createimage (pointlist, highlightedpointlist, name):
    MyImg = Image.new('RGB', (1024, 2048), "white")
    pixels = MyImg.load()

    scaledpointlist = []
    #cuts off most of the data, since otherwise the image would be huge and unusable
    for n in pointlist:
        if n[0] < 1024:
            scaledpointlist.append([n[0], n[1]-31744])

    for b in numberofboxestouched[1]:
        pixels[b[0], b[1]] = (250, 200, 21)

    for a in scaledpointlist:
        pixels[a[0], a[1]] = (0, 0, 0)

    imagename = name + ".jpg"
    MyImg.save(imagename, quality=95)

#delogged data to analyze
boxnumlist = []
for i in range (6, 15):
    boxsize = 32768/(2**i)
    #we take log base 2 of all the numbers, then do a linear regression, in order to find an exponential regression of the data as a whole
    #this means that we can just use i as the x axis, instead of messing around with exponents and logs here
    boxscale = i
    numberofboxestouched = checkboxes(boxsize, pointlist)
    #a bit inefficient getting a list of points first then creating an image, but this can be solved "in hardware"
    createimage(pointlist, numberofboxestouched[1], str(i-6))
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
#print(boxnumlist)
print("Time taken: ", time.time()-start)












