# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:34:20 2016

@author: hxu
"""

import datetime as dt
import pytz
import pandas as pd
from math import sqrt,radians,sin,cos,atan
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pytz import timezone
import numpy as np
import csv
from matplotlib.path import Path
from netCDF4 import Dataset
from scipy import  interpolate
from matplotlib.dates import date2num,num2date
def nearest_point(lon, lat, lons, lats, length):  #0.3/5==0.06
    '''Find the nearest point to (lon,lat) from (lons,lats),
     return the nearest-point (lon,lat)
     author: Bingwei'''
    p = Path.circle((lon,lat),radius=length)
    #numpy.vstack(tup):Stack arrays in sequence vertically
    points = np.vstack((lons.flatten(),lats.flatten())).T  
        
    insidep = []
    #collect the points included in Path.
    ii=[]
    for i in xrange(len(points)):
        if p.contains_point(points[i]):# .contains_point return 0 or 1
            insidep.append(points[i]) 
            ii.append(i)
    # if insidep is null, there is no point in the path.
    if not insidep:
        #print 'lon,lat',lon,lat
        print 'There is no model-point near the given-point.'
        raise Exception()
    #calculate the distance of every points in insidep to (lon,lat)
    distancelist = []
    for i in insidep:
        ss=sqrt((lon-i[0])**2+(lat-i[1])**2)
        distancelist.append(ss)
    # find index of the min-distance
    mindex = np.argmin(distancelist)
    # location the point
    
        
    return mindex,ii

def rot2d(x, y, ang):
    '''rotate vectors by geometric angle'''
    xr = x*np.cos(ang) - y*np.sin(ang)
    yr = x*np.sin(ang) + y*np.cos(ang)
    return xr, yr
def haversine(lon1, lat1, lon2, lat2): 
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """   
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
    #print 34
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * atan(sqrt(a)/sqrt(1-a))   
    r = 6371 
    d=c * r
    #print type(d)
    return d
def calculate_SD(modelpoints,dmlon,dmlat,drtime):
    '''compare the model_points and drifter point(time same as model point)
    (only can pompare one day)!!!'''
    dist=[];meandisdis=[];
    #print modelpoints,dmlon,dmlat,drtime
    print min(len(modelpoints['lon']),len(dmlon))
    for a in range(min(len(modelpoints['lon']),len(dmlon))):
        #print 12
        d=haversine(modelpoints['lon'][a],modelpoints['lat'][a],dmlon[a],dmlat[a])#Calculate the distance between two points 
        #print model_points['lon'][a][j],model_points['lat'][a][j],dmlon[a][j],dmlat[a][j],d           
        print d
        dist.append(d)
    l=0
    for a in np.arange(len(dmlon)-1):
        l=l+haversine(dmlon[a],dmlat[a],dmlon[a+1],dmlat[a+1])
    disdist=(dist[-1]/float(l))   
    '''if meansd!=0:
        meantimedis.append(meansd)'''
    #print dist
    meandisdis
    return dist,dist[-1],disdist
def timedeal(time):
    '''
    min different time between two near point '''
    span=[]
    for i in range(len(time)-1):
        span.append((time[i+1]-time[i]).seconds)
    span_time=np.mean(span)/60
    return span_time

######## Hard codes ##########
url='''current_04hind_hourly.nc'''
ds=Dataset(url,'r').variables
url1='''gom6-grid.nc'''
ds1=Dataset(url1,'r').variables
#for i in np.arange(len(np.hstack(ds1['lat_u']))):

t0=datetime(1858,11,17,0,0,0)
restart_days=1
track_days=15
t=np.array([t0+timedelta(days=ds['ocean_time'][kt]/float(60*60*24)) for kt in np.arange(len(ds['ocean_time']))])

Model=['ROMS']
F='data/'
file_drID=[]
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
if 'ROMS' in Model:
    spdis=[];disrat=[];idddd=[];lllo=[];llla=[]
if 'ROMS' in Model:
    romstmeandis=[];romstmindis=[];romstmaxdis=[];romsdmeandis=[];romsdmindis=[];romsdmaxdis=[]
ii=0

