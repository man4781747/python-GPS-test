# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:10:54 2018

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

F_phi_obs_error = 0.0019
F_pr_obs_error = 3

I_doy = 76
I_dt = 30.
'''
測試檔案位置
'''
S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseC1.npy'
S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseL1.npy'

S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseC1.npy'
S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseL1.npy'

S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phasetime.npy'

S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phasetime.npy'

S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15076.npy'

S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'

S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\pepu15076_position.npy'
#
#S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phaseC1.npy'
#S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phaseL1.npy'
#S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phaseC1.npy'
#S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phaseL1.npy'
#S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\pepu15073phasetime.npy'
#S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\phase_data\30s\hual15073phasetime.npy'
#S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15073.npy'
#S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\position_data\pepu15073_position.npy'
#S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015073\position_data\hual15073_position.npy'

'''
讀取檔案
L1 資料在o檔內單位為 '相位' 因此必須乘上波長使之變成長度單位
單位: m
'''
Ay_C1_a = np.load(S_C1_data_path_a)[:,:32]
Ay_L1_a = np.load(S_L1_data_path_a)[:,:32]*F_L1_eave_length
Ay_C1_b = np.load(S_C1_data_path_b)[:,:32]
Ay_L1_b = np.load(S_L1_data_path_b)[:,:32]*F_L1_eave_length
Ay_time_a = np.load(S_a_time_path)
Ay_time_b = np.load(S_b_time_path)
Ay_n_data = np.load(S_n_data_path)
Ay_position_a = np.load(S_a_position_path)[0:1,:]
#Ay_position_b = np.load(S_b_position_path)[0:1,:]
Ay_position_b = np.array([[-3055302.1000,4964313.4140,2580107.1000]])
Ay_position_b_llh = xyz2llh(Ay_position_b[0,0],Ay_position_b[0,1],Ay_position_b[0,2]).xyz()

Ay_position_a_guess_all = np.load(r'D:\github\python_code\GPS_position\test.npy')
Ay_position_a_guess_all[314] = np.array([ -3056583.9930276028,4965781.9920758503,2575815.6475489931])
#Ay_position_a_guess = np.array([[-3056583.63227,4965781.90302,2575812.44704]])
#Ay_position_a_guess_all = np.array([[-3056583.63227,4965781.90302,2575812.44704],
#                                [-3056584.12512,4965781.74061,2575811.87467]])
#

#Ay_position_a_guess_all = np.array([[-3056000.63227,4965000.90302,2575000.44704],
#                                [-3056584.12512,4965781.74061,2575811.87467]])


#Ay_C1_a[np.where(Ay_C1_a==0)] = np.nan
#Ay_L1_a[np.where(Ay_L1_a==0)] = np.nan
#Ay_C1_b[np.where(Ay_C1_b==0)] = np.nan
#Ay_L1_b[np.where(Ay_L1_b==0)] = np.nan

Ay_check_array = np.where((Ay_C1_a==0.)|(Ay_L1_a==0.)|(Ay_C1_b==0.)|(Ay_L1_a==0.))
Ay_C1_a[Ay_check_array] = 0.
Ay_L1_a[Ay_check_array] = 0.
Ay_C1_b[Ay_check_array] = 0.
Ay_L1_b[Ay_check_array] = 0.
'''
F_BL : 兩站間距離   單位: m
Ay_time_a, Ay_time_b : 兩站所記錄的時間     單位: s
F_gpsweektime : GPS紀錄的時間(秒)在當周的星期日開始算起 單位: s
'''
F_BL = np.sum( (Ay_position_a-Ay_position_b)**2 )**0.5

Ay_time_a = Ay_time_a[:,3]*3600+Ay_time_a[:,4]*60+Ay_time_a[:,5]
Ay_time_b = Ay_time_b[:,3]*3600+Ay_time_b[:,4]*60+Ay_time_b[:,5]

Ay_SD_L1_all = np.zeros((2880,32))
Ay_SD_C1_all = np.zeros((2880,32))

Ay_BL_all = np.zeros((2880,3))
Ay_N_SD_all = np.zeros((2880,32))


'''
狀態協方差矩陣(KALMAN) 總矩陣 [3+32,3+32]
[[BL的3軸方向(3*3) ,            0]
 [             0 ,32顆衛星(32*32)]]
'''
Ay_P_all = np.zeros((3+32,3+32))

F_gpsweektime = (float(DOY2GPSweek(15,76))%10)*24*60*60

