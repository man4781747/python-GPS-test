# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 15:32:21 2018

@author: owo
"""

import os
import numpy as np

S_command_data_path = '/pub3/man4781747/GPS_data/'

I_year_start = 15
I_year_end = 15
I_doy_start  = 73
I_doy_end = 73
I_rate = 30

for I_year in np.arange(I_year_start,I_year_end+1,1):
    for I_doy in np.arange(I_doy_start,I_doy_end+1,1):
        Lst_total_output = []
        
        Lst_phase_data_name = []
        S_dirpath = './data20{0:02d}{1:03d}/phase_data/{2:02d}s/'.format(I_year,I_doy,I_rate)
        for S_filename in os.listdir(S_dirpath):
            if os.path.isfile(S_dirpath+S_filename):
                if S_filename[4:] == '{0:02d}{1:03d}phaseL1.npy'.format(I_year,I_doy):
                    Lst_phase_data_name.append(S_filename[:4])
        
        Lst_aeosv_data_name = []
        S_dirpath = './data20{0:02d}{1:03d}/aeosv_data/{2:02d}s/'.format(I_year,I_doy,I_rate)
        for S_filename in os.listdir(S_dirpath):
            if os.path.isfile(S_dirpath+S_filename):
                if S_filename[0]=='a' and S_filename[5:] == '{0:03d}.npy'.format(I_doy):
                    Lst_aeosv_data_name.append(S_filename[1:5])
        
        Lst_position_data_name = []
        S_dirpath = './data20{0:02d}{1:03d}/position_data/'.format(I_year,I_doy)
        for S_filename in os.listdir(S_dirpath):
            if os.path.isfile(S_dirpath+S_filename):
                if S_filename[4:] == '{0:02d}{1:03d}_position.npy'.format(I_year,I_doy):
                    Lst_position_data_name.append(S_filename[:4])
        
        Lst_all_data_name = list(set(Lst_phase_data_name)&set(Lst_aeosv_data_name)&set(Lst_position_data_name))
        none = [Lst_total_output.append('python3.5 GNSS_positioning_argv.py {0:02d} {1:03d} {2} 15.'.format(I_year,I_doy,S_data_name)) for S_data_name in Lst_all_data_name]

np.save(S_command_data_path+'command_data.npy',Lst_total_output)