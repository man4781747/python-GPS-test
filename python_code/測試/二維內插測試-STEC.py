# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 17:28:15 2018

@author: owo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import glob

I_Doy = 324
I_Year = 3

S_BaseName = 'gust'
S_RoverName = 'woos'

#S_BaseName = 'fenp'
#S_RoverName = 'sun1'

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

#Ay_VData = np.zeros((len(VDataName), 2880, 32))
#Ay_SData = np.zeros((len(VDataName), 2880, 32))
#Ay_AData = np.zeros((len(VDataName), 2880, 32))
#Ay_EData = np.zeros((len(VDataName), 2880, 32))
#Ay_OData = np.zeros((len(VDataName), 2880, 32))

Ay_VData_Rover = np.zeros((2880,32))
Ay_SData_Rover = np.zeros((2880,32))
Ay_AData_Rover = np.zeros((2880,32))
Ay_EData_Rover = np.zeros((2880,32))
Ay_OData_Rover = np.zeros((2880,32))

Ay_SData_Rover_Liner = np.zeros((2880,32))
Ay_SData_Base_Liner = np.zeros((2880,32))

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
        
        
        Ay_VData[i] = Ay_VLoad
        Ay_SData[i] = Ay_SLoad
        Ay_AData[i] = Ay_ALoad
        Ay_EData[i] = Ay_ELoad
        Ay_OData[i] = Ay_OLoad
        
#        Ay_VData[i] = np.load(VDataName[i])[:,:32]
#        Ay_SData[i] = np.load(SDataName[i])[:,:32]
#        Ay_AData[i] = np.load(ADataName[i])[:,:32]
#        Ay_EData[i] = np.load(EDataName[i])[:,:32]
#        Ay_OData[i] = np.load(ODataName[i])[:,:32]
#        
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
        
    
#    Ay_VLoad = np.load(VDataName[i])[:,:32]
#    Ay_SLoad = np.load(SDataName[i])[:,:32]
#    Ay_ALoad = np.load(ADataName[i])[:,:32]
#    Ay_ELoad = np.load(EDataName[i])[:,:32]
#    Ay_OLoad = np.load(ODataName[i])[:,:32]
#    
#    Ay_SLoad[np.where(Ay_VLoad==0)] = 0 
#    Ay_ALoad[np.where(Ay_VLoad==0)] = 0 
#    Ay_ELoad[np.where(Ay_VLoad==0)] = 0 
#    Ay_OLoad[np.where(Ay_VLoad==0)] = 0 
#    
#    Ay_VData[i] = np.load(VDataName[i])[:,:32]
#    Ay_SData[i] = np.load(SDataName[i])[:,:32]
#    Ay_AData[i] = np.load(ADataName[i])[:,:32]
#    Ay_EData[i] = np.load(EDataName[i])[:,:32]
#    Ay_OData[i] = np.load(ODataName[i])[:,:32]
    
     #%%   
for k in range(2880):      
    print(k)
#for k in range(1):    
    Ay_VData_ = Ay_VData[:,k,:]
    Ay_SData_ = Ay_SData[:,k,:]
    Ay_AData_ = Ay_AData[:,k,:]
    Ay_EData_ = Ay_EData[:,k,:]
    Ay_OData_ = Ay_OData[:,k,:]
    
    
#    Ay_SData_ = Ay_SData_[np.where(Ay_VData_ != 0)]
#    Ay_AData_ = Ay_AData_[np.where(Ay_VData_ != 0)]
#    Ay_EData_ = Ay_EData_[np.where(Ay_VData_ != 0)]
#    Ay_OData_ = Ay_OData_[np.where(Ay_VData_ != 0)]
#    Ay_VData_ = Ay_VData_[np.where(Ay_VData_ != 0)]
        
    Ay_VData_Rover_ = Ay_VData_Rover[k,:]
    Ay_SData_Rover_ = Ay_SData_Rover[k,:]
    Ay_AData_Rover_ = Ay_AData_Rover[k,:]
    Ay_EData_Rover_ = Ay_EData_Rover[k,:]
    Ay_OData_Rover_ = Ay_OData_Rover[k,:]
    
    Ay_VData_Base_ = Ay_VData_Base[k,:]
    Ay_SData_Base_ = Ay_SData_Base[k,:]
    Ay_AData_Base_ = Ay_AData_Base[k,:]
    Ay_EData_Base_ = Ay_EData_Base[k,:]
    Ay_OData_Base_ = Ay_OData_Base[k,:]

#    Ay_lon_map, Ay_lat_map = np.meshgrid(np.arange(114,126,0.05), np.arange(15,32,0.05))
#    Ay_lon_map, Ay_lat_map = np.meshgrid(np.arange(123,125,0.05), np.arange(18.5,21.5,0.05))
    
    Ay_lon_map, Ay_lat_map = np.meshgrid(np.arange(-90,-72.5,0.05), np.arange(38,46,0.05))

    for j in range(32):
        Ay_testArray = np.zeros((len(np.where((Ay_SData_[:,j]!=0) & (Ay_EData_[:,j] >=0.))[0]),2 ))
        Ay_testArray[:,0] = Ay_OData_[np.where((Ay_SData_[:,j]!=0) & (Ay_EData_[:,j] >=0.))[0],j]
        Ay_testArray[:,1] = Ay_AData_[np.where((Ay_SData_[:,j]!=0) & (Ay_EData_[:,j] >=0.))[0],j]
        Ay_testS = Ay_SData_[np.where((Ay_SData_[:,j]!=0) & (Ay_EData_[:,j] >=0.))[0],j]
        if Ay_OData_Rover_[j] != 0 and len(np.where((Ay_SData_[:,j]!=0) & (Ay_EData_[:,j] >=0.))[0]) >= 10:
            grid_Rover = griddata(Ay_testArray, Ay_testS, (Ay_OData_Rover_[j], Ay_AData_Rover_[j]), method='nearest')
            grid_Base = griddata(Ay_testArray, Ay_testS, (Ay_OData_Base_[j], Ay_AData_Base_[j]), method='nearest')
            grid_test_linear = griddata(Ay_testArray, Ay_testS, (Ay_lon_map, Ay_lat_map), method='linear')
#            plt.pcolor(Ay_lon_map[~np.isnan(grid_test_linear)], Ay_lat_map[~np.isnan(grid_test_linear)],grid_test_linear[~np.isnan(grid_test_linear)])
            plt.contourf(Ay_lon_map, Ay_lat_map,grid_test_linear)
            plt.scatter(Ay_testArray[:,0], Ay_testArray[:,1], c=Ay_testS,linewidths=2,edgecolors='black')
            Ay_SData_Rover_Liner[k,j] = grid_Rover
            Ay_SData_Base_Liner[k,j] = grid_Base
        elif len(np.where(Ay_SData_[:,j]!=0)[0]) < 3:
            pass
#            plt.scatter(Ay_OData_Rover_[j], Ay_AData_Rover_[j])
            
#np.save(r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\aeosv_data\s{2}{1:03d}test_nearest.npy'.format(I_Year, I_Doy, S_RoverName), Ay_SData_Rover_Liner)
#np.save(r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\aeosv_data\s{2}{1:03d}test_nearest.npy'.format(I_Year, I_Doy, S_BaseName), Ay_SData_Base_Liner)

