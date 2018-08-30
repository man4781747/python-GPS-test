# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:40:11 2018

@author: owo
"""

from CustomValue import *
from NDataRead import NDataRead


class LoadGPSData:
    def __init__(self, I_Year, I_Doy, S_StationName):
        self.C_NData = NDataRead(S_n_data_path.format(I_Year,I_Doy)+'n_data_{0:02d}{1:03d}.npy'.format(I_Year,I_Doy)) 
        self.Ay_Pr_C1 = np.load(S_phase_data_path.format(I_Year,I_Doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_Year,I_Doy,S_StationName))[:,:32]
        self.Ay_AnsPosition = np.load(S_ans_position_path.format(I_Year,I_Doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_Year,I_Doy,S_StationName))[0,:]
        Ay_TimeRaw = np.load(S_phase_data_path.format(I_Year,I_Doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_Year,I_Doy,S_StationName))[:,0:6]
        self.Ay_Time = Ay_TimeRaw[:,3]*3600.+Ay_TimeRaw[:,4]*60.+Ay_TimeRaw[:,5]
    
    

#        return C_NData, Ay_Pr_C1, Ay_AnsPosition, Ay_TimeRaw, Ay_Time