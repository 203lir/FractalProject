#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     This program tests the linear regression part of the program in module1, in order to make sure it is working as intended
#
# Author:      Richard Li
#
# Created:     03/03/2021
# Copyright:   (c) Richard Li 2021
# Licence:     MIT License (see LICENSE file)
#-------------------------------------------------------------------------------
import numpy

#this data was taken from Griswold's notes
boxnumlist = [[0, 2], [1, -1], [3, -2]]

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

print(a)
print(b)