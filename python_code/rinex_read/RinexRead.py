# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:45:11 2018

@author: owo
"""

from YMD2DOY import YMD2DOY
import numpy as np
import os


def do(I_year, I_month, I_day, S_station, S_InputPath, S_OutputPath):
    I_doy = YMD2DOY(I_year, I_month, I_day)
    if not os.path.exists(S_OutputPath):
        os.makedirs(S_OutputPath)
    
    with open() as f:
        Lst_readlines = f.readlines()
    
    for I_line_chose_num_all in range(len(Lst_readlines)):
        if Lst_readlines[I_line_chose_num_all].find('# / TYPES OF OBSERV') != -1:
            Lst_OBS_base = Lst_readlines[I_line_chose_num_all].split()
            global I_L1_loc,I_L2_loc,I_P1_loc,I_P2_loc,I_C1_loc,I_C2_loc,I_S1_loc,I_S2_loc,I_numofOBStype
            I_numofOBStype = int(Lst_OBS_base[0])
            try:
                I_L1_loc = Lst_OBS_base.index('L1')-1
            except:
                pass
            try:
                I_L2_loc = Lst_OBS_base.index('L2')-1
            except:
                pass
            try:
                I_P1_loc = Lst_OBS_base.index('P1')-1
            except:
                pass
            try:
                I_P2_loc = Lst_OBS_base.index('P2')-1
            except:
                pass
            try:
                I_C1_loc = Lst_OBS_base.index('C1')-1
            except:
                pass
            try:
                I_C2_loc = Lst_OBS_base.index('C2')-1   
            except:
                pass   
            try:
                I_S1_loc = Lst_OBS_base.index('S1')-1
            except:
                pass
            try:
                I_S2_loc = Lst_OBS_base.index('S2')-1
            except:
                pass
#            print(I_L1_loc,I_L2_loc,I_P1_loc,I_P2_loc,I_C1_loc,I_C2_loc,I_S1_loc,I_S2_loc,I_numofOBStype)   
        if Lst_readlines[I_line_chose_num_all].find('END OF HEADER') != -1:
            I_line_chose_num_all += 1
            break
    
    Ay_L1_all = np.zeros((0,32))
    Ay_L1_slip_all = np.zeros((0,32))
    Ay_L2_all = np.zeros((0,32))
    Ay_L2_slip_all = np.zeros((0,32))
    Ay_P1_all = np.zeros((0,32))
    Ay_P2_all = np.zeros((0,32))
    Ay_C1_all = np.zeros((0,32))
    Ay_C2_all = np.zeros((0,32))
    Ay_S1_all = np.zeros((0,32))
    Ay_S2_all = np.zeros((0,32))
    
    Ay_time_all = np.zeros((0,6))
    while I_line_chose_num_all < len(Lst_readlines):
        (I_line_chose_num_all,F_time_in_day,Ay_time,
         Ay_gps_L1_sing,Ay_gps_L2_sing,
         Ay_gps_L1_slip,Ay_gps_L2_slip,
         Ay_gps_P1_sing,Ay_gps_P2_sing,
         Ay_gps_C1_sing,Ay_gps_C2_sing,
         Ay_gps_S1_sing,Ay_gps_S2_sing
         ) = Fun_info_get(Lst_readlines,I_line_chose_num_all)
#        print(Ay_gps_L1_sing)
        Ay_L1_all = np.concatenate((Ay_L1_all,Ay_gps_L1_sing))
        Ay_L1_slip_all = np.concatenate((Ay_L1_slip_all,Ay_gps_L1_slip))
        Ay_L2_all = np.concatenate((Ay_L2_all,Ay_gps_L2_sing))
        Ay_L2_slip_all = np.concatenate((Ay_L2_slip_all,Ay_gps_L2_slip))
        Ay_P1_all = np.concatenate((Ay_P1_all,Ay_gps_P1_sing))
        Ay_P2_all = np.concatenate((Ay_P2_all,Ay_gps_P2_sing))
        Ay_C1_all = np.concatenate((Ay_C1_all,Ay_gps_C1_sing))
        Ay_C2_all = np.concatenate((Ay_C2_all,Ay_gps_C2_sing))
        Ay_S1_all = np.concatenate((Ay_S1_all,Ay_gps_S1_sing))
        Ay_S2_all = np.concatenate((Ay_S2_all,Ay_gps_S2_sing))
        Ay_time_all = np.concatenate((Ay_time_all,np.array([Ay_time]) ))
    
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseL1.npy'.format(S_station,I_year,I_doy),Ay_L1_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseL1_slip.npy'.format(S_station,I_year,I_doy),Ay_L1_slip_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseL2.npy'.format(S_station,I_year,I_doy),Ay_L2_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseL2_slip.npy'.format(S_station,I_year,I_doy),Ay_L2_slip_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseP1.npy'.format(S_station,I_year,I_doy),Ay_P1_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseP2.npy'.format(S_station,I_year,I_doy),Ay_P2_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseC1.npy'.format(S_station,I_year,I_doy),Ay_C1_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseC2.npy'.format(S_station,I_year,I_doy),Ay_C2_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseS1.npy'.format(S_station,I_year,I_doy),Ay_S1_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phaseS2.npy'.format(S_station,I_year,I_doy),Ay_S2_all)
    np.save(S_phase_data_path+'{0}{1:02d}{2:03d}phasetime.npy'.format(S_station,I_year,I_doy),Ay_time_all)

if __name__ == '__main__':
    
    I_year = 15
    I_month = 3
    I_day = 14
    S_OutputPath = r'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/phase_data/30s/'.format(I_year,I_doy)
    
    Lst_station_name = ['pepu','hual']
#    Lst_station_name = ['woos','stkr','defi','metr','gust']
#    Lst_station_name = ['heri','pang','fenp','dajn']
#    S_station = 'dajn'
    for S_station in Lst_station_name:
        S_InputPath = r'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/odata/30s/{2}{1:03d}0.{0:02d}o'.format(I_year,I_doy,S_station)
        do(I_year, I_month, I_day, S_station, S_InputPath, S_OutputPath)