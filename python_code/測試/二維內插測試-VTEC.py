# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 17:28:15 2018

@author: owo
"""

import numpy as np
import matplotlib.markers as pltMark
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import glob

import scipy.signal

import scipy.io
coast_long = scipy.io.loadmat(r'D:\Ddddd\python\2003\Odata\test\coast.mat')['long']
coast_lat = scipy.io.loadmat(r'D:\Ddddd\python\2003\Odata\test\coast.mat')['lat']      

filtfilt_mark = pltMark.MarkerStyle(marker='s', fillstyle='bottom')
TrueValue_mark = pltMark.MarkerStyle(marker='s', fillstyle='top')

I_Doy = 324
I_Year = 3

S_BaseName = 'gust'
S_RoverName = 'woos'

S_DataPath = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\aeosv_data\30s'.format(I_Year, I_Doy)

VDataName = glob.glob(S_DataPath+'/v*{0:03d}.npy'.format(I_Doy))
SDataName = glob.glob(S_DataPath+'/s*{0:03d}.npy'.format(I_Doy))
ADataName = glob.glob(S_DataPath+'/a*{0:03d}.npy'.format(I_Doy))
EDataName = glob.glob(S_DataPath+'/e*{0:03d}.npy'.format(I_Doy))
ODataName = glob.glob(S_DataPath+'/o*{0:03d}.npy'.format(I_Doy))

Ay_VData = np.zeros((len(VDataName)-2, 2880, 32))
Ay_SData = np.zeros((len(VDataName)-2, 2880, 32))
Ay_AData = np.zeros((len(VDataName)-2, 2880, 32))
Ay_EData = np.zeros((len(VDataName)-2, 2880, 32))
Ay_OData = np.zeros((len(VDataName)-2, 2880, 32))

Ay_VData_Rover = np.zeros((2880,32))
Ay_SData_Rover = np.zeros((2880,32))
Ay_AData_Rover = np.zeros((2880,32))
Ay_EData_Rover = np.zeros((2880,32))
Ay_OData_Rover = np.zeros((2880,32))

Ay_VData_Rover_Liner = np.zeros((2880,32))
Ay_VData_Base_Liner = np.zeros((2880,32))

Ay_VData_Base = np.zeros((2880,32))
Ay_SData_Base = np.zeros((2880,32))
Ay_AData_Base = np.zeros((2880,32))
Ay_EData_Base = np.zeros((2880,32))
Ay_OData_Base = np.zeros((2880,32))

for i in range(len(VDataName)-2):
    print(i)
    S_StationName = VDataName[i][len(VDataName[i])-11:len(VDataName[i])-7]
    if S_StationName != S_RoverName and S_StationName != S_BaseName:
        Ay_VLoad = np.load(VDataName[i])[:,:32]
        Ay_SLoad = np.load(SDataName[i])[:,:32]
        Ay_ALoad = np.load(ADataName[i])[:,:32]
        Ay_ELoad = np.load(EDataName[i])[:,:32]
        Ay_OLoad = np.load(ODataName[i])[:,:32]
        
        Ay_SLoad[np.where(Ay_VLoad==0)] = 0 
        Ay_ALoad[np.where(Ay_VLoad==0)] = 0 
        Ay_ELoad[np.where(Ay_VLoad==0)] = 0 
        Ay_OLoad[np.where(Ay_VLoad==0)] = 0 
        Ay_VLoad[np.where(Ay_VLoad==0)] = 0 
        
        Ay_VData[i] = np.load(VDataName[i])[:,:32]
        Ay_SData[i] = np.load(SDataName[i])[:,:32]
        Ay_AData[i] = np.load(ADataName[i])[:,:32]
        Ay_EData[i] = np.load(EDataName[i])[:,:32]
        Ay_OData[i] = np.load(ODataName[i])[:,:32]
        
        
    elif S_StationName == S_RoverName:
        Ay_VData_Rover = np.load(VDataName[i])[:,:32]
        Ay_SData_Rover = np.load(SDataName[i])[:,:32]
        Ay_AData_Rover = np.load(ADataName[i])[:,:32]
        Ay_EData_Rover = np.load(EDataName[i])[:,:32]
        Ay_OData_Rover = np.load(ODataName[i])[:,:32]
    else :
        Ay_VData_Base = np.load(VDataName[i])[:,:32]
        Ay_SData_Base = np.load(SDataName[i])[:,:32]
        Ay_AData_Base = np.load(ADataName[i])[:,:32]
        Ay_EData_Base = np.load(EDataName[i])[:,:32]
        Ay_OData_Base = np.load(ODataName[i])[:,:32]
        
    
    
#%%     
Ay_Ans = np.zeros((2880,30,35))
Ay_VData_Rover_Liner = np.zeros((2880,32))
Ay_VData_Base_Liner = np.zeros((2880,32))

#Ay_VData[:,:,4] = 0
#Ay_AData[:,:,4] = 0
#Ay_EData[:,:,4] = 0
#Ay_OData[:,:,4] = 0

#for k in range(200,800):  
for k in range(2880):  
#for k in range(436,437): 
#for k in range(1800,1801): 
    print(k)
    Ay_VData_ = Ay_VData[:,k:k+10,:]
    Ay_AData_ = Ay_AData[:,k:k+10,:]
    Ay_EData_ = Ay_EData[:,k:k+10,:]
    Ay_OData_ = Ay_OData[:,k:k+10,:]
    
    

    Ay_VData_Rover_ = Ay_VData_Rover[k,:]
#    Ay_SData_Rover_ = Ay_SData_Rover[k,:]
    Ay_AData_Rover_ = Ay_AData_Rover[k,:]
    Ay_EData_Rover_ = Ay_EData_Rover[k,:]
    Ay_OData_Rover_ = Ay_OData_Rover[k,:]
    
    Ay_VData_Base_ = Ay_VData_Base[k,:]
#    Ay_SData_Base_ = Ay_SData_Base[k,:]
    Ay_AData_Base_ = Ay_AData_Base[k,:]
    Ay_EData_Base_ = Ay_EData_Base[k,:]
    Ay_OData_Base_ = Ay_OData_Base[k,:]
    
    
#    lat_min, lat_max = (-95, -70)
#    lon_min, lon_max = (30, 50)
    lat_min, lat_max = (-130, -60)
    lon_min, lon_max = (0, 60)
    
    Ay_testArray = np.zeros((len(np.where((Ay_VData_!=0)&(Ay_AData_>lon_min)&(Ay_AData_<lon_max)&(Ay_OData_>lat_min)&(Ay_OData_<lat_max))[0]),2 ))
    Ay_testArray[:,0] = Ay_OData_[np.where((Ay_VData_!=0)&
                          (Ay_AData_>lon_min)&(Ay_AData_<lon_max)&(Ay_OData_>lat_min)&(Ay_OData_<lat_max))]
    Ay_testArray[:,1] = Ay_AData_[np.where((Ay_VData_!=0)&(Ay_AData_>lon_min)&(Ay_AData_<lon_max)&(Ay_OData_>lat_min)&(Ay_OData_<lat_max))]
    Ay_testV = Ay_VData_[np.where((Ay_VData_!=0)&(Ay_AData_>lon_min)&(Ay_AData_<lon_max)&(Ay_OData_>lat_min)&(Ay_OData_<lat_max))]

    Ay_lon_map, Ay_lat_map = np.meshgrid(np.arange(-130,-60,2), np.arange(0,60,2))
    grid_test_linear = griddata(Ay_testArray, Ay_testV, (Ay_lon_map, Ay_lat_map), method='linear')
    
    Filtfilt_test = np.zeros_like(grid_test_linear)
    
    for i in range(len(grid_test_linear[0,:])):
        Filtfilt_test[:,i] = scipy.signal.filtfilt(np.zeros(3)+1/3., 1, grid_test_linear[:,i])
    
    
    Filtfilt_test_2 = np.zeros_like(grid_test_linear)
    
    for i in range(len(grid_test_linear[:,0])):
        Filtfilt_test_2[i,:] = scipy.signal.filtfilt(np.zeros(3)+1/3., 1, Filtfilt_test[i,:])
    
    
    
    Ay_OChose_Base = Ay_OData_Base_[np.where((Ay_OData_Base_!=0)&
                                             (Ay_AData_Base_>lon_min)&
                                             (Ay_AData_Base_<lon_max)&
                                             (Ay_OData_Base_>lat_min)&
                                             (Ay_OData_Base_<lat_max))]
    Ay_AChose_Base = Ay_AData_Base_[np.where((Ay_AData_Base_!=0)&
                                             (Ay_AData_Base_>lon_min)&
                                             (Ay_AData_Base_<lon_max)&
                                             (Ay_OData_Base_>lat_min)&
                                             (Ay_OData_Base_<lat_max))]
    
    Ay_Ans[k] = Filtfilt_test_2
    
    for j in range(len(Ay_OChose_Base)):
        O_Map_Chose = int((Ay_OChose_Base[j] - lat_min)/2)
        A_Map_Chose = int((Ay_AChose_Base[j] - lon_min)/2)
        V_Value_Chose = Filtfilt_test_2[A_Map_Chose,O_Map_Chose]
        Ay_VData_Base_Liner[k,np.where(Ay_OData_Base_!=0)[0][j]] = V_Value_Chose

    Ay_OChose_Rover = Ay_OData_Rover_[np.where((Ay_OData_Rover_!=0)&
                                             (Ay_AData_Rover_>lon_min)&
                                             (Ay_AData_Rover_<lon_max)&
                                             (Ay_OData_Rover_>lat_min)&
                                             (Ay_OData_Rover_<lat_max))]
    Ay_AChose_Rover = Ay_AData_Rover_[np.where((Ay_AData_Rover_!=0)&
                                             (Ay_AData_Rover_>lon_min)&
                                             (Ay_AData_Rover_<lon_max)&
                                             (Ay_OData_Rover_>lat_min)&
                                             (Ay_OData_Rover_<lat_max))]

    for j in range(len(Ay_OChose_Rover)):
        O_Map_Chose = int((Ay_OChose_Rover[j] - lat_min)/2)
        A_Map_Chose = int((Ay_AChose_Rover[j] - lon_min)/2)
        V_Value_Chose = Filtfilt_test_2[A_Map_Chose,O_Map_Chose]
        Ay_VData_Rover_Liner[k,np.where(Ay_OData_Rover_!=0)[0][j]] = V_Value_Chose 
#np.save(r'D:\google drive\我der碩士論文\磁暴\GridData\GidData15324_Grid2_Filt3_ALLDAY.npy', Ay_Ans)
#Ay_VData_Base_Liner[np.where(Ay_VData_Base_Liner==0)]=np.nan
np.save(r'D:\google drive\我der碩士論文\磁暴\GridData\v{2}{1:03d}GridDataLinear_grid2_filt3_box.npy'.format(I_Year, I_Doy, S_RoverName), Ay_VData_Rover_Liner)
np.save(r'D:\google drive\我der碩士論文\磁暴\GridData\v{2}{1:03d}GridDataLinear_grid2_filt3_box.npy'.format(I_Year, I_Doy, S_BaseName), Ay_VData_Base_Liner)



#for i in range(2880):
#    plt.pcolor(Ay_lon_map, Ay_lat_map,Ay_Ans[i] ,vmax=180, vmin=0)
#    plt.plot(coast_long, coast_lat, c='black', lw=1)
#    plt.axis('equal')
#    plt.xlim(-110, -80)
#    plt.ylim(10, 60)
#    plt.title(i)
#    plt.colorbar()
#    plt.savefig(r'D:\google drive\我der碩士論文\磁暴\image\GridDataAndFiltfiltMap\{0}.png'.format(i))
#    plt.clf()
    
for i in range(32):
    plt.plot(vgust324[:,i])
    plt.plot(Ay_VData_Base_Liner[:,i])
    plt.title('orange: filtfilt, blue: Original')
    plt.savefig(r'D:\google drive\我der碩士論文\磁暴\image\GridDataAndFiltfiltMap\gust站各衛星vTEC數值比較\gust_No{0}.png'.format(i+1))
    plt.clf()
    