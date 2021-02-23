#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Richard Li
#
# Created:     11/02/2021
# Copyright:   (c) Richard Li 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import random
from PIL import Image

down = 300
up = 300
#center is the remaining probability

#generates random list of points
pointlist = []

x = 0
y = 1000

for i in range (0, 5000):
    where = random.randint(0, 1000)
    pointlist.append([x, y])
    if where <= up:
        y += 1
    elif where <= (up+down):
        y -= 1
    x += 1


MyImg =Image.new('RGB', (5000, 2000), "white")
pixels = MyImg.load()
for a in pointlist:
    pixels[a[0], a[1]] = (0, 0, 0)
MyImg.show()
MyImg.save('graph.jpg', quality=95)














