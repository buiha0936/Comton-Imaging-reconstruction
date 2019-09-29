# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 21:37:51 2019

@author: buiha
"""

import numpy as np

linecnt = 0
                                # Checking final line in the history block
data = []
datftl = []                                     # Filtered data
datftl1 = []
output = []
output1 = []
zsur = []
colide = []
output2 = []
fall = []

npsdat = []
surck = 0
collck = 0
collcnt = 0
terck = 0
finck = 0
npsck = 0
lastck = 0
zsur = 0
zter = 0
right1 = right2 = 0
planedis = 4.0                    # KC 2 tam
planepos = 9.5                   # Toa do tam 2

linksource = '/home/HDD_4T1/DUONG/NaI/'
linkResult = '/home/HDD_4T1/DUONG/Results/NaI/Recondat/'
inputfile = '17.kq'
with open(linksource+inputfile, 'r') as file:
    for line in file:   
        line = line.strip()  
        temp = line.split()                        
        data.append(line)
        if (linecnt>9):
            if (npsck==0):                                                   # Checking nps line
                 if (temp[0]!='3000' and temp[0]!='4000' and temp[0]!='5000' and temp[0]!='9000'):
                     npsck = 1
                     datftl.append('npsline' + "\t" + temp[0] + "\t" + temp[1] + "\t" + temp[2])
                     
            if (linecnt-surck==1):                                             # Surface data line
                datftl.append('3000  '+line)                                   # Append surface data
                #surck = 0
            if (linecnt-surck>1):
                if (temp[0]=='3000'):                                          # Checking surface line
                    surck = linecnt
            
            if (linecnt-collck==1):                                            # Collision data
                datftl.append('4000  '+line)                                   # Append Collision data
            if (linecnt-collck>1):
                if (temp[0]=='4000'):                                          # Checking surface line
                    collck = linecnt
                    collcnt +=1                                                # Counting number of scaterring events
                    
            if (linecnt-terck==1):                                             # Terminal data
                datftl.append('5000  '+line)
            if (linecnt-terck>1):                                              # Checking terminal line
                if (temp[0]=='5000'):
                    terck = linecnt
            if ((linecnt-lastck)==1):
                datftl.append('9000   '+line)
                finck = 1
            if (temp[0]=='9000'):                                              # Checking for last event line
                #finck = 1
                lastck = linecnt     
            if (npsck==1):                                                     # Checking end of hisstory
                if (finck==1):
                     npsck=0
                     finck=0
                     surck = 0
                     collck = 0
                     terck = 0
                     collcnt = 0
        linecnt +=1
file.close()
endat = []
posdat = []
ensur = 0
linecnt = 0
collcnt = 0
potrack = 0
colpos1 = 0
for i in range (0,len(datftl)):
    temp = datftl[i].split()
    datftl1.append(datftl[i])
    linecnt +=1
    if (temp[0] == '3000' or temp[0] == '4000'):
        ensur = float(temp[7])                                                 # Marking surface energy
        if (linecnt<=2):
            binsur = float(temp[3])                                            # Marking the first position                                                  
    if (temp[0] == '4000'):
        potrack = abs(float(temp[3])-potrack)
        collcnt +=1
        collck +=1   
        en1 = float(temp[7])                                                   # Marking first Energy  
        if (collcnt==1):
            colpos1 = float(temp[3])                                           # Posirion of the first colission     
                                               
    if (temp[0]=='9000'):
        linecnt = 0
        endsur = float(temp[3])                                                # Marking the last position
        enfin = float(temp[7])                                                   # Marking second energy
        zter = float(temp[3])                                                  # Marking terminal position
        if (ensur==enfin):                                                     # If same energy
            datftl1.clear()
        if ((binsur-endsur)<planedis):
            datftl1.clear()
        collcnt = 0
        if (colpos1<planepos):                                                      # If first colission happened in second detector
            datftl1.clear()
        if (len(datftl1)>0):
            for j in range (0,len(datftl1)):
                output.append(datftl1[j])

# Data array without 3000 line        
for i in range (0,len(output)):
    temp = output[i].split()
    if (temp[0]=='npsline' or temp[0]=='4000' or temp[0]=='5000' or temp[0]=='9000'):
        output1.append(output[i])
    
datftl.clear()
collck = 0
endat.clear()
removevent = 0
for i in range (0,len(output1)):
    temp = output1[i].split()
    datftl.append(output1[i])
    if (temp[0]=='4000'):
        collck +=1
        endat.append(float(temp[7]))
        if (collck==1):                                                        # First Colission
            en1 = float(temp[7])
    if (temp[0]=='9000'):
        collck = 0
        for j in range (2,len(datftl)):
            temp1 = datftl[j].split()
            en2 = float(temp1[7])
            if (en1==en2):
                removevent = 1
        if (removevent==1):
            datftl.clear()
            removevent = 0
        if (len(datftl)>0):
            for j in range(0,len(datftl)):
                output2.append(datftl[j])
            datftl.clear()

output3 = []
datftl.clear()
collck = 0
for i in range (0,len(output2)):
    temp = output2[i].split()
    if (temp[0]=='4000'):
        collck +=1
    if (collck<3 and temp[0]=='4000'):
        datftl.append(output2[i])
    if (temp[0]=='9000'):
        if (collck==2):
            output3.append(datftl[0])
            output3.append(datftl[1])
            datftl.clear()
        else:
            datftl.clear()
        collck = 0
""" Remove Back Scattering Event"""
filterdat = []
for i in range (0,len(output3)):
    if (i%2!=0):
        temp1 = output3[i-1].split()
        temp2 = output3[i].split()
        if (float(temp1[3])>float(temp2[3])):
            filterdat.append(output3[i-1])
            filterdat.append(output3[i])
""" Writing data into file """
with open (linkResult+inputfile+'-recondat','w') as file:
    for i in range (0,len(filterdat)):
        file.write(filterdat[i])
        file.write('\n')
file.close()
print('File ' + inputfile + ' is finished')

        
"""
with open (inputfile+'filter'+'.txt','w') as file:
    for i in range (0,len(output)):
        file.write(output[i])
        file.write('\n')
file.close()
with open (inputfile+'No3000'+'.txt','w') as file:
    for i in range (0,len(output1)):
        file.write(output1[i])
        file.write('\n')
file.close()
with open (inputfile+'final'+'.txt','w') as file:
    for i in range (0,len(output2)):
        file.write(output2[i])
        file.write('\n')
file.close()
"""
