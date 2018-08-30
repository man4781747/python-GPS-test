# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:24:27 2017

@author: Chuanping_LASC_PC
"""

import numpy as np
import os
import multiprocessing as mp
import sys
import llh2xyz
import xyz2enu

def error_get(data_name,year,doy):
    PPP_load = np.load('./rtkp_data/{0}{1:02d}{2:03d}0_PPP.npy'.format(data_name,year,doy))
    PPP_load_check_sum = np.sum(PPP_load,axis=1)
    PPP_array = np.delete(PPP_load,np.where(PPP_load_check_sum==0.),0)
    PPP_location = np.mean(PPP_array,axis = 0)
    PPP_location_std = np.std(PPP_array,axis=0)
    
    PPP_location_xyz = llh2xyz.llh2xyz(np.array([PPP_location])).return_xyz()
    
    
    single_load = np.load('./rtkp_data/{0}{1:02d}{2:03d}0_sin.npy'.format(data_name,year,doy))
    
    for i in range(len(single_load)):
        if np.sum(single_load[i:i+1]) != 0.:
            sin_location_xyz = llh2xyz.llh2xyz(single_load[i:i+1]).return_xyz()
            single_load[i:i+1] = xyz2enu.xyz2enu(sin_location_xyz,PPP_location_xyz).return_enu()
        else:
            single_load[i:i+1] = np.array([[np.nan,np.nan,np.nan]])
    
    single_d = single_load
    
    all_data = np.concatenate((np.array([PPP_location]),np.array([PPP_location_std]),single_d))
    
    np.save('./position_data/{0}{1:02d}{2:03d}_position.npy'.format(data_name,year,doy),all_data)
    
def multucore(name_list,processes_num,year,doy):
    pool = mp.Pool(processes=processes_num)
    res = [pool.apply_async(error_get,(name_list.pop(),year,doy)) for i in range(len(name_list))]
    print([R.get() for R in res])   

if __name__ == '__main__':
    year_list = [int(sys.argv[1])]
    doy_list = [int(sys.argv[2])]
    processes_num = int(sys.argv[3])
    
    
    for year in year_list:
        for doy in doy_list:
            os.chdir('data20{0:02d}{1:03d}/rtkp_data'.format(year,doy))
            data_list_single = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[4:] == '{0:02d}{1:03d}0_PPP.npy'.format(year,doy):            
                        data_list_single.append(filenames[0:4])
                        
            data_list_PPP = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[4:] == '{0:02d}{1:03d}0_sin.npy'.format(year,doy):            
                        data_list_PPP.append(filenames[0:4])
            
            os.chdir('..')
            data_all_data = set(data_list_single)&set(data_list_PPP)
            
            if os.path.exists("./position_data") == False:
                os.makedirs("./position_data")
        
            multucore(data_all_data,processes_num,year,doy)
        