Ay_X_all = np.zeros((2880,3))
test_all = []
#%%
#for I_time_chose in range(len(Ay_time_a)):
#for I_time_chose in range(2880):
for I_time_chose in range(1):
    Ay_position_a_guess = Ay_position_a_guess_all[I_time_chose:I_time_chose+1,:]
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
    
    '''
    Ay_SD_L1,C1_ab : L1,C1 訊號兩站做SD
    '''
    Ay_SD_L1_ab = Ay_L1_chose_a - Ay_L1_chose_b
    Ay_SD_C1_ab = Ay_C1_chose_a - Ay_C1_chose_b
    
    '''
    記錄用
    '''
    Ay_SD_L1_all[I_time_chose] = Ay_SD_L1_ab
    Ay_SD_C1_all[I_time_chose] = Ay_SD_C1_ab
    
#    Ay_SD_L1_ab = Ay_SD_L1_ab[~np.isnan(Ay_SD_L1_ab)]
#    Ay_SD_C1_ab = Ay_SD_C1_ab[~np.isnan(Ay_SD_C1_ab)]
    '''
    去除沒有資料檔案
    (正序)
    '''
    Ay_SD_L1_ab = Ay_SD_L1_ab[np.where(Ay_SD_L1_ab!=0)]
    Ay_SD_C1_ab = Ay_SD_C1_ab[np.where(Ay_SD_C1_ab!=0)]
    
