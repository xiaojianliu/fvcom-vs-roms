# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 10:18:02 2016

@author: xiaojian
"""
import numpy as np
import datetime as dt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv
drifter_list='drifter_vs_roms use hourly data3.csv'
#mend_list='bar1.csv'
day=3
drifters = np.genfromtxt(drifter_list,dtype=None,names=['ids','lon','lat','s','d'],delimiter=',',skip_header=1)
#mend = np.genfromtxt(mend_list,dtype=None,names=['ids','lon','lat','s','d'],delimiter=',',skip_header=1)   
num=[]
x=[]
for b in np.arange(1,round(max(drifters['s']))+1,1):
    #print b,'##################################'
    aa=0
    x.append(b-1)
    x.append(b)
    for a in np.arange(len(drifters['s'])):
        if drifters['s'][a]>=b-1 and drifters['s'][a]<b:
            aa=aa+1
            #print drifters['s'][a]
    num.append(aa)
    num.append(aa)
num.append(0)
x.append(b)
fig,axes=plt.subplots(2,1,figsize=(6,10))
axes[0].set_title('Separation distance density distribution(%s days)'%day) 
axes[0].plot(x,num,'b-',label='roms',linewidth=1)
axes[0].set_xlabel('km')
axes[0].set_ylabel('number')

num1=[]
x1=[]
for b in np.arange(0.03,round(max(drifters['d'])*100)/float(100),0.03):
    #print b
    aa=0
    x1.append(b-0.03)
    x1.append(b)
    for a in np.arange(len(drifters['d'])):
        if drifters['d'][a]>=b-0.03 and drifters['d'][a]<b:
            aa=aa+1
            
    num1.append(aa)
    num1.append(aa)
num1.append(0)
x1.append(b)
axes[1].set_title('distance ratio density distribution') 
axes[1].set_xlabel('km/km')
axes[1].set_ylabel('number')

#plt.title('drifter_meandis_and_mend_meandis') 
axes[1].plot(x1,num1,'b-',label='roms',linewidth=1)
print '''roms'''
print 'mean',np.mean(drifters['s'])/day
print 'max',np.max(drifters['s'])
print 'min',np.min(drifters['s'])
print 'std',np.std(drifters['s'])
#print np.mean(drifters['s'][drifters['d']<1])
print 'mean',np.mean(drifters['d'])
print 'max',np.max(drifters['d'])
print 'min',np.min(drifters['d'])
print 'std',np.std(drifters['d'])
print '###############################################'
drifter_list='drifter_vs_model use hourly data3.csv'
#mend_list='bar1.csv'
drifters = np.genfromtxt(drifter_list,dtype=None,names=['ids','lon','lat','s','d'],delimiter=',',skip_header=1)
#mend = np.genfromtxt(mend_list,dtype=None,names=['ids','lon','lat','s','d'],delimiter=',',skip_header=1)   
num=[]
x=[]
for b in np.arange(1,round(max(drifters['s']))+1,1):
    #print b,'##################################'
    aa=0
    x.append(b-1)
    x.append(b)
    for a in np.arange(len(drifters['s'])):
        if drifters['s'][a]>=b-1 and drifters['s'][a]<b:
            aa=aa+1
            #print drifters['s'][a]
    num.append(aa)
    num.append(aa)
num.append(0)
x.append(b)
axes[0].plot(x,num,'r-',label='fvcom',linewidth=1)
num1=[]
x1=[]
for b in np.arange(0.03,round(max(drifters['d'])*100)/float(100),0.03):
    #print b
    aa=0
    x1.append(b-0.03)
    x1.append(b)
    for a in np.arange(len(drifters['d'])):
        if drifters['d'][a]>=b-0.03 and drifters['d'][a]<b:
            aa=aa+1
            
    num1.append(aa)
    num1.append(aa)
num1.append(0)
x1.append(b)
axes[0].legend()
axes[1].plot(x1,num1,'r-',label='fvcom',linewidth=1)
axes[1].legend(loc='best')
plt.savefig('roms_vs_fvcomx%s'%day,dpi=200)
plt.show()
print 'mean',np.mean(drifters['s'])/day
print 'max',np.max(drifters['s'])
print 'min',np.min(drifters['s'])
print 'std',np.std(drifters['s'])
#print np.mean(drifters['s'][drifters['d']<1])
print 'mean',np.mean(drifters['d'])
print 'max',np.max(drifters['d'])
print 'min',np.min(drifters['d'])
print 'std',np.std(drifters['d'])
plt.figure()
#plt.title('drifter_meandis_and_mend_meandis') 
#plt.scatter(drifters['lon'][drifters['s']>2*np.mean(drifters['s'])],drifters['lat'][drifters['s']>2*np.mean(drifters['s'])],s=drifters['s'][drifters['s']>2*np.mean(drifters['s'])]*2,color='red')
plt.scatter(drifters['lon'][drifters['s']>10],drifters['lat'][drifters['s']>10],s=drifters['s'][drifters['s']>10]*2,color='red')

#plt.scatter(drifters['lon'],drifters['lat'],s=drifters['d']*10,color='yellow')
plt.show()
plt.figure()
#plt.title('drifter_meandis_and_mend_meandis') 
#plt.scatter(drifters['lon'],drifters['lat'],s=drifters['s'],color='red')
#plt.scatter(drifters['lon'][drifters['d']>2*np.mean(drifters['d'])],drifters['lat'][drifters['d']>2*np.mean(drifters['d'])],s=drifters['d'][drifters['d']>2*np.mean(drifters['d'])]*20,color='green')
plt.scatter(drifters['lon'][drifters['d']>0.4],drifters['lat'][drifters['d']>0.4],s=drifters['d'][drifters['d']>0.4]*20,color='green')

plt.show()
i=0
I=[]
xx=[]
for a in np.arange(len(num1)):
    if a%2==0 and a!=142:
        i=num1[a]+i
        I.append(i/float((sum(num1)/2)))
for a in np.arange(len(x1)):
    if a%2==0 and a!=142:
        
        xx.append((x1[a]+x1[a+1])/float(2))
plt.figure()
plt.plot(xx,I)
II=[]
for a in np.arange(len(I)):
    II.append(1-I[a])
plt.figure()
plt.plot(xx,II)
mm=[]
for a in np.arange(len(num1)):
    if a%2==0 and a!=142:
        mm.append(num1[a]/float(sum(num1)/float(2)))
plt.figure()
plt.plot(xx,mm)
        
'''
dd=[]
dd=drifters['s'][mend['s']>7]-mend['s'][mend['s']>7]
print len(dd)
print len(dd[dd<=0])
new_drifters=[]
new_drifters=drifters['s']
drifters['s'][mend['s']<7]=mend['s'][mend['s']<7]
#new_drifters.append(drifters['s'][mend['s']>=10])
num=[]
x=[]
for b in np.arange(1,round(max(drifters['s']))+1):
    #print b,'##################################'
    aa=0
    x.append(b-1)
    x.append(b)
    for a in np.arange(len(drifters['s'])):
        if drifters['s'][a]>=b-1 and drifters['s'][a]<b:
            aa=aa+1
            #print drifters['s'][a]
    num.append(aa)
    num.append(aa)
num.append(0)
x.append(b)
plt.figure()
#plt.title('drifter_meandis_and_mend_meandis') 
plt.plot(x,num,'b-')
plt.show()
print 'mean',np.mean(drifters['s'])
print 'max',np.max(drifters['s'])
print 'min',np.min(drifters['s'])
'''