# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:58:32 2018

@author: owo
"""

import numpy as np 
import matplotlib.pyplot as plt
from DOY2GPSweek import DOY2GPSweek
from GNSS_positioning_argv_ver2 import *
import xyz2enu
import LDL_decomposition as LDL
import LAMBDA
from GNSS_positioning_argv_ver2 import Error_module
from xyz2llh import xyz2llh
import nmf

global F_OMGE       # /* earth angular velocity (IS-GPS) (rad/s) */
global F_C

F_OMGE = 7.2921151467E-5  # /* earth angular velocity (IS-GPS) (rad/s) */
F_C = 299792458.0

F_L1_eave_length = (299792458.0/1.57542e9) #(m)


S_Base = 'fenp'
S_Rover = 'sun1'
#S_Base = 'pepu'
#S_Rover = 'hual'
I_Year = 15
I_doy = 73


#S_Base = 'gust'
#S_Rover = 'woos'
#I_Year = 3
#I_doy = 323



I_dt = 30.
'''
測試檔案位置
'''
S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phaseC1.npy'.format(I_Year, I_doy, S_Rover)
S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phaseL1.npy'.format(I_Year, I_doy, S_Rover)
S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phaseC1.npy'.format(I_Year, I_doy, S_Base)
S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phaseL1.npy'.format(I_Year, I_doy, S_Base)
S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phasetime.npy'.format(I_Year, I_doy, S_Rover)
S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phasetime.npy'.format(I_Year, I_doy, S_Base)
S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_{0:02d}{1:03d}.npy'.format(I_Year, I_doy, S_Rover)
S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\position_data\{2}{0:02d}{1:03d}_position.npy'.format(I_Year, I_doy, S_Rover)
S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\position_data\{2}{0:02d}{1:03d}_position.npy'.format(I_Year, I_doy, S_Base)
S_L1_silp_path_a = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phaseL1_slip.npy'.format(I_Year, I_doy, S_Rover)
S_L1_silp_path_b = r'D:\Ddddd\python\2003\Odata\test\data20{0:02d}{1:03d}\phase_data\30s\{2}{0:02d}{1:03d}phaseL1_slip.npy'.format(I_Year, I_doy, S_Base)

#S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phaseC1.npy'
#S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phaseL1.npy'
#S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phaseC1.npy'
#S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phaseL1.npy'
#S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phasetime.npy'
#S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phasetime.npy'
#S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15073.npy'
#S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\position_data\hual15073_position.npy'
#S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\position_data\pepu15073_position.npy'
#S_L1_silp_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phaseL1_slip.npy'
#S_L1_silp_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phaseL1_slip.npy'
'''
讀取檔案
L1 資料在o檔內單位為 '相位' 因此必須乘上波長使之變成長度單位
單位: m
'''
Ay_C1_a = np.load(S_C1_data_path_a)[:,:32]
Ay_L1_a = np.load(S_L1_data_path_a)[:,:32]*F_L1_eave_length
Ay_C1_b = np.load(S_C1_data_path_b)[:,:32]
Ay_L1_b = np.load(S_L1_data_path_b)[:,:32]*F_L1_eave_length

Ay_check_array = np.where((Ay_C1_a==0.)|(Ay_L1_a==0.))
Ay_C1_a[Ay_check_array] = 0.
Ay_L1_a[Ay_check_array] = 0.
Ay_check_array = np.where((Ay_C1_b==0.)|(Ay_L1_b==0.))
Ay_C1_b[Ay_check_array] = 0.
Ay_L1_b[Ay_check_array] = 0.

Ay_L1_slip_a = np.load(S_L1_silp_path_a)[:,:32]
Ay_L1_slip_b = np.load(S_L1_silp_path_b)[:,:32]

Ay_time_a = np.load(S_a_time_path)
Ay_time_b = np.load(S_b_time_path)
Ay_n_data = np.load(S_n_data_path)
Ay_position_a = np.load(S_a_position_path)[0:1,:]
Ay_position_b = np.load(S_b_position_path)[0:1,:]
#Ay_position_b = np.array([[-3055302.1000,4964313.4140,2580107.1000]])
Ay_position_b_llh = xyz2llh(Ay_position_b[0,0],Ay_position_b[0,1],Ay_position_b[0,2]).xyz()

#Ay_position_a_guess_all = np.load(r'D:\github\python_code\GPS_position\test.npy')
Ay_position_a_guess_all = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\PositioningOutput\possun115073_broadcast.npy')
#Ay_position_a_guess_all = np.load(r'D:\Ddddd\python\2003\Odata\test\data2003324\PositioningOutput\poswoos03324_broadcast.npy')



#Ay_position_a_guess_all[314] = np.array([ -3056583.9930276028,4965781.9920758503,2575815.6475489931])


'''
Ay_time_a, Ay_time_b : 兩站所記錄的時間     單位: s
F_gpsweektime : GPS紀錄的時間(秒)在當周的星期日開始算起 單位: s
'''

Ay_time_a = Ay_time_a[:,3]*3600+Ay_time_a[:,4]*60+Ay_time_a[:,5]
Ay_time_b = Ay_time_b[:,3]*3600+Ay_time_b[:,4]*60+Ay_time_b[:,5]

F_gpsweektime = (float(DOY2GPSweek(I_Year,I_doy))%10)*24*60*60

Ay_N_SD_all = np.zeros((2880,32))
Ay_P_all    = np.zeros((32+3,3+32))
Ay_X_all    = np.zeros((2880,3))
Ay_ENU_all = np.zeros((2880,3))

test_all = []
#for I_time_chose in range(2880):
for I_time_chose in range(3): 
    try:
        '''
        F_time_get_a : a站所記錄的時間
        F_time_get_b : 以 F_time_get_a 找尋b站相對應時間
        '''
        F_time_get_a = Ay_time_a[I_time_chose]
        F_time_get_b = Ay_time_b[np.where((Ay_time_b>=F_time_get_a-0.5)&(Ay_time_b<=F_time_get_a+0.5))][0]
        
        '''
        Ay_L1,C1_chose_a,b : 對應時間下兩站各自的 L1 ,C1 量測值 
        '''
        Ay_L1_chose_a = Ay_L1_a[I_time_chose]
        Ay_C1_chose_a = Ay_C1_a[I_time_chose]
        Ay_L1_chose_b = Ay_L1_b[np.where((Ay_time_b>=F_time_get_a-0.5)&(Ay_time_b<=F_time_get_a+0.5))][0]
        Ay_C1_chose_b = Ay_C1_b[np.where((Ay_time_b>=F_time_get_a-0.5)&(Ay_time_b<=F_time_get_a+0.5))][0]
    
        Ay_slip_chose_a = Ay_L1_slip_a[I_time_chose]
        Ay_slip_chose_b = Ay_L1_slip_b[np.where((Ay_time_b>=F_time_get_a-0.5)&(Ay_time_b<=F_time_get_a+0.5))][0]
    
        '''
        計算 a,b 兩站的接收機時間(整數,小數 分開計算)
        '''
        F_a_timechose_int   = int(F_time_get_a)
        F_a_timechose_float = F_time_get_a%1
        F_a_timechose_total = F_time_get_a
        
        F_b_timechose_int   = int(F_time_get_b)
        F_b_timechose_float = F_time_get_b%1
        F_b_timechose_total = F_time_get_b
    
        '''
        Ay_sate_n_data_a,b : 依有資料的衛星來選取 n data
        Ay_sate_chose_a    : 選取的衛星編號
        Ay_C1_a,b_chose    : 相對應衛星的C1資料
        '''
        Ay_sate_n_data_a = Get_n_data_each_time(I_time_chose,Ay_C1_a,Ay_n_data,F_a_timechose_total)[::-1]
        Ay_sate_chose_a = Ay_sate_n_data_a[:,0].astype('int')-1
        Ay_sate_n_data_b = Get_n_data_each_time(np.where((Ay_time_b>=F_time_get_a-0.5)&(Ay_time_b<=F_time_get_a+0.5))[0][0],
                                                Ay_C1_b,Ay_n_data,F_b_timechose_total)[::-1]
        Ay_sate_chose_b = Ay_sate_n_data_b[:,0].astype('int')-1
    
        Ay_sate_chose_all = np.array(list(set(list(Ay_sate_chose_a))&set(list(Ay_sate_chose_b))))
    
        Ay_sate_n_data_a_ = np.zeros((len(Ay_sate_chose_all),38))
        Ay_sate_n_data_b_ = np.zeros((len(Ay_sate_chose_all),38))
        for I_i in range(len(Ay_sate_chose_all)):
            Ay_sate_n_data_a_[I_i] = Ay_sate_n_data_a[np.where(Ay_sate_n_data_a[:,0]==Ay_sate_chose_all[I_i]+1)][0]
            Ay_sate_n_data_b_[I_i] = Ay_sate_n_data_b[np.where(Ay_sate_n_data_b[:,0]==Ay_sate_chose_all[I_i]+1)][0]
        Ay_sate_n_data_a = Ay_sate_n_data_a_
        Ay_sate_n_data_b = Ay_sate_n_data_b_
        
        '''
        Mobj_sate_cal_a,b       : 計算 測站 衛星相關資料 (Mobj)
        Ay_delta_t_sv_a,b       : 衛星時終誤差 (s)   (一開始粗略估計,而後求出精準)
        Ay_xk,Ay_yk,Ay_zk       : 測站所有衛星位置(m) (ECEF)
        '''
        Mobj_sate_cal_a = Satellite_Calculate(Ay_sate_n_data_a)
        Ay_delta_t_sv_a = Mobj_sate_cal_a.get_sate_clock_error(Ay_C1_chose_a[Ay_sate_chose_all],F_a_timechose_int,F_a_timechose_float,F_gpsweektime)
        (Ay_xk_a,Ay_yk_a,Ay_zk_a,Ay_delta_t_sv_a) = Mobj_sate_cal_a.get_sate_position(
                                                F_a_timechose_int,F_a_timechose_float,
                                                F_gpsweektime,Ay_delta_t_sv_a,Ay_C1_chose_a[Ay_sate_chose_all])    
        Ay_sate_position_a = np.array([Ay_xk_a,Ay_yk_a,Ay_zk_a]).T        #OK
        
        Mobj_sate_cal_b = Satellite_Calculate(Ay_sate_n_data_b)
        Ay_delta_t_sv_b = Mobj_sate_cal_b.get_sate_clock_error(Ay_C1_chose_b[Ay_sate_chose_all],F_b_timechose_int,F_b_timechose_float,F_gpsweektime)
        (Ay_xk_b,Ay_yk_b,Ay_zk_b,Ay_delta_t_sv_b) = Mobj_sate_cal_b.get_sate_position(
                                                F_b_timechose_int,F_b_timechose_float,
                                                F_gpsweektime,Ay_delta_t_sv_b,Ay_C1_chose_b[Ay_sate_chose_all])  
        Ay_sate_position_b = np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T 
        
        '''
        計算各衛星對a,b 兩站的仰角
        Ay_elevation : b站對所有衛星仰角(弧度)
        I_ele_max_sate : 仰角最大衛星
        '''
        
        Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T,Ay_position_b).return_enu()
        Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
        Ay_ele_chose = np.where(Ay_elevation >= 15.*np.pi/180.)[0]
        
        Ay_sate_chose_all=Ay_sate_chose_all[Ay_ele_chose]
        
        Ay_L1_chose_a = Ay_L1_chose_a[Ay_sate_chose_all]
        Ay_C1_chose_a = Ay_C1_chose_a[Ay_sate_chose_all]
        Ay_L1_chose_b = Ay_L1_chose_b[Ay_sate_chose_all]
        Ay_C1_chose_b = Ay_C1_chose_b[Ay_sate_chose_all]
        
        Ay_slip_chose_a = Ay_slip_chose_a[Ay_sate_chose_all]
        Ay_slip_chose_b = Ay_slip_chose_b[Ay_sate_chose_all]
        
        Ay_delta_t_sv_a = Ay_delta_t_sv_a[Ay_ele_chose]
        Ay_delta_t_sv_b = Ay_delta_t_sv_b[Ay_ele_chose]
        
        Ay_elevation = Ay_elevation[Ay_ele_chose]
        I_ele_max = np.where(Ay_elevation==max(Ay_elevation))[0][0]
        
        Ay_xk_a = Ay_xk_a[Ay_ele_chose]
        Ay_yk_a = Ay_yk_a[Ay_ele_chose]
        Ay_zk_a = Ay_zk_a[Ay_ele_chose]
        Ay_xk_b = Ay_xk_b[Ay_ele_chose]
        Ay_yk_b = Ay_yk_b[Ay_ele_chose]
        Ay_zk_b = Ay_zk_b[Ay_ele_chose]
        
        '''
        計算測站與衛星間地理距離
        Ay_geographical_distance_b  : b基站與衛星的地理距離(修正自轉及衛星時鐘誤差)
        Ay_geographical_distance_a  : a測站與衛星的地理距離(猜測)(修正自轉及衛星時鐘誤差)
        '''
        
        Ay_geographical_distance_b =((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5\
                                    + F_OMGE*(Ay_xk_b*Ay_position_b[0,1]-Ay_yk_b*Ay_position_b[0,0])/F_C - Ay_delta_t_sv_b*F_C   
    
        Ay_position_a_guess = Ay_position_a_guess_all[I_time_chose:I_time_chose+1,:]
        Ay_geographical_distance_a =((Ay_xk_a-Ay_position_a_guess[0,0])**2+(Ay_yk_a-Ay_position_a_guess[0,1])**2+(Ay_zk_a-Ay_position_a_guess[0,2])**2)**0.5\
                                    + F_OMGE*(Ay_xk_a*Ay_position_a_guess[0,1]-Ay_yk_a*Ay_position_a_guess[0,0])/F_C - Ay_delta_t_sv_a*F_C
        
    
        Mobj_b_base_Error = Error_module()
        Ay_position_a_guess_llh = xyz2llh(Ay_position_a_guess[0,0],Ay_position_a_guess[0,1],Ay_position_a_guess[0,2]).xyz()
        F_zhd_a = Mobj_b_base_Error.saastamoinen_model(np.array([Ay_position_a_guess_llh[0]]),
                                                     np.array([Ay_position_a_guess_llh[1]]),
                                                     np.array([Ay_position_a_guess_llh[2]]),
                                                     np.array([np.pi/2]),0)
        
        F_zhd_b = Mobj_b_base_Error.saastamoinen_model(np.array([Ay_position_b_llh[0]]),
                                                     np.array([Ay_position_b_llh[1]]),
                                                     np.array([Ay_position_b_llh[2]]),
                                                     np.array([np.pi/2]),0)
        
        '''
        Ay_nmf : b站nmf值
        並修正Ay_geographical_distance_a,b
        '''
        Ay_nmf_b = nmf.nmf(I_doy,Ay_position_b_llh[0],Ay_position_b_llh[1],Ay_position_b_llh[2],Ay_elevation)
        Ay_nmf_a = nmf.nmf(I_doy,Ay_position_a_guess_llh[0],Ay_position_a_guess_llh[1],Ay_position_a_guess_llh[2],Ay_elevation)
        
        Ay_geographical_distance_b += F_zhd_b*Ay_nmf_b
        Ay_geographical_distance_a += F_zhd_a*Ay_nmf_a
        
        Ay_L1_chose_a_minus_ra = Ay_L1_chose_a - Ay_geographical_distance_a
        Ay_C1_chose_a_minus_ra = Ay_C1_chose_a - Ay_geographical_distance_a
        
        Ay_L1_chose_b_minus_rb = Ay_L1_chose_b - Ay_geographical_distance_b
        Ay_C1_chose_b_minus_rb = Ay_C1_chose_b - Ay_geographical_distance_b
        
        Ay_L1_chose_SD_minus_rSD = Ay_L1_chose_a_minus_ra - Ay_L1_chose_b_minus_rb
        Ay_C1_chose_SD_minus_rSD = Ay_C1_chose_a_minus_ra - Ay_C1_chose_b_minus_rb
        
        Ay_L1_chose_DD_minus_rDD = np.delete(Ay_L1_chose_SD_minus_rSD[I_ele_max] - Ay_L1_chose_SD_minus_rSD,I_ele_max)
        Ay_C1_chose_DD_minus_rDD = np.delete(Ay_C1_chose_SD_minus_rSD[I_ele_max] - Ay_C1_chose_SD_minus_rSD,I_ele_max)
        
        Ay_L1_chose_SD = Ay_L1_chose_a - Ay_L1_chose_b
        Ay_C1_chose_SD = Ay_C1_chose_a - Ay_C1_chose_b
        
        Ay_obs_ambiguity = Ay_N_SD_all[I_time_chose-1][Ay_sate_chose_all]
        Ay_obs_ambiguity[np.where(Ay_obs_ambiguity==0)] = ((Ay_L1_chose_SD - Ay_C1_chose_SD)/F_L1_eave_length)[np.where(Ay_obs_ambiguity==0)]
        Ay_obs_ambiguity[np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))] = ((Ay_L1_chose_SD - Ay_C1_chose_SD)/F_L1_eave_length)[np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))]
        
        Ay_obs_ambiguity_DD = np.delete(Ay_obs_ambiguity[I_ele_max] - Ay_obs_ambiguity,I_ele_max)
        
        Ay_L1_chose_DD_minus_rDD -= Ay_obs_ambiguity_DD*F_L1_eave_length
        
        '''
        Ay_LOS_b_x,y,z     : 測站與衛星的單位方向向量
        '''
        Ay_LOS_distance_b = ((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5
        Ay_LOS_b_x = ((Ay_xk_b-Ay_position_b[0,0])/Ay_LOS_distance_b)
        Ay_LOS_b_y = ((Ay_yk_b-Ay_position_b[0,1])/Ay_LOS_distance_b)
        Ay_LOS_b_z = ((Ay_zk_b-Ay_position_b[0,2])/Ay_LOS_distance_b)
        
        '''
        KALMAN
        '''
        
        '''
        Mt_X : 狀態矩陣 [x ,y ,z ,SD-N]  [3+N,1]
           SD_N :  若該衛星沒有過資料 則使用 (L1_SD_ab - Ay_SD_C1_ab)/F_L1_eave_length
                   若該衛星為持續觀測 則使用前一時刻 KALMAN濾波器之結果
           x ,y ,z 沿用SPP結果
           
        Mt_P : 狀態協方差矩陣 [3+N,3+N]
           Mt_P[:3,:3] : 固定 eye(3)*900
           Mt_P[3:,3:] : P一直沿用 若之前無資料 則為900
        #'''
        if I_time_chose == 0:
            Ay_X_make = np.zeros(3+len(Ay_L1_chose_SD))
            Ay_X_make[:3] = Ay_position_a_guess[0]
            Ay_X_make[3:] = Ay_obs_ambiguity
            Mt_X = np.matrix(Ay_X_make).T
            Mt_P = np.matrix(np.eye(3+len(Ay_L1_chose_SD)))*900.   # 狀態協方差矩陣       
            
        else:
            Ay_X_make = np.zeros(3+len(Ay_L1_chose_SD))
            Ay_X_make[:3] = Ay_position_a_guess[0]
            Ay_X_make[3:] = Ay_N_SD_all[I_time_chose-1,Ay_sate_chose_all]
            Ay_X_make[3:][np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))] = 0
            Ay_X_make[3:][np.where(Ay_X_make[3:]==0)] = Ay_obs_ambiguity[np.where(Ay_X_make[3:]==0)]
    #        if len(np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))[0]) != 0:
    #            print('slip!! {}'.format(Ay_sate_chose_all[np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))]))
            Mt_X = np.matrix(Ay_X_make).T
    
            Mt_P = np.matrix(np.zeros((3+len(Ay_L1_chose_SD),3+len(Ay_L1_chose_SD))))
            Mt_P[:3,:3] = np.eye(3)*900.
            Ay_P_all[3:,3:][Ay_sate_chose_all[np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))],:] = 0
            Ay_P_all[3:,3:][:,Ay_sate_chose_all[np.where((Ay_slip_chose_a==1)|(Ay_slip_chose_b==1))]] = 0
            for i in range(len(Ay_sate_chose_all)):
                for j in range(len(Ay_sate_chose_all)):
                    Mt_P[3+i,3+j] = Ay_P_all[3+Ay_sate_chose_all[i],3+Ay_sate_chose_all[j]]
                    if i==j and Mt_P[3+i,3+j] == 0:
                        Mt_P[3+i,3+j] = 900.
    
                    
        '''
        模型設定
        Mt_X_(t) = Mt_F*Mt_X(t-1)
        Mt_F : [3+N ,3+N ]   這邊沒啥幹用
        Mt_Q : [3+N ,3+N ]   這邊沒啥幹用
        '''
        Mt_F = np.matrix(np.eye(3+len(Ay_L1_chose_SD)))
    #    
    #    Mt_Q_make = np.zeros((3+len(Ay_SD_L1_ab),3+len(Ay_SD_L1_ab)))
    #    Mt_Q_make[:3,:3] = 9999999
    #    Mt_Q_make[3:,3:] = 0.
    ##    Mt_Q_make[len(Ay_SD_L1_ab):,len(Ay_SD_L1_ab):] = np.eye(len(Ay_SD_L1_ab))
    #    Mt_Q = np.matrix(Mt_Q_make)
    
        '''
        觀測相關
        Mt_Z = Mt_H*Mt_X
        Mt_H : [2(N-1) ,3+N ]
        Ay_D : [N-1,N]
        '''
        Ay_D = np.zeros((len(Ay_L1_chose_SD)-1,len(Ay_L1_chose_SD)))
        Ay_D[:,I_ele_max] = 1
        Ay_D[:I_ele_max,:I_ele_max] = np.eye(len(Ay_D[0,:I_ele_max]))*-1
        Ay_D[I_ele_max:,I_ele_max+1:] = np.eye(len(Ay_D[0,I_ele_max+1:]))*-1
        Ay_H_make = np.zeros((2*len(Ay_L1_chose_SD)-2,3+len(Ay_L1_chose_SD)))
        
        Ay_H_make[:len(Ay_L1_chose_SD)-1,0] = np.delete((-Ay_LOS_b_x[I_ele_max]+Ay_LOS_b_x),I_ele_max)
        Ay_H_make[len(Ay_L1_chose_SD)-1:,0] = np.delete((-Ay_LOS_b_x[I_ele_max]+Ay_LOS_b_x),I_ele_max)
        Ay_H_make[:len(Ay_L1_chose_SD)-1,1] = np.delete((-Ay_LOS_b_y[I_ele_max]+Ay_LOS_b_y),I_ele_max)
        Ay_H_make[len(Ay_L1_chose_SD)-1:,1] = np.delete((-Ay_LOS_b_y[I_ele_max]+Ay_LOS_b_y),I_ele_max)
        Ay_H_make[:len(Ay_L1_chose_SD)-1,2] = np.delete((-Ay_LOS_b_z[I_ele_max]+Ay_LOS_b_z),I_ele_max)
        Ay_H_make[len(Ay_L1_chose_SD)-1:,2] = np.delete((-Ay_LOS_b_z[I_ele_max]+Ay_LOS_b_z),I_ele_max)
        Ay_H_make[:len(Ay_L1_chose_SD)-1,3:] = Ay_D*F_L1_eave_length
        
    
        Mt_H = np.matrix(Ay_H_make)  # 觀測矩陣
    
        '''
        Mt_R : 
        '''
        Ay_R = np.zeros((2*len(Ay_L1_chose_SD)-2,2*len(Ay_L1_chose_SD)-2))
        
        Ay_R[:len(Ay_L1_chose_SD)-1,:len(Ay_L1_chose_SD)-1] = ((0.003**2+(0.003**2)/(np.sin(Ay_elevation)**2))*2)[I_ele_max]
        Ay_R[range(len(Ay_L1_chose_SD)-1),range(len(Ay_L1_chose_SD)-1)] += np.delete(((0.003**2+(0.003**2)/(np.sin(Ay_elevation)**2))*2),I_ele_max)
        Ay_R[len(Ay_L1_chose_SD)-1:,len(Ay_L1_chose_SD)-1:] = ((0.3**2+(0.3**2)/(np.sin(Ay_elevation)**2))*2)[I_ele_max]
        Ay_R[range(len(Ay_L1_chose_SD)-1,2*len(Ay_L1_chose_SD)-2),range(len(Ay_L1_chose_SD)-1,2*len(Ay_L1_chose_SD)-2)] += np.delete(((0.3**2+(0.3**2)/(np.sin(Ay_elevation)**2))*2),I_ele_max)
        Mt_R = np.matrix(Ay_R)
    
        Mt_X_ = Mt_F*Mt_X
        Mt_P_ = np.copy(Mt_P)
        test = Mt_H*Mt_P_*(Mt_H.T) + Mt_R
        Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv(Mt_H*Mt_P_*(Mt_H.T) + Mt_R)
    
        Ay_V = np.zeros((2*len(Ay_L1_chose_SD)-2,1))
        Ay_V[:len(Ay_L1_chose_SD)-1,0] = Ay_L1_chose_DD_minus_rDD
        Ay_V[len(Ay_L1_chose_SD)-1:,0] = Ay_C1_chose_DD_minus_rDD
        Mt_X  = Mt_X_ + Mt_K*(np.matrix(Ay_V))
        Mt_P  = (np.eye(3+len(Ay_L1_chose_SD)) - Mt_K*Mt_H)*Mt_P_
        
        Ay_N_SD_all[I_time_chose,Ay_sate_chose_all] = np.array(Mt_X)[3:,0]
        
        Ay_P_all[:3,:3] = Mt_P[:3,:3]
        
        for i in range(len(Ay_sate_chose_all)):
            for j in range(len(Ay_sate_chose_all)):
                Ay_P_all[3+Ay_sate_chose_all[i],3+Ay_sate_chose_all[j]] = Mt_P[3+i,3+j]
                
        Ay_X_all[I_time_chose] = np.array(Mt_X)[0:3,0]
    #    test_all.append( np.sum((np.array([-3056585.4078,4965782.4534,2575811.0739])-np.array(Mt_X)[0:3,0])**2)**0.5 )
    #    Ay_ENU_all[I_time_chose] = xyz2enu.xyz2enu(np.array([np.array(Mt_X)[0:3,0]]),np.array([[-3056585.4078,4965782.4534,2575811.0739]])).return_enu()[0]
        test_all.append( np.sum((np.array([-3056585.4078,4965782.4534,2575811.0739])-np.array(Mt_X)[0:3,0])**2)**0.5 )
        Ay_ENU_all[I_time_chose] = xyz2enu.xyz2enu(np.array([np.array(Mt_X)[0:3,0]]),Ay_position_a).return_enu()[0]
    except:
        Ay_ENU_all[I_time_chose] = np.nan