#    print(Ay_DD_L1_ab)
    '''
    計算 a,b 兩站的接收機時間(整數,小數 分開計算)
    '''
    F_a_timechose_int = int(Ay_time_a[I_time_chose])
    F_a_timechose_float = Ay_time_a[I_time_chose]%1
    F_a_timechose_total = Ay_time_a[I_time_chose]
    
    F_b_timechose_int = int(Ay_time_b[I_time_chose])
    F_b_timechose_float = Ay_time_b[I_time_chose]%1
    F_b_timechose_total = Ay_time_b[I_time_chose]
    
    '''
    Ay_sate_n_data_a,b : 依有資料的衛星來選取 n data
    Ay_sate_chose_a    : 選取的衛星編號
    Ay_C1_a,b_chose    : 相對應衛星的C1資料
    '''
    Ay_sate_n_data_a = Get_n_data_each_time(I_time_chose,Ay_C1_a,Ay_n_data,F_a_timechose_total)[::-1]
    Ay_sate_chose_a = Ay_sate_n_data_a[:,0].astype('int')-1
    Ay_sate_n_data_b = Get_n_data_each_time(I_time_chose,Ay_C1_b,Ay_n_data,F_b_timechose_total)[::-1]
    Ay_sate_chose_b = Ay_sate_n_data_b[:,0].astype('int')-1
    
    Lst_all_sate = [i for i in range(32)]
    for I_pop in range(len(Ay_sate_chose_b)):
        Lst_all_sate.pop(Ay_sate_chose_b[I_pop]-I_pop)

    Ay_no_data_sate = np.array(Lst_all_sate)
    Ay_P_all[3+Ay_no_data_sate] = 0
    Ay_P_all[:,3+Ay_no_data_sate] = 0
    
    test = Ay_P_all[Ay_sate_chose_a+3]
    test_ = Ay_P_all[Ay_sate_chose_a+3]
    
    Ay_C1_a_chose = Ay_C1_a[I_time_chose,Ay_sate_chose_a]
    Ay_C1_b_chose = Ay_C1_b[I_time_chose,Ay_sate_chose_b]
    
    '''
    Mobj_sate_cal_a,b       : 計算 測站 衛星相關資料 (Mobj)
    Ay_delta_t_sv_a,b       : 衛星時終誤差 (s)   (一開始粗略估計,而後求出精準)
    Ay_xk,Ay_yk,Ay_zk       : 測站所有衛星位置(m) (ECEF)
    '''
    Mobj_sate_cal_a = Satellite_Calculate(Ay_sate_n_data_a)
    Ay_delta_t_sv_a = Mobj_sate_cal_a.get_sate_clock_error(Ay_C1_a_chose,F_a_timechose_int,F_a_timechose_float,F_gpsweektime)
    (Ay_xk_a,Ay_yk_a,Ay_zk_a,Ay_delta_t_sv_a) = Mobj_sate_cal_a.get_sate_position(
                                            F_a_timechose_int,F_a_timechose_float,
                                            F_gpsweektime,Ay_delta_t_sv_a,Ay_C1_a_chose)    
    Ay_sate_position_a = np.array([Ay_xk_a,Ay_yk_a,Ay_zk_a]).T        #OK
    
    Mobj_sate_cal_b = Satellite_Calculate(Ay_sate_n_data_b)
    Ay_delta_t_sv_b = Mobj_sate_cal_b.get_sate_clock_error(Ay_C1_b_chose,F_b_timechose_int,F_b_timechose_float,F_gpsweektime)
    (Ay_xk_b,Ay_yk_b,Ay_zk_b,Ay_delta_t_sv_b) = Mobj_sate_cal_b.get_sate_position(
                                            F_b_timechose_int,F_b_timechose_float,
                                            F_gpsweektime,Ay_delta_t_sv_b,Ay_C1_b_chose)  
    Ay_sate_position_b = np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T           #OK
    
    '''
    計算測站與衛星間地理距離
    Ay_geographical_distance_b  : b基站與衛星的地理距離(修正自轉及衛星時鐘誤差)
    Ay_geographical_distance_a  : a測站與衛星的地理距離(猜測)(修正自轉及衛星時鐘誤差)
    
    '''
    
    Ay_geographical_distance_b =((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5\
                                + F_OMGE*(Ay_xk_b*Ay_position_b[0,1]-Ay_yk_b*Ay_position_b[0,0])/F_C - Ay_delta_t_sv_b*F_C   
    Ay_geographical_distance_a =((Ay_xk_a-Ay_position_a_guess[0,0])**2+(Ay_yk_a-Ay_position_a_guess[0,1])**2+(Ay_zk_a-Ay_position_a_guess[0,2])**2)**0.5\
                                + F_OMGE*(Ay_xk_a*Ay_position_a_guess[0,1]-Ay_yk_a*Ay_position_a_guess[0,0])/F_C - Ay_delta_t_sv_a*F_C
    
    test_g_a = np.copy(Ay_geographical_distance_a)
    test_g_b = np.copy(Ay_geographical_distance_b)
    # 整數位OK
    
#    F_OMGE*(Ay_xk_b*Ay_position_b[0,1]-Ay_yk_b*Ay_position_b[0,0])/F_C
    '''
    計算估計所得的 ambiguity
    若該衛星沒有過資料 則使用 (L1_SD_ab - Ay_SD_C1_ab)/F_L1_eave_length
    可得觀測的 ambiguity (含電離層,量測誤差造成之誤差)
    若該衛星為持續觀測 則使用前一時刻 KALMAN濾波器之結果
    '''
    if I_time_chose == 0:
        Ay_obs_ambiguity = (Ay_SD_L1_ab - Ay_SD_C1_ab)/F_L1_eave_length    #OK
    else :
        Ay_obs_ambiguity = Ay_N_SD_all[I_time_chose-1,Ay_sate_chose_a]
        Ay_test_ambiguity = ((Ay_SD_L1_ab - Ay_SD_C1_ab)/F_L1_eave_length)
        Ay_obs_ambiguity[np.where(Ay_obs_ambiguity==0)] = Ay_test_ambiguity[np.where(Ay_obs_ambiguity==0)]
        
        Ay_search = np.where(abs(Ay_obs_ambiguity-Ay_test_ambiguity)>55)[0]
        
        if len(Ay_search) != 0:
            print('{0} sat={1} cycle-slip??'.format(I_time_chose,Ay_sate_chose_b[Ay_search]+1))
            Ay_obs_ambiguity[Ay_search] = Ay_test_ambiguity[Ay_search]
            Ay_P_all[3+Ay_sate_chose_b[Ay_search]] = 0
            Ay_P_all[:,3+Ay_sate_chose_b[Ay_search]] = 0

    '''
    計算各衛星對a,b 兩站的仰角
    Ay_elevation : b站對所有衛星仰角(弧度)
    I_ele_max_sate : 仰角最大衛星
    
    Ay_position_a_guess_llh : 計算目前猜測點LLH
    F_zhd_a,b = a,b 兩站在仰角90度,濕度0 的情況下的大氣誤差
    '''
    
    Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T,Ay_position_b).return_enu()
    Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
    I_ele_max_sate = np.where(Ay_elevation==np.max(Ay_elevation))[0][0]
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
    
    '''
    
    Ay_L1,C1_chose_a,b_y : a,b 兩站 L1,C1 訊號 分別減去 a_guess,b 的地理距離(修正過)
    

    Ay_kalman_L1_y : 對仰角對大的衛星做SD 並減去觀測ambiguity
    Ay_kalman_C1_y : 對仰角對大的衛星做SD
    '''
    Ay_L1_chose_a_y = Ay_L1_chose_a[np.where(Ay_L1_chose_a!=0)] - Ay_geographical_distance_a
    Ay_C1_chose_a_y = Ay_C1_chose_a[np.where(Ay_C1_chose_a!=0)] - Ay_geographical_distance_a

    Ay_L1_chose_b_y = Ay_L1_chose_b[np.where(Ay_L1_chose_b!=0)] - Ay_geographical_distance_b
    Ay_C1_chose_b_y = Ay_C1_chose_b[np.where(Ay_C1_chose_b!=0)] - Ay_geographical_distance_b

    Ay_kalman_L1_y = np.delete(((Ay_L1_chose_a_y[I_ele_max_sate] - Ay_L1_chose_b_y[I_ele_max_sate])-(Ay_L1_chose_a_y - Ay_L1_chose_b_y)),I_ele_max_sate)
    test_Ay_kalman_L1_y = np.copy(Ay_kalman_L1_y)
    test_Ay_obs_ambiguity = np.copy(Ay_obs_ambiguity)
    Ay_kalman_L1_y -= np.delete(Ay_obs_ambiguity[I_ele_max_sate] - Ay_obs_ambiguity,I_ele_max_sate)*F_L1_eave_length
    Ay_kalman_C1_y = np.delete(((Ay_C1_chose_a_y[I_ele_max_sate] - Ay_C1_chose_b_y[I_ele_max_sate])-(Ay_C1_chose_a_y - Ay_C1_chose_b_y)),I_ele_max_sate)
    
    '''
    不同衛星SD資料做DD,以衛星仰角最大的為主
    '''
    Ay_DD_L1_ab = np.delete((Ay_SD_L1_ab-Ay_SD_L1_ab[I_ele_max_sate]),I_ele_max_sate)
    Ay_DD_C1_ab = np.delete((Ay_SD_C1_ab-Ay_SD_C1_ab[I_ele_max_sate]),I_ele_max_sate)
    
    '''
    Ay_LOS_b_x,y,z     : 測站與衛星的單位方向向量
    '''
    Ay_LOS_distance_b = ((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5
    Ay_LOS_b_x = ((Ay_xk_b-Ay_position_b[0,0])/Ay_LOS_distance_b)
    Ay_LOS_b_y = ((Ay_yk_b-Ay_position_b[0,1])/Ay_LOS_distance_b)
    Ay_LOS_b_z = ((Ay_zk_b-Ay_position_b[0,2])/Ay_LOS_distance_b)

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
#        Mt_X = np.matrix(np.zeros(len(Ay_SD_L1_ab)*3)).T   # 初始狀態 (SD-r ,SD-I ,SD-N)    
        Ay_X_make = np.zeros(3+len(Ay_SD_L1_ab))
        Ay_X_make[:3] = Ay_position_a_guess[0]
        Ay_X_make[3:] = Ay_obs_ambiguity
        Mt_X = np.matrix(Ay_X_make).T
        test_XX = Ay_X_make
#        Mt_X = np.matrix(np.zeros(3+len(Ay_SD_L1_ab))).T   # 初始狀態 (BL_x ,BL_y ,BL_z ,SD-N)
     
        Mt_P = np.matrix(np.eye(3+len(Ay_SD_L1_ab)))*900.   # 狀態協方差矩陣       
    else:
        Ay_X_make = np.zeros(3+len(Ay_SD_L1_ab))
        Ay_X_make[:3] = Ay_position_a_guess[0]
        Ay_X_make[3:] = Ay_N_SD_all[I_time_chose-1,Ay_sate_chose_a]
        Ay_X_make[3:][np.where(Ay_X_make[3:]==0)] = ((Ay_SD_L1_ab - Ay_SD_C1_ab)/F_L1_eave_length)[np.where(Ay_X_make[3:]==0)]
#        Ay_X_make[3:] = (Ay_SD_L1_ab - Ay_SD_C1_ab)/F_L1_eave_length
        Mt_X = np.matrix(Ay_X_make).T
        test_X = Mt_X
        Mt_P = np.matrix(np.zeros((3+len(Ay_SD_L1_ab),3+len(Ay_SD_L1_ab))))
        Mt_P[:3,:3] = np.eye(3)*900.
        for i in range(len(Ay_sate_chose_b)):
            for j in range(len(Ay_sate_chose_b)):
                Mt_P[3+i,3+j] = Ay_P_all[3+Ay_sate_chose_b[i],3+Ay_sate_chose_b[j]]
                if i==j and Mt_P[3+i,3+j] == 0:
                    Mt_P[3+i,3+j] = 900.
#        print(Mt_P[7,7])           
        testt = np.copy(Mt_P)       
                
    '''
    模型設定
    Mt_X_(t) = Mt_F*Mt_X(t-1)
    Mt_F : [3+N ,3+N ]   這邊沒啥幹用
    Mt_Q : [3+N ,3+N ]   這邊沒啥幹用
    '''
    Mt_F = np.matrix(np.eye(3+len(Ay_SD_L1_ab)))
    
    Mt_Q_make = np.zeros((3+len(Ay_SD_L1_ab),3+len(Ay_SD_L1_ab)))
    Mt_Q_make[:3,:3] = 9999999
    Mt_Q_make[3:,3:] = 0.
#    Mt_Q_make[len(Ay_SD_L1_ab):,len(Ay_SD_L1_ab):] = np.eye(len(Ay_SD_L1_ab))
    Mt_Q = np.matrix(Mt_Q_make)

    '''
    觀測相關
    Mt_Z = Mt_H*Mt_X
    Mt_H : [2(N-1) ,3+N ]
    Ay_D : [N-1,N]
    '''
    Ay_D = np.zeros((len(Ay_DD_L1_ab),len(Ay_SD_L1_ab)))
    Ay_D[:,I_ele_max_sate] = 1
    Ay_D[:I_ele_max_sate,:I_ele_max_sate] = np.eye(len(Ay_D[0,:I_ele_max_sate]))*-1
    Ay_D[I_ele_max_sate:,I_ele_max_sate+1:] = np.eye(len(Ay_D[0,I_ele_max_sate+1:]))*-1
#    Mt_D = np.matrix(Ay_D)
    Ay_H_make = np.zeros((2*len(Ay_DD_L1_ab),3+len(Ay_SD_L1_ab)))
    
#    np.delete((Ay_SD_L1_ab-Ay_SD_L1_ab[I_ele_max_sate]),I_ele_max_sate)
#    np.delete((-Ay_LOS_b_x[I_ele_max_sate]+Ay_LOS_b_x),I_ele_max_sate)
    
    Ay_H_make[:len(Ay_DD_L1_ab),0] = np.delete((-Ay_LOS_b_x[I_ele_max_sate]+Ay_LOS_b_x),I_ele_max_sate)
    Ay_H_make[len(Ay_DD_L1_ab):,0] = np.delete((-Ay_LOS_b_x[I_ele_max_sate]+Ay_LOS_b_x),I_ele_max_sate)
    Ay_H_make[:len(Ay_DD_L1_ab),1] = np.delete((-Ay_LOS_b_y[I_ele_max_sate]+Ay_LOS_b_y),I_ele_max_sate)
    Ay_H_make[len(Ay_DD_L1_ab):,1] = np.delete((-Ay_LOS_b_y[I_ele_max_sate]+Ay_LOS_b_y),I_ele_max_sate)
    Ay_H_make[:len(Ay_DD_L1_ab),2] = np.delete((-Ay_LOS_b_z[I_ele_max_sate]+Ay_LOS_b_z),I_ele_max_sate)
    Ay_H_make[len(Ay_DD_L1_ab):,2] = np.delete((-Ay_LOS_b_z[I_ele_max_sate]+Ay_LOS_b_z),I_ele_max_sate)
    Ay_H_make[:len(Ay_DD_L1_ab),3:] = Ay_D*F_L1_eave_length
    
    
#    Ay_H_make = np.zeros((2*len(Ay_DD_L1_ab),3*len(Ay_SD_L1_ab)))
#    Ay_H_make[:len(Ay_DD_L1_ab),:len(Ay_SD_L1_ab)] = Ay_D
#    Ay_H_make[len(Ay_DD_L1_ab):,:len(Ay_SD_L1_ab)] = Ay_D
#    Ay_H_make[:len(Ay_DD_L1_ab),len(Ay_SD_L1_ab):len(Ay_SD_L1_ab)*2] = -Ay_D
#    Ay_H_make[len(Ay_DD_L1_ab):,len(Ay_SD_L1_ab):len(Ay_SD_L1_ab)*2] = Ay_D
#    Ay_H_make[:len(Ay_DD_L1_ab),len(Ay_SD_L1_ab)*2:len(Ay_SD_L1_ab)*3] = Ay_D*F_L1_eave_length

    Mt_H = np.matrix(Ay_H_make)  # 觀測矩陣
    
#    Mt_R = np.matrix(np.zeros((2*len(Ay_DD_L1_ab),2*len(Ay_DD_L1_ab))))
#    Mt_phi_obs_error = np.matrix(np.eye(len(Ay_SD_L1_ab))*2*F_phi_obs_error**2)
#    Mt_pr_obs_error  = np.matrix(np.eye(len(Ay_SD_C1_ab))*2*F_pr_obs_error**2) 
#    Mt_R[:len(Ay_DD_L1_ab),:len(Ay_DD_L1_ab)] = np.matrix(Ay_D)*Mt_phi_obs_error*(np.matrix(Ay_D).T)
#    Mt_R[len(Ay_DD_L1_ab):,len(Ay_DD_L1_ab):] = np.matrix(Ay_D)*Mt_pr_obs_error*(np.matrix(Ay_D).T)
#    
    '''
    Mt_R : 
    '''
    Ay_R = np.zeros((2*len(Ay_DD_L1_ab),2*len(Ay_DD_L1_ab)))
    
    Ay_R[:len(Ay_DD_L1_ab),:len(Ay_DD_L1_ab)] = ((0.003**2+(0.003**2)/(np.sin(Ay_elevation)**2))*2)[I_ele_max_sate]
    Ay_R[range(len(Ay_DD_L1_ab)),range(len(Ay_DD_L1_ab))] += np.delete(((0.003**2+(0.003**2)/(np.sin(Ay_elevation)**2))*2),I_ele_max_sate)
    Ay_R[len(Ay_DD_L1_ab):,len(Ay_DD_L1_ab):] = ((0.3**2+(0.3**2)/(np.sin(Ay_elevation)**2))*2)[I_ele_max_sate]
    Ay_R[range(len(Ay_DD_L1_ab),2*len(Ay_DD_L1_ab)),range(len(Ay_DD_L1_ab),2*len(Ay_DD_L1_ab))] += np.delete(((0.3**2+(0.3**2)/(np.sin(Ay_elevation)**2))*2),I_ele_max_sate)
    Mt_R = np.matrix(Ay_R)

    Mt_X_ = Mt_F*Mt_X
#    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_P_ = np.copy(Mt_P)
    test = Mt_H*Mt_P_*(Mt_H.T) + Mt_R
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv(Mt_H*Mt_P_*(Mt_H.T) + Mt_R)
#    Mt_Z  = np.matrix( np.concatenate((Ay_DD_L1_ab,Ay_DD_C1_ab))).T
#    Mt_Z  = np.matrix( np.concatenate((Ay_obs_L_p_SD,Ay_obs_phi_p_SD))).T
#    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
#Ay_kalman_y
    Ay_V = np.zeros((2*len(Ay_DD_L1_ab),1))
    Ay_V[:len(Ay_DD_L1_ab),0] = Ay_kalman_L1_y
    Ay_V[len(Ay_DD_L1_ab):,0] = Ay_kalman_C1_y
    Mt_X  = Mt_X_ + Mt_K*(np.matrix(Ay_V))
    Mt_P  = (np.eye(3+len(Ay_SD_L1_ab)) - Mt_K*Mt_H)*Mt_P_
    
    Ay_N_SD_all[I_time_chose,Ay_sate_chose_b] = np.array(Mt_X)[3:,0]
    Ay_BL_all[I_time_chose] = np.array(Mt_X)[:3,0]
    
    Ay_P_all[:3,:3] = Mt_P[:3,:3]
    
    for i in range(len(Ay_sate_chose_b)):
        for j in range(len(Ay_sate_chose_b)):
            Ay_P_all[3+Ay_sate_chose_b[i],3+Ay_sate_chose_b[j]] = Mt_P[3+i,3+j]
            
    
    Ay_X_all[I_time_chose] = np.array(Mt_X)[0:3,0]
    test_all.append( np.sum((np.array([-3056585.4078,4965782.4534,2575811.0739])-np.array(Mt_X)[0:3,0])**2)**0.5 )
#    test_all.append( np.sum((Ay_position_a[0]-np.array(Mt_X)[0:3,0])**2)**0.5 )
#    print(Ay_position_a[0]-Ay_X_make[0:3])