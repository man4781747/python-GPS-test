# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 13:25:51 2017

@author: owo

Example不分站: python3.5 minyangTEC2other_command_do.py 15 15 60 80 30 all

Example分站: python3.5 minyangTEC2other_command_do.py 15 15 60 80 30 aknd
"""



import os 
import numpy as np
import sys

S_yankai_data_path = "/pub3/man4781747/GPS_data/"
S_minyang_data_path = "/nishome/man4781747/GPSTEC_minyan/gnsstec_v7.2/"


#I_year_start = 15
#I_year_end = 15
#I_doy_start = 60
#I_doy_end = 80
#I_rate = 30
I_year_start = int(sys.argv[1])
I_year_end = int(sys.argv[2])
I_doy_start = int(sys.argv[3])
I_doy_end = int(sys.argv[4])
I_rate = int(sys.argv[5])
S_stataion_chose = str(sys.argv[6])

if S_stataion_chose == 'all':
    Lst_sys_command = []
    for I_year in np.arange(I_year_start,I_year_end+1,1):
        for I_doy in np.arange(I_doy_start,I_doy_end+1,1):
            
            os.chdir(S_minyang_data_path+'OBS/gps/20{0:02d}.{1:03d}/{2}s'.format(I_year,I_doy,I_rate))
            Lst_data_GPS = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[9:13] == "mat":
                        Lst_data_GPS.append(filenames[0:4])
                        
            os.chdir(S_minyang_data_path+'OBS/glonass/20{0:02d}.{1:03d}/{2}s'.format(I_year,I_doy,I_rate))
            Lst_data_glonass = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[9:13] == "mat":
                        Lst_data_glonass.append(filenames[0:4])
            
            Lst_all_data = list(set(Lst_data_GPS)|set(Lst_data_glonass))
            
            for S_station_name in Lst_all_data:
                Lst_sys_command.append('python3.5 minyangTEC2other_main_code_stationVer.py {0} {1} {2} {3}'.format(I_year,I_doy,S_station_name,I_rate))
else:
    Lst_sys_command = []
    for I_year in np.arange(I_year_start,I_year_end+1,1):
        for I_doy in np.arange(I_doy_start,I_doy_end+1,1):
            
            os.chdir(S_minyang_data_path+'OBS/gps/20{0:02d}.{1:03d}/{2}s'.format(I_year,I_doy,I_rate))
            Lst_data_GPS = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[9:13] == "mat":
                        if filenames[0:4] == S_stataion_chose:
                            Lst_data_GPS.append(filenames[0:4])
                        
            os.chdir(S_minyang_data_path+'OBS/glonass/20{0:02d}.{1:03d}/{2}s'.format(I_year,I_doy,I_rate))
            Lst_data_glonass = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[9:13] == "mat":
                        if filenames[0:4] == S_stataion_chose:
                            Lst_data_glonass.append(filenames[0:4])
            
            Lst_all_data = list(set(Lst_data_GPS)|set(Lst_data_glonass))
            
            for S_station_name in Lst_all_data:
                Lst_sys_command.append('python3.5 minyangTEC2other_main_code_stationVer.py {0} {1} {2} {3}'.format(I_year,I_doy,S_station_name,I_rate))

np.save(S_yankai_data_path+"minyangTEC2other_command.npy",Lst_sys_command)