for a in np.arange(695):
    #print a
    iiiii=a
    dtime=[]
    drifters = np.genfromtxt(F+str(a)+'.csv',dtype=None,names=['ids','time','lon','lat','depth'],delimiter=',',skip_header=1)  
    try:
        for b in np.arange(len(drifters['time'])):
            dtime.append(datetime.strptime(drifters['time'][b], '%Y-%m-%d'+'T'+'%H:%M:%SZ'))
        #print dtime
    except:
        continue
    try:
        day=(dtime[-1]-dtime[0]).days
    except:
        continue
    if day<=10:
        continue
    print 1
    rawtime=[]
    for a in np.arange(len(dtime)):
        rawtime.append(date2num(dtime[a]))
    t1=np.ceil(np.min(rawtime)*24.)/24.
    t2=np.floor(np.max(rawtime)*24.)/24.
    tdh=np.arange(t1,t2,1./(24*6))
    try:
        
        lo=interpolate.interp1d(rawtime,drifters['lon'],kind='cubic')  
        la=interpolate.interp1d(rawtime,drifters['lat'],kind='cubic')
        dr=dict(lon=[],lat=[],time=[])
        for a in np.arange(len(tdh)):
            dr['lon'].append(lo(tdh[a]))
            dr['lat'].append(la(tdh[a]))
            dr['time'].append(tdh[a])
    except:
        continue

    ii=ii+1
    print ii
    
        
    drift=dict(lon=[],lat=[],time=[])
    for a in np.arange(len(tdh)):
        if num2date(tdh[a]).minute==0 and num2date(tdh[a]).second==0:
            drift['lon'].append(dr['lon'][a])
            drift['lat'].append(dr['lat'][a])
            drift['time'].append((num2date(tdh[a])).replace(tzinfo=None))
        
        #print drifter_points
   
    plt.figure()
    plt.plot(dr['lon'],dr['lat'],'r-') 
    plt.plot(drifters['lon'],drifters['lat'],'b-')
    print ii

    lonnn=[]
    lattt=[]
    distance=[]
    meantimedis=[]
    meandisdist=[]
    model_points_s=[]
    model_points =dict(lon=[],lat=[],time=[])
    iiiiiiiiiii=0
    days=(drift['time'][-1]-drift['time'][0]).days
    for nday in np.arange(1,days+1,restart_days): 
        modelpoints = dict(lon=[],lat=[],time=[]) 
        try:
            start_time=drift['time'][(nday-1)*24]
            end_times=drift['time'][(nday-1+track_days)*24]
        except:
            continue
        print start_time
        print end_times
        index1=np.argmin(abs(t-start_time))
        index2=np.argmin(abs(t-end_times))
        print t[index1]
        print t[index2]
        mlon=drift['lon'][(nday-1)*24:(nday-1+track_days)*24]
        mlat=drift['lat'][(nday-1)*24:(nday-1+track_days)*24]
        print '#####################################################33'
        modelpoints['lon'].append(mlon[0])
        modelpoints['lat'].append(mlat[0])
        modelpoints['time'].append(start_time)
        temlon=mlon[0]
        temlat=mlat[0]
        for a in np.arange(index1, index2,1):
            #ds['u'][a][-1][]
            dmmu=[]
            dmmv=[]
            
            imxu,iu=nearest_point(temlon, temlat, np.hstack(ds1['lon_u']), np.hstack(ds1['lat_u']), 0.2)
            imxv,iv=nearest_point(temlon, temlat, np.hstack(ds1['lon_v']), np.hstack(ds1['lat_v']), 0.2)
            
            p = Path.circle((temlon,temlat),radius=0.1)
            uuu=[]
            vvv=[]
            for jj in np.arange(len(iu)):
                uuu.append(np.hstack(ds['u'][a][-1][:])[iu[jj]])
            for jj in np.arange(len(iv)):
                vvv.append(np.hstack(ds['v'][a][-1][:])[iv[jj]])
            uu=uuu[imxu]
            vv=vvv[imxv]
            if uu>100 or vv>100:
                continue
            u_t,v_t=rot2d(uu,vv,ds1['angle'][0][0])
            print 'u_t',u_t
            print 'v_t',v_t
            dx = 60*60*u_t; dy = 60*60*v_t
            temlon = temlon + (dx/(111111*np.cos(temlat*np.pi/180)))
            temlat = temlat + dy/111111
            modelpoints['lon'].append(temlon)
            modelpoints['lat'].append(temlat)
            modelpoints['time'].append(t[a])      
        
        dist=[]
        
        if len(modelpoints['lon'])-1==24*track_days:
            dist,meantdis,meandisdis=calculate_SD(modelpoints,drift['lon'][(nday-1)*24:(nday-1+track_days)*24+1],drift['lat'][(nday-1)*24:(nday-1+track_days)*24+1],drift['time'][(nday-1)*24:(nday-1+track_days)*24+1]) 
        else:
            continue
        #dist,meantdis,meandisdis=calculate_SD(modelpoints,drifter_points['lon_hr'][(nday-1)*24:(nday-1+track_days)*24+1],drifter_points['lat_hr'][(nday-1)*24:(nday-1+track_days)*24+1],drifter_points['h_hr'][(nday-1)*24:(nday-1+track_days)*24+1]) 
        iiiiiiiiiii=iiiiiiiiiii+1 
        model_points['lon'].append(modelpoints['lon']); model_points['lat'].append(modelpoints['lat']);model_points['time'].append(modelpoints['time'])
        
        if meantdis>100000000000000 or meandisdis>10000000000000000:
            continue
        distance.append(dist)#one drifter one model all distance 
        meandisdist.append(meandisdis) #one drifter one model per day mean distance/dist                
        meantimedis.append(dist[-1])#one drifter one model per day mean distance/day
        lonnn.append(drift['lon'][(nday-1)*24])
        lattt.append(drift['lat'][(nday-1)*24])
    try:
        
        plt.figure(1) 
        plt.title('id=%s drifter track vs modle=%s'%(drifters['ids'][0],Model[0]))
        for haha in np.arange(0,iiiiiiiiiii,restart_days):#drifters['days'][num]-2,restart_days): drifters['days'][num]-2,restart_days):#
            plt.plot(model_points['lon'][haha],model_points['lat'][haha],'ro-')
        
        plt.plot(drift['lon'][0:],drift['lat'][0:],'bo-')
        plt.grid(True)
        plt.savefig('id=%s drifter track vs modle=%s '%(drifters['ids'][0],Model[0]))  
        plt.show()
        
        plt.figure(2)
        plt.title('id=%s drifter  vs modle=%s distance'%(drifters['ids'][0],Model[0]))
        iddd=[]
        for x in range(len(distance)):
            plt.plot(distance[x][:])
            plt.text(track_days*24-3,distance[x][-1],'meandis=%.2f' %(meantimedis[x]),color='red',fontsize=12)
            iddd.append(drifters['ids'][0])
        plt.ylabel('distance(km)')   
        plt.xlabel('time')
        #plt.savefig('id=%s drifter   vs modle=%s distance'%(drifters['ids'][a],Model[0]))
        plt.show()
    
        if Model[0] == 'ROMS':
            idddd.append(iddd)
            spdis.append(meantimedis)
            disrat.append(meandisdist)
            lllo.append(lonnn)
            llla.append(lattt)
    except:
        continue
data=[];tdata=[];model=[];dataaa=[]
if 'ROMS' in Model:
    tdata.append(np.hstack(idddd));tdata.append(np.hstack(lllo));tdata.append(np.hstack(llla));data.append(np.hstack(spdis));data.append(np.hstack(disrat))
    model.append('roms')    
#tdata.append(file_drID)
for w in range(0,len(data),1):
    ldata=[]    
    for e in data[w]:
        e="%.2f" %e
        ldata.append(e)
    tdata.append(ldata)
            
chat=map(list, zip(*tdata))  
csvfile = file('drifter_vs_roms use hourly data15.csv', 'wb')
writer = csv.writer(csvfile)
fh=['ids']
fh.append('lon')
fh.append('lat')
for z in range(len(model)):
    fh.append('%s_separation(km/day)' %model[z] )
    fh.append('%s_separation(km/km)' %model[z] )
writer.writerow(fh)
writer.writerows(chat)
csvfile.close()
