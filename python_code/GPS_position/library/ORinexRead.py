# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 19:28:19 2018

@author: owo

o_data 讀取資料程式
㍍
"""

from YMD2DOY import YMD2DOY
import numpy as np
import os

from CustomValue import *

def Fun_info_get(Lst_readlines,I_title_num):
    try:
        I_title_num_chose = I_title_num
        Lst_each_title_read = Lst_readlines[I_title_num_chose].split()
        Ay_time = np.array([int(Lst_each_title_read[0]),int(Lst_each_title_read[1]),int(Lst_each_title_read[2]),
                            int(Lst_each_title_read[3]),int(Lst_each_title_read[4]),float(Lst_each_title_read[5]),])
        F_time_in_day = (int(Lst_each_title_read[2])-I_day)*3600*24. +\
                         int(Lst_each_title_read[3])*3600. +\
                         int(Lst_each_title_read[4])*60. +\
                         float(Lst_each_title_read[5])
        try:
            S_GNSS_num = int(Lst_each_title_read[7][0:2])
            I_GNSS_jump = 2 
        except:
            S_GNSS_num = int(Lst_each_title_read[7][0:1])
            I_GNSS_jump = 1 
        if S_GNSS_num > 12:
            S_GNSS_info = Lst_readlines[I_title_num_chose][32:].strip() + Lst_readlines[I_title_num_chose+1][32:].strip()
            I_title_num_chose += 1
        else:
            S_GNSS_info = Lst_readlines[I_title_num_chose][32:]
        I_title_num_chose += 1
        Lst_GNSS_info = [S_GNSS_info[3*j:3*j+3] for j in range(S_GNSS_num)]
    
        Ay_gps_L1_sing = np.zeros((1,32))
        Ay_gps_L1_slip = np.zeros((1,32)).astype('int')
        Ay_gps_L2_sing = np.zeros((1,32))
        Ay_gps_L2_slip = np.zeros((1,32)).astype('int')
        Ay_gps_P1_sing = np.zeros((1,32))
        Ay_gps_P2_sing = np.zeros((1,32))
        Ay_gps_C1_sing = np.zeros((1,32))
        Ay_gps_C2_sing = np.zeros((1,32))
        Ay_gps_S1_sing = np.zeros((1,32))
        Ay_gps_S2_sing = np.zeros((1,32))
    
        for S_gnss_chose in Lst_GNSS_info:
#            print(S_gnss_chose)
            if S_gnss_chose[0] == 'G':
                I_gps_num = int(S_gnss_chose[1:])-1 
                Lst_observ = [Lst_readlines[I_title_num_chose][k*16:k*16+16] for k in range(5)]
                try:
                    Lst_observ.pop(Lst_observ.index('\n'))
                except:
                    pass
                if I_numofOBStype > 5:
                    Lst_observ += [Lst_readlines[I_title_num_chose+1][k*16:(k+1)*14] for k in range(5)]
                try:
                    Ay_gps_L1_sing[0,I_gps_num] = float(Lst_observ[I_L1_loc][:14])
                    if Lst_observ[I_L1_loc][14] == '1' or Lst_observ[I_L1_loc][14] == '3' or Lst_observ[I_L1_loc][14] == '5' or Lst_observ[I_L1_loc][14] == '7':
                        Ay_gps_L1_slip[0,I_gps_num] = 1
                except:
                    print('L1 data lose? In line {0}'.format(I_title_num_chose))
                    pass
                try:
                    Ay_gps_L2_sing[0,I_gps_num] = float(Lst_observ[I_L2_loc][:14])
                    if Lst_observ[I_L2_loc][14] == '1' or Lst_observ[I_L2_loc][14] == '3' or Lst_observ[I_L2_loc][14] == '5' or Lst_observ[I_L2_loc][14] == '7':
                        Ay_gps_L2_slip[0,I_gps_num] = 1
                except:
                    pass
                try:
                    Ay_gps_P1_sing[0,I_gps_num] = float(Lst_observ[I_P1_loc][:14])
                except:
                    pass
                try:
                    Ay_gps_P2_sing[0,I_gps_num] = float(Lst_observ[I_P2_loc][:14])
                except:
                    pass
                try:
                    Ay_gps_C1_sing[0,I_gps_num] = float(Lst_observ[I_C1_loc][:14])
                except:
                    pass
                try:
                    Ay_gps_C2_sing[0,I_gps_num] = float(Lst_observ[I_C2_loc][:14])
                except:
                    pass
                try:
                    Ay_gps_S1_sing[0,I_gps_num] = float(Lst_observ[I_S1_loc][:14])
                except:
                    pass
                try:
                    Ay_gps_S2_sing[0,I_gps_num] = float(Lst_observ[I_S2_loc][:14])
                except:
                    pass
            if I_numofOBStype > 5:
                I_title_num_chose += 2
            elif I_numofOBStype <= 5:
                I_title_num_chose += 1
    except:
        I_title_num_chose += 1
        (I_title_num_chose,F_time_in_day,Ay_time,
           Ay_gps_L1_sing,Ay_gps_L2_sing,
           Ay_gps_L1_slip,Ay_gps_L2_slip,
           Ay_gps_P1_sing,Ay_gps_P2_sing,
           Ay_gps_C1_sing,Ay_gps_C2_sing,
           Ay_gps_S1_sing,Ay_gps_S2_sing) = Fun_info_get(Lst_readlines,I_title_num_chose)
    
    return(I_title_num_chose,F_time_in_day,Ay_time,
           Ay_gps_L1_sing,Ay_gps_L2_sing,
           Ay_gps_L1_slip,Ay_gps_L2_slip,
           Ay_gps_P1_sing,Ay_gps_P2_sing,
           Ay_gps_C1_sing,Ay_gps_C2_sing,
           Ay_gps_S1_sing,Ay_gps_S2_sing)

def do(I_year,I_month,I_day,S_station):
    I_doy = YMD2DOY(I_year,I_month,I_day)
    
    S_phase_data_path = r'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/phase_data/30s/'.format(I_year,I_doy)
    if not os.path.exists(S_phase_data_path):
        os.makedirs(S_phase_data_path)
    
    with open(r'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/odata/30s/{2}{1:03d}0.{0:02d}o'.format(I_year,I_doy,S_station)) as f:
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
#    I_year = 3
#    I_month = 11
#    I_day = 19
    I_year = 15
    I_month = 3
    I_day = 17
#    Lst_station_name = ['woos','gust']
    Lst_station_name = ['sun1','fenp']
#    Lst_station_name = ['woos','stkr','defi','metr','gust']
#    Lst_station_name = ['heri','pang','fenp','dajn']
#    S_station = 'dajn'
    for S_station in Lst_station_name:
        print(S_station)
        do(I_year,I_month,I_day,S_station)