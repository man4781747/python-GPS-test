# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:20:16 2018

@author: owo
"""

import sys
sys.path.append(r'./library')

import numpy as np
#import matplotlib.pyplot as plt
from ErrorVariance import Error_variance
from DOY2GPSweek import DOY2GPSweek
from Satellite_Calculate import Satellite_Calculate
from LeastSquaresPositioning import Positioning
from ErrorModule import Error_module
from TimeBreakDown import TimeBreakDown
from NDataRead import NDataRead
import xyz2llh
import xyz2enu
from CustomValue import *

global S_phase_data_path
global S_aeosv_data_path
global S_n_data_path
global S_ans_position_path
#global F_f1_hz
#global F_f2_hz 
#global F_err_cbias # code bias error std (m)
#global F_std_brdcclk # error of broadcast clock (m)
#global F_EFACT_GPS  # error factor: GPS 
#global F_ERR_BRDCI  # broadcast iono model error factor
#global F_ERR_SAAS
#global F_OMGE       # /* earth angular velocity (IS-GPS) (rad/s) */
#global F_C

#F_err_cbias = 0.3  # code bias error std (m)
#F_f1_hz = 1575.42
#F_f2_hz = 1227.6
#F_std_brdcclk = 30.0 # error of broadcast clock (m)
#F_EFACT_GPS = 1.0  # error factor: GPS 
#F_ERR_BRDCI = 0.5
#F_ERR_SAAS = 0.3   # /* saastamoinen model error std (m) */
#F_OMGE = 7.2921151467E-5  # /* earth angular velocity (IS-GPS) (rad/s) */
#F_C = 299792458.0

S_phase_data_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/phase_data/'
S_aeosv_data_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/aeosv_data/'
S_n_data_path = '/pub3/man4781747/GPS_data/n_data/'
S_ans_position_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/position_data/'
S_DGPS_Correction_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/DGPS_Correction_data/'
S_GIMRIM_TEC_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/GIM_svTEC/'

S_phase_data_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/phase_data/'
S_aeosv_data_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/aeosv_data/'
S_n_data_path = 'D:/Ddddd/python/2003/Odata/test/n_data/'
S_ans_position_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/position_data/'
S_DGPS_Correction_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/DGPS_Correction_data/'
S_GIMRIM_TEC_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/GIM_svTEC/'

def ez2do_every_thing(I_year,I_doy,S_station_name,F_elevation_filter=15.,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='No',Beta='No'):
    C_NData = NDataRead(S_n_data_path.format(I_year,I_doy)+'n_data_{0:02d}{1:03d}.npy'.format(I_year,I_doy)) 
    Ay_Pr_C1_Rover = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_station_name))[:,:32]
    Ay_AnsPosition_Rover = np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_station_name))[0,:]
    Ay_TimeRaw_Rover = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_year,I_doy,S_station_name))[:,0:6]
    Ay_Time_Rover = Ay_TimeRaw_Rover[:,3]*3600.+Ay_TimeRaw_Rover[:,4]*60.+Ay_TimeRaw_Rover[:,5]

    if S_ion_model=='C1P2':
       Ay_Pr_P2_Rover = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseP2.npy'.format(I_year,I_doy,S_station_name))[:,:32]
       Ay_Pr_P2_Rover[np.where(Ay_Pr_C1_Rover==0)]=0
       Ay_Pr_C1_Rover[np.where(Ay_Pr_P2_Rover==0)]=0    
    
    if S_DGPS != 'No':
        Ay_Pr_C1_Base       = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_DGPS))[:,:32]
        Ay_AnsPosition_Base = np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_DGPS))[0,:]
        Ay_TimeRaw_Base     = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_year,I_doy,S_DGPS))[:,0:6]
        Ay_Time_Base        = Ay_TimeRaw_Base[:,3]*3600.+Ay_TimeRaw_Base[:,4]*60.+Ay_TimeRaw_Base[:,5]
#        '''
#        test
#        '''
        if Beta != 'No':
            global Ay_base_sTEC,Ay_rover_sTEC
#            Ay_base_sTEC  = np.load(S_aeosv_data_path.format(I_year,I_doy)+'30s/s{0}{1:03d}.npy'.format(S_DGPS, I_doy))[:,:32]
#            Ay_rover_sTEC = np.load(S_aeosv_data_path.format(I_year,I_doy)+'30s/s{0}{1:03d}.npy'.format(S_station_name, I_doy))[:,:32]
            Ay_base_sTEC  = np.load(S_aeosv_data_path.format(I_year,I_doy)+'s{0}{1:03d}test_nearest_v2s.npy'.format(S_DGPS, I_doy))[:,:32]
            Ay_rover_sTEC = np.load(S_aeosv_data_path.format(I_year,I_doy)+'s{0}{1:03d}test_nearest_v2s.npy'.format(S_station_name, I_doy))[:,:32]


    I_loop_num = 0
    test = np.zeros((len(Ay_Pr_C1_Rover[:,0]),3))
    test_DGPS = np.zeros((len(Ay_Pr_C1_Rover[:,0]),3))
    test_GDOP = np.zeros((len(Ay_Pr_C1_Rover[:,0]),1))
    test_GDOP_DGPS = np.zeros((len(Ay_Pr_C1_Rover[:,0]),1))
    Ay_OutPut_xyz = np.zeros((len(Ay_Pr_C1_Rover[:,0]),3))
    
    test_dTEC = np.zeros((2880,32))
    
    for I_time_chose in range(len(Ay_Pr_C1_Rover[:,0])):
#    for I_time_chose in range(1):
#    for I_time_chose in np.zeros(1).astype('int')+332:
#    for I_time_chose in np.arange(161, 164,1):
        try:
            S_info = "\r{0} ,Y:{1:02d} ,D:{2:03d} ,Elevation:{5:2.2f} ,ionofree:{4} ,DGPS:{6} ,now in {3:2.2f}%\r".format(S_station_name,
                        I_year,
                        I_doy,
                        (I_time_chose/float(len(Ay_Pr_C1_Rover[:,0])))*100 
                        ,S_ion_model,
                        F_elevation_filter,
                        S_DGPS)
#            print(S_info,end='')
            C_TimeRover = TimeBreakDown(Ay_Time_Rover[I_time_chose])
            Ay_NDataChose_Rover, Ay_SateChoseNum_Rover = C_NData.GetData(Ay_Pr_C1_Rover[I_time_chose], C_TimeRover.F_TimeTotal)
#            print(Ay_Pr_C1_Rover[I_time_chose,4])
#            print(Ay_SateChoseNum_Rover)
            if len(np.where(Ay_Pr_C1_Rover[I_time_chose,:] != 0.)[0]) >= 4:    
                Ay_PrChose_C1_Rover = Ay_Pr_C1_Rover[I_time_chose,Ay_SateChoseNum_Rover] 
                if S_ion_model=='C1P2':
                    Ay_PrChose_P2_Rover = Ay_Pr_P2_Rover[I_time_chose,Ay_SateChoseNum_Rover] 
            

                F_GPSWeek_Sec= (float(DOY2GPSweek(I_year,I_doy))%10)*24*60*60  
                Ay_ReceiverDelay_Rover = 0

                Mobj_sate_cal = Satellite_Calculate(Ay_NDataChose_Rover)
                Ay_SateTimeDelay_Rover = Mobj_sate_cal.get_sate_clock_error(Ay_PrChose_C1_Rover,C_TimeRover.I_TimeInt,C_TimeRover.F_TimeDecimal,F_GPSWeek_Sec)
                sva_Rover = Mobj_sate_cal.sva
                tgd_Rover = Mobj_sate_cal.tgd
                (Ay_xk,Ay_yk,Ay_zk,Ay_SateTimeDelay_Rover) = Mobj_sate_cal.get_sate_position(
                                                        C_TimeRover.I_TimeInt,C_TimeRover.F_TimeDecimal,
                                                        F_GPSWeek_Sec,Ay_SateTimeDelay_Rover,Ay_PrChose_C1_Rover)    
    
                Mobj_error_variance = Error_variance()
                Ay_vare = Mobj_error_variance.vare(sva_Rover)
                Ay_vmeas = Mobj_error_variance.vmeas()
                if I_loop_num == 0:
                    F_test_point_x = 0.000000001
                    F_test_point_y = 0.
                    F_test_point_z = 0.
                    Ay_guess_position = np.array([[F_test_point_x],[F_test_point_y],[F_test_point_z]])
                    I_loop_num = 1
                Ay_elevation = np.zeros(len(Ay_xk)) + np.pi/2
                Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                Ay_fix_position = np.array([100,100,100])
                TF_tgd_fix = True
                I_loop_break = 0
                while abs(Ay_fix_position[0]) > 1e-4 or abs(Ay_fix_position[1]) > 1e-4 or abs(Ay_fix_position[2]) > 1e-4:
                    Ay_guess_position_llh = np.zeros((3,len(Ay_PrChose_C1_Rover)))
                    for j in range(len(Ay_PrChose_C1_Rover)):
                        Ay_guess_position_llh[:,j] = np.array([xyz2llh.xyz2llh(Ay_guess_position[0],Ay_guess_position[1],Ay_guess_position[2]).xyz()])
                    
                    Ay_varerr = Mobj_error_variance.varerr(Ay_elevation,S_ion_model)

                    Mobj_delay = Error_module()
                    if S_ion_model == 'broadcast' or S_DGPS != 'No':
                        S_n_data_path_ = S_n_data_path.format(I_year,I_doy)+'n_data_{0:02d}{1:03d}_ion.npy'.format(I_year,I_doy)
                        Ay_dion = Mobj_delay.iono_model_broadcast(I_year,I_doy,
                                                                  Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                  Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                  Ay_elevation,
                                                                  Ay_enu_resever_sate,
                                                                  C_TimeRover.F_TimeTotal,
                                                                  S_n_data_path_
                                                                  )
                    else:
                        Ay_dion = 0
                    Ay_vion = Mobj_error_variance.vion(I_loop_break,S_ion_model,Ay_dion,S_DGPS)
                    if S_trp_model == 'saastamoinen':
                        Ay_dtrp = Mobj_delay.saastamoinen_model(Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                Ay_guess_position_llh[2,:],
                                                                Ay_elevation,
                                                                0.6)
                    else:  
                        Ay_dtrp = 0
                    Ay_vtrp = Mobj_error_variance.vtrp(I_loop_break,S_trp_model,Ay_elevation)
                    Ay_error_variance_all = Ay_varerr + Ay_vmeas + Ay_vare + Ay_vion + Ay_vtrp 
                    Ay_error_variance_all = np.zeros_like(Ay_error_variance_all)+1
                    Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
                    Ay_guess_range_list_first = np.copy(Ay_beacon_position)
                    for nn in range(len(Ay_guess_range_list_first[0,:])):
                        Ay_guess_range_list_first[:,nn] -= Ay_guess_position[:,0]
                    Ay_guess_range_list = np.sum((Ay_guess_range_list_first)**2,0)**0.5
                    Ay_guess_range_list_ = np.sum((Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_xk*Ay_guess_position[1]-Ay_yk*Ay_guess_position[0])/F_C
                    if TF_tgd_fix:
                        F_gamma = F_f1_hz**2/F_f2_hz**2
                        if S_ion_model != 'C1P2':
                            Ay_P1_P2 = (1.0-F_gamma)*tgd_Rover*F_C
                            Ay_PrChose_C1_Rover = Ay_PrChose_C1_Rover - Ay_P1_P2/(1.0-F_gamma)
#                            print(Ay_pseudo_range[-1])
                        else:
                            Ay_PrChose_C1_Rover = (F_gamma*Ay_PrChose_C1_Rover - Ay_PrChose_P2_Rover)/(F_gamma-1)
                        TF_tgd_fix = False
                    Ay_pseudo_range_fix = Ay_PrChose_C1_Rover + F_C*Ay_SateTimeDelay_Rover - Ay_ReceiverDelay_Rover - Ay_dtrp -Ay_dion
#                    print(Ay_PrChose_C1_Rover)
#                    print(Ay_beacon_position)
                    Mobj_get_position_fst = Positioning(Ay_pseudo_range_fix[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                        Ay_guess_range_list[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                        Ay_guess_range_list_[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                        Ay_beacon_position[:,np.where(Ay_elevation > F_elevation_filter/180*np.pi)[0]],
                                                        Ay_guess_position,
                                                        Ay_error_variance_all[np.where(Ay_elevation > F_elevation_filter/180*np.pi)])
                    
                    '''
                    更新下列數值
                    Ay_guess_position
                    Ay_resever_time_delay
                    Ay_enu_resever_sate
                    Ay_elevation
                    Ay_fix_position
                    '''
                    Ay_guess_position = Mobj_get_position_fst.Positioning_results()[0]
                    Ay_ReceiverDelay_Rover = Mobj_get_position_fst.Positioning_results()[1] + Ay_ReceiverDelay_Rover
                    Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                    Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
                    Ay_fix_position = Mobj_get_position_fst.Positioning_results()[2]
                    if I_loop_break > 10:
                        print('test_break')
                        break
                    I_loop_break += 1
                
                Ay_OutPut_xyz[I_time_chose] = Ay_guess_position[:,0]
                test_GDOP[I_time_chose,0] = Mobj_get_position_fst.F_GDOP
                Ay_ENU = xyz2enu.xyz2enu(np.array([Ay_guess_position[:,0]]),
                               np.array([Ay_AnsPosition_Rover])
                               ).return_enu()
                test[I_time_chose] = Ay_ENU[0,:]
                if S_DGPS != 'No':
                    C_TimeBase = TimeBreakDown(Ay_Time_Base[I_time_chose])
                    Ay_NDataChose_Base, Ay_SateChoseNum_Base = C_NData.GetData(Ay_Pr_C1_Base[I_time_chose], C_TimeBase.F_TimeTotal)
                    
                    '''
                    Mobj_sate_cal_DGPS_before                   : 基站衛星計算 Mobj
                    Ay_delta_t_sv_DGPS_before                   : 基站衛星時鐘誤差
                    Ay_pseudo_range_DGPS_berofe                 : 基站選取的偽距
                    Ay_xk_DGPS_before,Ay_yk_DGPS_before,Ay_zk_DGPS_before
                                                                : 基站衛星位置 ECEF
                    '''
                    Ay_PrChose_C1_Base = Ay_Pr_C1_Base[I_time_chose,Ay_SateChoseNum_Base] 
                    
                    Mobj_SateCal_Base = Satellite_Calculate(Ay_NDataChose_Base)
                    Ay_SateTimeDelay_Base = Mobj_SateCal_Base.get_sate_clock_error(Ay_PrChose_C1_Base,
                                                                                   C_TimeBase.I_TimeInt,
                                                                                   C_TimeBase.F_TimeDecimal,
                                                                                   F_GPSWeek_Sec)
#                    sva_DGPS_before = Mobj_sate_cal_DGPS_before.sva
                    tgd_Base = Mobj_SateCal_Base.tgd
                    (Ay_xk_Base,Ay_yk_Base,Ay_zk_Base,Ay_SateTimeDelay_Base) = Mobj_SateCal_Base.get_sate_position(
                                                            C_TimeBase.I_TimeInt,C_TimeBase.F_TimeDecimal,
                                                            F_GPSWeek_Sec,Ay_SateTimeDelay_Base,Ay_PrChose_C1_Base)

                    '''
                    基站 TGD修正
                    '''

                    Ay_P1_P2_DGPS = (1.0-F_gamma)*tgd_Base*F_C
                    Ay_PrChose_C1_Base = Ay_PrChose_C1_Base - Ay_P1_P2_DGPS/(1.0-F_gamma)
                    
                    '''
                    ### 基站衛星位置 ###
                    Ay_beacon_position_DGPS_before(x,y,z)    (3,N)
                    '''
                    Ay_SatePosition_Base = np.array([Ay_xk_Base,Ay_yk_Base,Ay_zk_Base])
                    
                    '''
                    ### 基站真實距離計算 ###
                    Ay_guess_range_list_DGPS_before   基站"不"考慮旋轉後的真實距離
                    Ay_guess_range_list_DGPS_before_  基站考慮旋轉後的真實距離
                    '''
                    Ay_guess_range_list_DGPS_before_first = np.copy(Ay_SatePosition_Base)
                    for nn in range(len(Ay_guess_range_list_DGPS_before_first[0,:])):
                        Ay_guess_range_list_DGPS_before_first[:,nn] -= Ay_AnsPosition_Base
                    Ay_guess_range_list_DGPS_before_ = np.sum((Ay_guess_range_list_DGPS_before_first)**2,0)**0.5 + F_OMGE*(Ay_xk_Base*Ay_AnsPosition_Base[1]-Ay_yk_Base*Ay_AnsPosition_Base[0])/F_C

                    
                    
                    '''
                    基站/測站 衛星配對
                    Ay_sate_match_raver                     : 測站衛星位置碼
                    Ay_pseudo_range_DGPS_chose_rover        : 測站偽距選取
                    Ay_sate_match_base                      : 基站衛星位置碼
                    Ay_pseudo_range_DGPS_chose_base         : 基站偽距選取
                    '''
                    
                    if Beta != 'No':
                        I_time_index = int(round(C_TimeRover.F_TimeTotal/30))
                        Ay_TEC_chose_base_index  = np.where(Ay_base_sTEC[I_time_index,:] != 0)[0]
                        Ay_TEC_chose_rover_index = np.where(Ay_rover_sTEC[I_time_index,:] != 0)[0]

                        Lst_sate_match = list(set(Ay_SateChoseNum_Rover)&
                                              set(Ay_SateChoseNum_Base)&
                                              set(Ay_TEC_chose_base_index)&
                                              set(Ay_TEC_chose_rover_index))
                        
                        Ay_sate_match_raver = np.zeros(len(Lst_sate_match)).astype('int')
                        Ay_sate_match_base = np.zeros(len(Lst_sate_match)).astype('int')
                        Ay_sTEC_match_raver = np.zeros(len(Lst_sate_match)).astype('int')
                        Ay_sTEC_match_base = np.zeros(len(Lst_sate_match)).astype('int')     

                        for I_sate_chose in range(len(Lst_sate_match)):
                            Ay_sate_match_raver[I_sate_chose] = int(np.where(Ay_SateChoseNum_Rover == Lst_sate_match[I_sate_chose])[0])
                            Ay_sate_match_base[I_sate_chose]  = int(np.where(Ay_SateChoseNum_Base  == Lst_sate_match[I_sate_chose])[0])
                            Ay_sTEC_match_raver[I_sate_chose] = int(np.where(Ay_TEC_chose_rover_index == Lst_sate_match[I_sate_chose])[0])
                            Ay_sTEC_match_base[I_sate_chose]  = int(np.where(Ay_TEC_chose_base_index == Lst_sate_match[I_sate_chose])[0])
                        
                        Ay_TECChose_Base = Ay_base_sTEC[I_time_index,Ay_TEC_chose_base_index][Ay_sTEC_match_base]
                        Ay_TECChose_Rover = Ay_rover_sTEC[I_time_index,Ay_TEC_chose_rover_index][Ay_sTEC_match_raver]
                        
                    else:
                        Lst_sate_match = list(set(Ay_SateChoseNum_Rover)&
                                              set(Ay_SateChoseNum_Base))             
                    
                        Ay_sate_match_raver = np.zeros(len(Lst_sate_match)).astype('int')
                        Ay_sate_match_base = np.zeros(len(Lst_sate_match)).astype('int')   
                        
                        for I_sate_chose in range(len(Lst_sate_match)):
                            Ay_sate_match_raver[I_sate_chose] = int(np.where(Ay_SateChoseNum_Rover == Lst_sate_match[I_sate_chose])[0])
                            Ay_sate_match_base[I_sate_chose]  = int(np.where(Ay_SateChoseNum_Base  == Lst_sate_match[I_sate_chose])[0])

                        Ay_TECChose_Base = 0
                        Ay_TECChose_Rover = 0

                    Ay_pseudo_range_DGPS_chose_rover = Ay_PrChose_C1_Rover[Ay_sate_match_raver[:]]
                    Ay_pseudo_range_DGPS_chose_base  = Ay_PrChose_C1_Base[Ay_sate_match_base[:]]
                    

                    

                    Ay_TEC_delay_base = Ay_TECChose_Base*(40.3*(10**16))/((F_f1_hz*10**6)**2)
                    Ay_TEC_delay_rover = Ay_TECChose_Rover*(40.3*(10**16))/((F_f1_hz*10**6)**2)
                    
                    
                    for i in range(3):
                        Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
                        Ay_guess_range_list_first = np.copy(Ay_beacon_position)
                        for nn in range(len(Ay_guess_range_list_first[0,:])):
                            Ay_guess_range_list_first[:,nn] -= Ay_guess_position[:,0]
                        Ay_guess_range_list = np.sum((Ay_guess_range_list_first)**2,0)**0.5
                        Ay_guess_range_list_ = np.sum((Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_xk*Ay_guess_position[1]-Ay_yk*Ay_guess_position[0])/F_C
                        
                        '''
                        Ay_pseudo_range_fix_DGPS             : 測站修過 DGPS 的偽距
                                                               測站偽距 - ( 基站偽距 - 基站真實距離(修過自轉) ) - 測站時鐘誤差
                                                               
                        Mobj_get_position_DGPS         : 定位矩陣(
                                                                Ay_pseudo_range_fix_DGPS       : 測站修過 DGPS 的偽距
                                                                Ay_guess_range_list            : 猜測點與測站衛星距離(m) 無修正轉動
                                                                Ay_guess_range_list_           : 猜測點與測站衛星距離(m) 有修正轉動
                                                                Ay_beacon_position             : 測站衛星位置
                                                                Ay_guess_position              : 猜測點
                                                                Ay_error_variance_all          : 品質權重
                                                                )
                        '''
                        
                        Ay_pseudo_range_fix_DGPS = (Ay_pseudo_range_DGPS_chose_rover-Ay_TEC_delay_rover) - ((Ay_pseudo_range_DGPS_chose_base-Ay_TEC_delay_base) - Ay_guess_range_list_DGPS_before_[Ay_sate_match_base[:]]) - Ay_ReceiverDelay_Rover
                        
#                        Ay_pseudo_range_fix_DGPS = (Ay_pseudo_range_DGPS_chose_rover) - ((Ay_pseudo_range_DGPS_chose_base) - Ay_guess_range_list_DGPS_before_[Ay_sate_match_base[:]]) - Ay_ReceiverDelay_Rover
#
#                        print(test_dTEC[I_time_index,Ay_TEC_chose_base_index])
#                        print(test_dTEC[I_time_index,Ay_TEC_chose_base_index[Ay_sTEC_match_base]])
#                        print(Ay_TEC_delay_rover-Ay_TEC_delay_base)
#                        test_dTEC[I_time_index,Ay_TEC_chose_base_index[Ay_sTEC_match_base]] = Ay_TEC_delay_rover-Ay_TEC_delay_base
                        Mobj_get_position_DGPS = Positioning(Ay_pseudo_range_fix_DGPS[np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)],
                                        Ay_guess_range_list[Ay_sate_match_raver[:]][np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)],
                                        Ay_guess_range_list_[Ay_sate_match_raver[:]][np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)],
                                        Ay_beacon_position[:,Ay_sate_match_raver[:]][:,np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)[0]],
                                        Ay_guess_position,
                                        Ay_error_variance_all[Ay_sate_match_raver[:]][np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)])
                        '''
                        更新下列數值
                        Ay_guess_position
                        Ay_resever_time_delay
                        Ay_enu_resever_sate
                        Ay_elevation
                        '''
                        Ay_guess_position = Mobj_get_position_DGPS.Positioning_results()[0]
                        Ay_ReceiverDelay_Rover = Mobj_get_position_DGPS.Positioning_results()[1] + Ay_ReceiverDelay_Rover
                        Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                        Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
                        Ay_ENU = xyz2enu.xyz2enu(np.array([Ay_guess_position[:,0]]),
                                       np.array([Ay_AnsPosition_Rover])
                                       ).return_enu()
                        test_DGPS[I_time_chose] = Ay_ENU[0,:]
                        Ay_fix_position = Mobj_get_position_DGPS.Positioning_results()[2]
#                        print(Ay_fix_position)
#                        print(Mobj_get_position_DGPS.Positioning_results()[1])
                    test_GDOP_DGPS[I_time_chose,0] = Mobj_get_position_DGPS.F_GDOP
                    print(Ay_guess_position)
        except:
            test[I_time_chose] = np.nan
            test_DGPS[I_time_chose] = np.nan
            print('ERROR')
    return test,Ay_OutPut_xyz,test_DGPS,test_GDOP,test_GDOP_DGPS,test_dTEC

        
if __name__ == '__main__':
#    I_year = 3
#    I_doy = 324
#
#
#    S_station = 'woos'
#    test,test_DGPS,test_GDOP,test_GDOP_DGPS,test_dTEC = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='gust')


    I_year = 15
    I_doy = 73


    S_station = 'sun1'
#    test,Ay_OutPut_xyz,test_DGPS,test_GDOP,test_GDOP_DGPS,test_dTEC = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='fenp')
    test,Ay_OutPut_xyz,test_DGPS,test_GDOP,test_GDOP_DGPS,test_dTEC = ez2do_every_thing(I_year,I_doy,S_station,S_DGPS='fenp')
#    test,Ay_OutPut_xyz,test_DGPS,test_GDOP,test_GDOP_DGPS,test_dTEC = ez2do_every_thing(I_year,I_doy,S_station)
#    np.save(r'D:\google drive\我der碩士論文\磁暴\磁暴各定位結果\woos_DPGS_gust_v2sfit_nearest版.npy', test_DGPS)
#    np.save(r'D:\google drive\我der碩士論文\磁暴\磁暴各定位結果\woos_DPGS_gust_GDOP_v2sfit_nearest版.npy', test_GDOP_DGPS)
    

#    test,test_DGPS,test_GDOP,test_GDOP_DGPS,test_dTEC = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='fenp')
    

#    test,test_DGPS = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen')
#    test,test_DGPS = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='C1P2',S_trp_model='saastamoinen')
#    I_year = 3
#    I_doy = 324
#
#    S_station = 'woos'
#    test,test_DGPS = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='gust')
##    
#    test,test_DGPS = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='fenp')
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\{1}_sin_{0:03d}_broadcast.npy'.format(I_doy,S_station ),test)
#
#    test = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='No')
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\{1}_sin_{0:03d}_noionfree.npy'.format(I_doy,S_station ),test)
#    
#    test = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='C1P2')
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\{1}_sin_{0:03d}_C1P2.npy'.format(I_doy,S_station ),test)
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_broadcast.npy'.format(I_day),test_ENU)
#

#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_noionfree.npy'.format(I_day),test_ENU) 