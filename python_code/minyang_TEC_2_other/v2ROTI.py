# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:47:10 2018

@author: owo
"""

import os
import numpy as np
import matplotlib.pyplot as plt
#import scipy.io

I_year = 15
I_doy = 73

#coast_long = scipy.io.loadmat(r'D:\Ddddd\python\2003\Odata\test\coast.mat')['long']
#coast_lat = scipy.io.loadmat(r'D:\Ddddd\python\2003\Odata\test\coast.mat')['lat']     

S_v_data_path = r"D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\aeosv_data\30s".format(I_year, I_doy)

S_OutputPath = r"D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/ROTI_data/30s".format(I_year, I_doy)
if not  os.path.isdir(S_OutputPath):
    os.makedirs(S_OutputPath)


#if os.path.exists('./data20{0}{1}/ROTI_data'.format(year,day)) == False:
#    os.makedirs('./data20{0}{1}/ROTI_data'.format(year,day))
    
data_name = []
#for filenames in os.listdir(S_v_data_path): 
#    if filenames[0] == 'v':      # dat檔判別
#        data_name.append(filenames[1:5])
data_name = ['sun1','fenp', 'heri', 'dajn', 'pang']

   
Ay_v_all = np.zeros((len(data_name),2880,58))      
Ay_ROT_all = np.zeros((len(data_name),2880-1,58))      
Ay_ROTI_all = np.zeros((len(data_name),2880-9-1,58))      
Ay_lat_all = np.zeros_like(Ay_ROTI_all)
Ay_lon_all = np.zeros_like(Ay_ROTI_all)
Ay_ele_all = np.zeros_like(Ay_ROTI_all)

for i in range(len(data_name)):
    print(i)
    Ay_v_read = np.load(r"{0}\v{1}{2:03d}.npy".format(S_v_data_path,data_name[i],I_doy))
    Ay_v_read[np.where(Ay_v_read==0)] = np.nan
    
    Ay_o_read = np.load(r"{0}\o{1}{2:03d}.npy".format(S_v_data_path,data_name[i],I_doy))
    Ay_o_read[np.where(Ay_o_read==0)] = np.nan
    Ay_a_read = np.load(r"{0}\a{1}{2:03d}.npy".format(S_v_data_path,data_name[i],I_doy))
    Ay_a_read[np.where(Ay_a_read==0)] = np.nan
    Ay_e_read = np.load(r"{0}\e{1}{2:03d}.npy".format(S_v_data_path,data_name[i],I_doy))
    Ay_e_read[np.where(Ay_e_read==0)] = np.nan
    Ay_lat_all[i] = Ay_a_read[10:,:]
    Ay_lon_all[i] = Ay_o_read[10:,:]
    Ay_ele_all[i] = Ay_e_read[10:,:]
    
    
    
    Ay_ROT = (Ay_v_read[1:,:] - Ay_v_read[:len(Ay_v_read)-1,:])/0.5
    Ay_ROT_all[i] = Ay_ROT
    for j in range(2880-9-1):
        '''
        1. (<ROT**2>-<ROT>**2)**0.5
        '''
        Ay_ROTI_all[i,j] = (np.sum(Ay_ROT[j:j+9,:]**2,0)/9 - (np.sum(Ay_ROT[j:j+9,:],0)/9)**2)**0.5
        '''
        2. STD
        '''
#        Ay_ROTI_all[i,j] = (np.sum(( Ay_ROT[i:i+9,:] - np.sum(Ay_ROT[i:i+9,:],0)/9  )**2,0) /9 )**0.5
#        Ay_ROTI_all[i,j] = tt = np.std(Ay_ROT[j:j+9,:],0)

    np.save(S_OutputPath+'/{0}ROTI{1:03d}.npy'.format(data_name[i],I_doy), Ay_ROTI_all[i])