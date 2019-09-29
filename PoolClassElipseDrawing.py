# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:23:48 2019

@author: Adminis
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 21:00:02 2019

@author: buiha
"""
""" Import """
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import figure
#import cv2
import time
import multiprocessing 

""" Function decleration """
# Scattering Angle Function
def ScatAng (e1,e2):
    temp = 1-(0.511*(e1-e2))/(e1*e2)
    return temp

# Cone Axis Direction Function
def conedir (x,y):
    #dis = math.sqrt((x[0]-y[0])**2+(x[1]-y[2])**2+x(x[2]-y[2])**2) 
    sumt = 0
    for i in range (0, len(x)):
        temp1 = float(x[i])
        temp2 = float(y[i])
        sumt = sumt + (temp1 - temp2)**2
    dis = math.sqrt(sumt)
    return dis

# Elipse Drawing Function
def ElipseDrawing (coAngle):
    planez0 = np.zeros((512,512),'uint16')
    x0 = -51.1
    y0 = -51.1
    global z
    global x1, y1, z1, u2x, u2y, u2z
    ck = 0
    global costheta
    for i in range (0,len(costheta)):
        if(coAngle==costheta[i]):
            k=i
    for i in range (0,512):
        x = i*0.2+x0
        for j in range (0,512):
            y = j*0.2+y0 
            if (coAngle>0.1):
                left = ((x-x1[k])*(u2x[k])+(y-y1[k])*(u2y[k])+(z-z1[k])*(u2z[k]))**2
                left = int(left)
                right = (coAngle**2)*(((x-x1[k])**2+(y-y1[k])**2+(z-z1[k])**2)*((u2x[k])**2+(u2y[k])**2+(u2z[k])**2))
                right = int(right)
                if (abs(left-right)<2):
                    ck +=1
                    planez0[i,j]=planez0[i,j]+500
    return planez0

""" Variable decleration """
inputfile = '15.kq-recondat'

data = []
linecnt = 0
with open (inputfile, 'r') as file:
    for line in file:
        line = line.strip()                         
        data.append(line)
        linecnt +=1
file.close()

costheta = []
dircone = []
x1 = []
y1 = []
z1 = []
x2 = []
y2 = []
z2 = []
cosbeta = []
for k in range (0,len(data)):
    if(k%2==0):
        # Calculation of Compton Angle
        # Data on first plane
        plane1 = data[k].split()
        x1.append(float(plane1[1]))               # x position
        y1.append(float(plane1[2]))               # y position
        z1.append(float(plane1[3]))               # z position
        e1 = float(plane1[7])               # Energy
        plane2 = data[k+1].split()
        x2.append(float(plane2[1]))               # x position
        y2.append(float(plane2[2]))               # y position
        z2.append(float(plane2[3]))               # z position
        e2 = float(plane2[7])               # Energy
        # Calculation of scattering angle
        theta = ScatAng(e1, e2)
        costheta.append(np.float16(theta))

# Direction Vector
u1x = []
u1y = []
u1z = []
# Scattering Vector
u2x = []
u2y = []
u2z = []    
for i in range (0,len(x1)):
    # Scattering Vector
    temp1 = np.float16(abs(x1[i]-x2[i]))
    temp2 = np.float16(abs(y1[i]-y2[i]))
    temp3 = np.float16(abs(z1[i]-z2[i]))
    tmax = max(temp1, temp2, temp3)
    if (tmax!=0):
        temp1 = temp1/tmax
        temp2 = temp2/tmax
        temp3 = temp3/tmax
    if (tmax==0):
        temp1 = 0
        temp2 = 0
        temp3 = 1
    u2x.append(temp1)
    u2y.append(temp2)
    u2z.append(temp3)

ck = 0
z = 45

""" Reconstruction Process """
planez0 = np.zeros((512,512),'uint16')
t1 = time.time()
#planez0 = ElipseDrawing(x1,y1,z1,u2x,u2y,u2z,costheta,z)
if __name__ == '__main__':
    
    starttime = time.time()
    pool = multiprocessing.Pool(40)
    result = pool.map(ElipseDrawing, costheta)
    pool.close()
print('Elipse Calculation time = ',(time.time()-t1))
           
for i in range (0,len(result)):
        planez0 = planez0 + result[i]

#cv2.imshow('img',planez0)
fig, ax = plt.subplots()
im = ax.imshow(planez0,origin='lower', extent=[-51.1, 51.2, -51.1,51.2])
plt.show()
 

""" Reconstruction Process """
"""
planez0 = np.zeros((512,512),'uint16')
for k in range (1,len(costheta)):
    for i in range (0,512):
        x = i*0.2+x0
        for j in range (0,512):
            y = j*0.2+y0 
            if (costheta[k]>0.1):
                left = ((x-x1[k])*(u2x[k])+(y-y1[k])*(u2y[k])+(z-z1[k])*(u2z[k]))**2
                left = int(left)
                right = (costheta[k]**2)*(((x-x1[k])**2+(y-y1[k])**2+(z-z1[k])**2)*((u2x[k])**2+(u2y[k])**2+(u2z[k])**2))
                right = int(right)
                if (abs(left-right)<2):
                    ck +=1
                    planez0[i,j]=planez0[i,j]+100
"""   