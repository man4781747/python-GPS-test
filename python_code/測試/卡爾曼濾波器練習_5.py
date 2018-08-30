# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:02:25 2018

@author: owo
卡爾曼濾波器測試練習 - 4

single difference measurement model

""" 
import numpy as np 
import matplotlib.pyplot as plt
from DOY2GPSweek import DOY2GPSweek
from GNSS_positioning_argv_ver2 import *
import xyz2enu
import LDL_decomposition as LDL
import LAMBDA

#F_sig_b_dot = 0.01
#F_sig_b = 0.001
F_sig_b_dot = 1
F_sig_b = 1
F_Re = 6371000.       # earth radius (m)
F_ion_h = 350000.      # ionsphere hight (m)

#F_alpha_iono = 1/30
#F_sig_viono = 1/18000.
F_sig_viono = 1/1000000.
F_sig_amb = 1000

F_alpha_iono = 1/30.   #(1/30 ~ 1/300)
#F_sig_viono = 1/100.
#F_sig_amb = 0.001

F_L1_eave_length = (299792458.0/1.57542e9) #(m)

I_dt = 30.
'''
測試檔案位置
'''
S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseC1.npy'
S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseL1.npy'
S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseC1.npy'
S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseL1.npy'
S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phasetime.npy'
S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phasetime.npy'
S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15076.npy'
S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\pepu15076_position.npy'
S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'
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
Ay_L1_a = np.load(S_L1_data_path_a)[:,:32]*(299792458.0/1.57542e9)
Ay_C1_b = np.load(S_C1_data_path_b)[:,:32]
Ay_L1_b = np.load(S_L1_data_path_b)[:,:32]*(299792458.0/1.57542e9)
Ay_time_a = np.load(S_a_time_path)
Ay_time_b = np.load(S_b_time_path)
Ay_n_data = np.load(S_n_data_path)
Ay_position_a = np.load(S_a_position_path)[0:1,:]
Ay_position_b = np.load(S_b_position_path)[0:1,:]

'''
F_BL : 兩站間距離   單位: m
Ay_time_a, Ay_time_b : 兩站所記錄的時間     單位: s
F_gpsweektime : GPS紀錄的時間(秒)在當周的星期日開始算起 單位: s
'''
F_BL = np.sum( (Ay_position_a-Ay_position_b)**2 )**0.5

Ay_time_a = Ay_time_a[:,3]*3600+Ay_time_a[:,4]*60+Ay_time_a[:,5]
Ay_time_b = Ay_time_b[:,3]*3600+Ay_time_b[:,4]*60+Ay_time_b[:,5]

F_gpsweektime = (float(DOY2GPSweek(15,76))%10)*24*60*60

'''
將a,b兩站互相沒有資料的資料去除
'''
Ay_check_array = np.where((Ay_C1_a==0.)|(Ay_L1_a==0.)|(Ay_C1_b==0.)|(Ay_L1_a==0.))
Ay_C1_a[Ay_check_array] = 0.
Ay_L1_a[Ay_check_array] = 0.
Ay_C1_b[Ay_check_array] = 0.
Ay_L1_b[Ay_check_array] = 0.

'''
GRoup And Phase Ionospheric Correction (GRAPHIC)
單位: m
'''
Ay_L_p_a = (Ay_C1_a+Ay_L1_a)*0.5
Ay_L_p_b = (Ay_C1_b+Ay_L1_b)*0.5

'''
SD
'''
Ay_phi_p_SD = Ay_L1_a - Ay_L1_b
Ay_L_p_SD   = Ay_L_p_a - Ay_L_p_b

Ay_receiver_bias_all = np.zeros(len(Ay_L_p_SD))
Ay_receiver_drift_all = np.zeros(len(Ay_L_p_SD))
Ay_d_I_SD_all = np.zeros((len(Ay_L_p_SD),32))
Ay_N_SD_all = np.zeros((len(Ay_L_p_SD),32))
Ay_obs_phi_p_SD_all = np.zeros((len(Ay_L_p_SD),32))
Ay_obs_L_p_SD_all = np.zeros((len(Ay_L_p_SD),32))
Ay_P_all = np.zeros((2+64,2+64))
Ay_P_all_test = np.zeros((len(Ay_L_p_SD),2+64,2+64))
Ay_geo_distan_all = np.zeros((len(Ay_L_p_SD),32))

test_Lst = []
#for I_time_chose in range(len(Ay_time_a)):
for I_time_chose in range(10):   
    print(I_time_chose)
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
    Ay_sate_position_a = np.array([Ay_xk_a,Ay_yk_a,Ay_zk_a]).T
    
    Mobj_sate_cal_b = Satellite_Calculate(Ay_sate_n_data_b)
    Ay_delta_t_sv_b = Mobj_sate_cal_b.get_sate_clock_error(Ay_C1_b_chose,F_b_timechose_int,F_b_timechose_float,F_gpsweektime)
    (Ay_xk_b,Ay_yk_b,Ay_zk_b,Ay_delta_t_sv_b) = Mobj_sate_cal_b.get_sate_position(
                                            F_b_timechose_int,F_b_timechose_float,
                                            F_gpsweektime,Ay_delta_t_sv_b,Ay_C1_b_chose)  
    Ay_sate_position_b = np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T
    '''
    計算測站與衛星間地理距離
    Ay_geographical_distance_a,b  : 測站與衛星的地理距離(尚未修自轉)
    
    已知a,b兩站與衛星地理距離下,將SD的資料作修正
    Ay_obs_phi_p_SD  : 修正的 SD"phase"
    Ay_obs_L_p_SD    : 修正的 SD"GRAPHIC"
    '''
    Ay_geographical_distance_a =((Ay_xk_a-Ay_position_a[0,0])**2+(Ay_yk_a-Ay_position_a[0,1])**2+(Ay_zk_a-Ay_position_a[0,2])**2)**0.5
    Ay_geographical_distance_b =((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5
    
    Ay_obs_phi_p_SD = Ay_phi_p_SD[I_time_chose,Ay_sate_chose_a] - (Ay_geographical_distance_a-Ay_geographical_distance_b)
    Ay_obs_L_p_SD   = Ay_L_p_SD[I_time_chose,Ay_sate_chose_a] - (Ay_geographical_distance_a-Ay_geographical_distance_b)
    
    '''
    Ay_EOL_b_x,y,z     : 測站與衛星的單位方向向量
    Ay_EOL_b_x,y,z_DD  : 已知位置測站的 測站-衛星 不同衛星單位方向向量相減 (應為空中一次差)
    Ay_phi_DD          : 相位資料的DD  (未知兩站位置下)(驗證答案用)
    '''
    
    Ay_EOL_b_x = (Ay_xk_b-Ay_position_b[0,0])/Ay_geographical_distance_b
    Ay_EOL_b_y = (Ay_yk_b-Ay_position_b[0,1])/Ay_geographical_distance_b
    Ay_EOL_b_z = (Ay_zk_b-Ay_position_b[0,2])/Ay_geographical_distance_b
    
    Ay_EOL_b_x_DD = -(Ay_EOL_b_x-Ay_EOL_b_x[0])[1:]
    Ay_EOL_b_y_DD = -(Ay_EOL_b_y-Ay_EOL_b_y[0])[1:]
    Ay_EOL_b_z_DD = -(Ay_EOL_b_z-Ay_EOL_b_z[0])[1:]
    
    Ay_phi_DD = (Ay_phi_p_SD[I_time_chose,Ay_sate_chose_a]-Ay_phi_p_SD[I_time_chose,Ay_sate_chose_a][0])[1:]
    
    
    '''
    (不參與計算 純紀錄)
    計算 SD的測站-衛星地理距離 數值並記錄
    '''
    Ay_geo_distan_all[I_time_chose,Ay_sate_chose_a] = (Ay_geographical_distance_a-Ay_geographical_distance_b)
    
    '''
    計算衛星仰角
    Ay_elevation_a,b   : 測站對每顆衛星的仰角
    Ay_elevation_all   : 兩站仰角平均 (不確定這步驟對不對)
    Ay_elevation_chose : 仰角挑選位置
    '''
    Ay_enu_resever_sate_a = np.zeros((len(Ay_xk_a),3))
    for I_Ay_enu_resever_sate_num in range(len(Ay_xk_a)):
        Ay_enu_resever_sate_a[I_Ay_enu_resever_sate_num] = xyz2enu.xyz2enu(Ay_sate_position_a[I_Ay_enu_resever_sate_num:I_Ay_enu_resever_sate_num+1],
                           Ay_position_a).return_enu()
    Ay_elevation_a = np.arctan2( (Ay_enu_resever_sate_a[:,2]),np.sum(Ay_enu_resever_sate_a[:,0:2]**2,1)**0.5 )

    Ay_enu_resever_sate_b = np.zeros((len(Ay_xk_b),3))
    for I_by_enu_resever_sate_num in range(len(Ay_xk_b)):
        Ay_enu_resever_sate_b[I_by_enu_resever_sate_num] = xyz2enu.xyz2enu(Ay_sate_position_b[I_by_enu_resever_sate_num:I_by_enu_resever_sate_num+1],
                           Ay_position_b).return_enu()
    Ay_elevation_b = np.arctan2( (Ay_enu_resever_sate_b[:,2]),np.sum(Ay_enu_resever_sate_b[:,0:2]**2,1)**0.5 )
    
    Ay_elevation_all = 0.5*(Ay_elevation_a+Ay_elevation_b)
    
    Ay_elevation_chose = np.where(Ay_elevation_all >= 0.2617993877991494)
    
    '''
    Ay_q_p_iono : KALMAN 的 Q矩陣設計用係數 與仰角有關
    '''
    Ay_q_p_iono = (F_sig_viono*F_BL/(1-(F_Re*np.cos(Ay_elevation_all[Ay_elevation_chose])/(F_Re+F_ion_h))**2)**0.5)**2*(1-np.e**(-2*F_alpha_iono*I_dt))/(2*F_alpha_iono)

    '''
    以衛星仰角篩選資料以下資料
    Ay_obs_phi_p_SD
    Ay_obs_L_p_SD
    Ay_sate_chose_a
    '''
    Ay_obs_phi_p_SD = Ay_obs_phi_p_SD[Ay_elevation_chose]
    Ay_obs_L_p_SD = Ay_obs_L_p_SD[Ay_elevation_chose]
    Ay_sate_chose_a = Ay_sate_chose_a[Ay_elevation_chose]
    
    '''
    進入 KALMAN 計算流程
    '''
    
    '''
    以下2個初始值不太重要  跌代後會收斂
    X 矩陣設計 (時鐘bios ,時鐘drift ,dI ,N) [2+2N ,1]
    
    P 矩陣設計 [2+2N ,2+2N]
    會依你計算所用的衛星編號來調用 Ay_P_all 中相對應的系數
    
    '''
    if I_time_chose == 0:
        Mt_X = np.matrix(np.zeros(2+len(Ay_obs_phi_p_SD)*2)).T   # 初始狀態 
        Mt_P = np.matrix(np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2)))   # 狀態協方差矩陣
    else:
        Mt_X = np.zeros((2+len(Ay_obs_phi_p_SD)*2,1))
        Mt_X[0,0] = Ay_receiver_bias_all[I_time_chose-1]
        Mt_X[1,0] = Ay_receiver_drift_all[I_time_chose-1]
        Mt_X[2:2+len(Ay_obs_phi_p_SD),0] = Ay_d_I_SD_all[I_time_chose-1,Ay_sate_chose_a]
        Mt_X[2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2,0] = Ay_N_SD_all[I_time_chose-1,Ay_sate_chose_a]
        Mt_X = np.matrix(Mt_X)
        
        Mt_P = np.matrix(np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2)))
        Mt_P[:2,:2] = np.matrix(Ay_P_all[:2,:2])
        for I_i_chose in range(int(len(Ay_obs_phi_p_SD))):
            for I_j_chose in range(int(len(Ay_obs_phi_p_SD))):
#                print(2+I_i_chose,2+I_j_chose)
#                print(2+Ay_sate_chose_a[I_i_chose],2+Ay_sate_chose_a[I_j_chose])
                Mt_P[2+I_i_chose,2+I_j_chose] = Ay_P_all[2+Ay_sate_chose_a[I_i_chose],2+Ay_sate_chose_a[I_j_chose]]
                Mt_P[2+len(Ay_obs_phi_p_SD)+I_i_chose,2+len(Ay_obs_phi_p_SD)+I_j_chose] = Ay_P_all[2+32+Ay_sate_chose_a[I_i_chose],2+32+Ay_sate_chose_a[I_j_chose]]
#        print(Mt_P[1,0]-Mt_P[0,1])
#        Mt_P = np.matrix(np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2)))
#        for I_i_chose in range(int(len(Ay_obs_phi_p_SD)/2)):
#            for I_j_chose in range(int(len(Ay_obs_phi_p_SD)/2)):
#                Mt_P[I_i_chose,I_j_chose] = Ay_P_all[Ay_sate_chose_a[I_i_chose],Ay_sate_chose_a[I_j_chose]]
#                Mt_P[int(len(Ay_obs_phi_p_SD)/2)+I_i_chose,int(len(Ay_obs_phi_p_SD)/2)+I_j_chose] = Ay_P_all[32+Ay_sate_chose_a[I_i_chose],32+Ay_sate_chose_a[I_j_chose]]

    '''
    模型設定
    Mt_X_(t) = Mt_F*Mt_X(t-1)
    Mt_F : (2+2*n) X (2+2*n) 
    Mt_Q : (2+2*n) X (2+2*n) 
    
    F 矩陣 : [2+2N ,2+2N]
        時鐘誤差的F   :  [[ 1  dt ]
                        [ 0   1 ]]
        電離層的F     : diag([e^(dt*F_alpha_iono)]) [ n ,n ]
        ambiguity的F : I [ n ,n ]  
        
    Q 矩陣 : [2+2N ,2+2N]
        細節參照  [Fujita 2010]
    '''
    Mt_F_make = np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2))
    Mt_F_make[:2,:2] = np.array([[1,I_dt],[0,1]])
    Mt_F_make[2:2+len(Ay_obs_phi_p_SD),2:2+len(Ay_obs_phi_p_SD)] = np.eye(len(Ay_obs_phi_p_SD))*(np.e**(-F_alpha_iono*I_dt))
    Mt_F_make[2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2] = np.eye(len(Ay_obs_phi_p_SD))
    Mt_F = np.matrix(Mt_F_make)
    
    Mt_Q_make = np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2))
    Mt_Q_make[:2,:2] = np.array([[I_dt * F_sig_b**2 + (1/3.)*I_dt**3 * F_sig_b_dot**2, 0.5*I_dt**2 * F_sig_b_dot**2],
                                 [                       0.5*I_dt**2 * F_sig_b_dot**2,        I_dt * F_sig_b_dot**2]])
    Mt_Q_make[2:2+len(Ay_obs_phi_p_SD),2:2+len(Ay_obs_phi_p_SD)] = np.eye(len(Ay_obs_phi_p_SD)) * Ay_q_p_iono
    Mt_Q_make[2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2] = np.eye(len(Ay_obs_phi_p_SD))*(F_sig_amb**2)*I_dt
    Mt_Q = np.matrix(Mt_Q_make)

    '''
    觀測相關
    Mt_Z = Mt_H*Mt_X
    
    H矩陣    : [ 2n ,2+2n]
      [[ 1 ,0 ,-I ,lambda*I    ]     n
       [ 1 ,0 , 0 ,lambda*I*0.5]]    n
         1  1   n      n
         
    R矩陣    : [ 2n ,2n]   
      表 SD phase 量測誤差
    '''
    Mt_H_make = np.zeros((2*len(Ay_obs_phi_p_SD),2+2*len(Ay_obs_phi_p_SD)))
    Mt_H_make[:,0] = 1
    Mt_H_make[:len(Ay_obs_phi_p_SD),2:len(Ay_obs_phi_p_SD)+2] = -np.eye(len(Ay_obs_phi_p_SD))
    Mt_H_make[:len(Ay_obs_phi_p_SD),len(Ay_obs_phi_p_SD)+2:len(Ay_obs_phi_p_SD)*2+2] = np.eye(len(Ay_obs_phi_p_SD))*F_L1_eave_length
    Mt_H_make[len(Ay_obs_phi_p_SD):,len(Ay_obs_phi_p_SD)+2:len(Ay_obs_phi_p_SD)*2+2] = np.eye(len(Ay_obs_phi_p_SD))*F_L1_eave_length*0.5
    Mt_H = np.matrix(Mt_H_make)  # 觀測矩陣
    
    Mt_R = np.matrix(np.eye(2*len(Ay_obs_phi_p_SD)))*0.03

    '''
    KALMAN 計算過程
    '''
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv(Mt_H*Mt_P_*(Mt_H.T) + Mt_R)
    Mt_Z  = np.matrix( np.concatenate((Ay_obs_phi_p_SD,Ay_obs_L_p_SD))).T
#    Mt_Z  = np.matrix( np.concatenate((Ay_obs_L_p_SD,Ay_obs_phi_p_SD))).T
    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
    Mt_P  = (np.eye(2+2*len(Ay_obs_phi_p_SD)) - Mt_K*Mt_H)*Mt_P_
    
    '''
    紀錄更新所求得數據
    '''
    
    Ay_receiver_bias_all[I_time_chose] = Mt_X[0,0]
    Ay_receiver_drift_all[I_time_chose] = Mt_X[1,0]
    Ay_d_I_SD_all[I_time_chose,Ay_sate_chose_a] = np.array(Mt_X[2:len(Ay_obs_phi_p_SD)+2,0])[:,0]
    Ay_N_SD_all[I_time_chose,Ay_sate_chose_a] = np.array(Mt_X[len(Ay_obs_phi_p_SD)+2:len(Ay_obs_phi_p_SD)*2+2,0])[:,0]
    
    
    
    Ay_D = np.zeros((len(Ay_obs_phi_p_SD)-1,len(Ay_obs_phi_p_SD)))
    Ay_D[:,0] = -1
    Ay_D[:,1:] = np.eye(len(Ay_obs_phi_p_SD)-1)
    Mt_D = np.matrix(Ay_D)
    
    '''
    LAMBDA 法過程
    Mt_N_DD    : SD_N 改為 DD_N
    Mt_P_N_DD  : SD_N
    
    Mt_L,Mt_D  : LDL_decomposition 後的 L矩陣與D矩陣
    Ay_a_      : 就是 Mt_N_DD (我忘記為啥要這行)
    Ay_LAMBDA_chose : LAMBDA
    '''
    Mt_N_DD = Mt_D*Mt_X[2+len(Ay_obs_phi_p_SD):]
    Mt_P_N_DD = Mt_D*Mt_P[2+len(Ay_obs_phi_p_SD):,2+len(Ay_obs_phi_p_SD):]*(Mt_D.T)
    
    Mt_L,Mt_D = LDL.D_L_design(Mt_P_N_DD)
    Ay_a_ = np.array(Mt_N_DD.T)
    Ay_LAMBDA_chose = LAMBDA.search(Ay_a_,10,Mt_D,Mt_L)
    
#    print(Ay_LAMBDA_chose[0]*F_L1_eave_length)
    '''
    Ay_ans_test   : a站與b站的位置向量
    tt_ans        : a站與b站的位置向量分別乘上Ay_EOL_b_x,y,z_DD
    test_         : DD_phase 減去 DD_N*波長
                    理論上 test_ 會與 np.sum(tt_ans,1) 相同
    '''
    Ay_ans_test = (Ay_position_a - Ay_position_b)[0]
    tt_ans,tt_x_DD =  np.meshgrid(Ay_ans_test,Ay_EOL_b_x_DD)
    tt_ans[:,0] *= Ay_EOL_b_x_DD
    tt_ans[:,1] *= Ay_EOL_b_y_DD
    tt_ans[:,2] *= Ay_EOL_b_z_DD

    test_ = Ay_phi_DD - Ay_LAMBDA_chose[0]*F_L1_eave_length 
    
    '''
    test_ : 理論上 BL * 向量 值
    np.sum(tt_ans,1) : N_DD * 波長 值總和實際值
    Ay_LAMBDA_chose[0]*F_L1_eave_length : N_DD * 波長 值
    Ay_phi_DD : DD觀測量值
    '''
    print(test_ - np.sum(tt_ans,1))
#    print(Ay_phi_DD - np.sum(tt_ans,1))
#    print(Ay_LAMBDA_chose[0]*F_L1_eave_length)
    

    Ay_P_all[:2,:2] = np.array(Mt_P[:2,:2])
    for I_i_chose in range(int(len(Ay_obs_phi_p_SD))):
        for I_j_chose in range(int(len(Ay_obs_phi_p_SD))):
            Ay_P_all[2+Ay_sate_chose_a[I_i_chose],2+Ay_sate_chose_a[I_j_chose]] = Mt_P[2+I_i_chose,2+I_j_chose]
            Ay_P_all[2+32+Ay_sate_chose_a[I_i_chose],2+32+Ay_sate_chose_a[I_j_chose]] = Mt_P[2+len(Ay_obs_phi_p_SD)+I_i_chose,2+len(Ay_obs_phi_p_SD)+I_j_chose]
 

#    for I_i_chose in range(int(len(Ay_obs_phi_p_SD)/2)):
#        for I_j_chose in range(int(len(Ay_obs_phi_p_SD)/2)):
#            Ay_P_all[Ay_sate_chose_a[I_i_chose],Ay_sate_chose_a[I_j_chose]] = Mt_P[I_i_chose,I_j_chose]
#            Ay_P_all[32+Ay_sate_chose_a[I_i_chose],32+Ay_sate_chose_a[I_j_chose]] = Mt_P[int(len(Ay_obs_phi_p_SD)/2)+I_i_chose,
#                    int(len(Ay_obs_phi_p_SD)/2)+I_j_chose]

    Ay_P_all_test[I_time_chose] = Ay_P_all
    Ay_obs_phi_p_SD_all[I_time_chose,Ay_sate_chose_a] = Ay_obs_phi_p_SD
    Ay_obs_L_p_SD_all[I_time_chose,Ay_sate_chose_a] = Ay_obs_L_p_SD
#    test_sum = np.sum(Ay_P_all.diagonal())
#    test_Lst.append(np.sum(Ay_P_all.diagonal()))
test = Ay_N_SD_all
Ay_obs_phi_p_SD_KALMAN = test[:,1]*F_L1_eave_length
Ay_obs_phi_p_SD_KALMAN[np.where(Ay_obs_phi_p_SD_KALMAN==0)]=np.nan
Ay_obs_phi_p_SD_KALMAN += Ay_receiver_bias_all
Ay_obs_phi_p_SD_KALMAN -= Ay_d_I_SD_all[:,1]
plt.plot(Ay_obs_phi_p_SD_KALMAN)
Ay_obs_phi_p_SD_all[np.where(Ay_obs_phi_p_SD_all==0)]=np.nan
plt.plot(Ay_obs_phi_p_SD_all[:,1])
#        Lst_x_1.append(Mt_X[0,0])
#        Lst_x_2.append(Mt_X[3,0])  
#        Lst_v_1.append(Mt_X[1,0])
#        Lst_v_2.append(Mt_X[4,0])
#        Lst_a_1.append(Mt_X[2,0])
#        Lst_a_2.append(Mt_X[5,0])   
#    
#    
#plt.figure(1)
#plt.title('x')
#plt.plot(Lst_x_1,color='red')
#plt.plot(Ay_Z_x_1,color='red',ls='--')
#plt.plot(Lst_x_2,color='blue')
#plt.plot(Ay_Z_x_2,color='blue',ls='--')
#plt.plot(Ay_Z_x_ans,color='black',ls='--')
#
#plt.figure(2)
#plt.title('v')
#plt.plot([0,I_total_t/I_dt],[0,I_a*I_total_t],color='black')
#plt.plot(Lst_v_1,color='red')
#plt.plot(Lst_v_2,color='blue')
#
#plt.figure(3)
#plt.title('a')
#plt.plot([0,I_total_t/I_dt],[I_a,I_a],color='black')
#plt.plot(Lst_a_1,color='red')
#plt.plot(Lst_a_2,color='blue')

