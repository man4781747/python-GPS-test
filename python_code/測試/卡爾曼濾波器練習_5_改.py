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

F_sig_b_dot = 0.001
F_sig_b = 0.001
F_Re = 6371000.       # earth radius (m)
F_ion_h = 325000.      # ionsphere hight (m)
F_alpha_iono = 0.03
F_sig_viono = 0.03
F_sig_amb = 0.01
F_L1_eave_length = (299792458.0/1.57542e9) #(m)
#F_L1_eave_length = 1
I_dt = 30.

S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseC1.npy'
S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseL1.npy'
S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseC1.npy'
S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseL1.npy'
S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phasetime.npy'
S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phasetime.npy'
S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15076.npy'
S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'
S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\pepu15076_position.npy'

Ay_C1_a = np.load(S_C1_data_path_a)
Ay_L1_a = np.load(S_L1_data_path_a)*F_L1_eave_length
Ay_C1_b = np.load(S_C1_data_path_b)
Ay_L1_b = np.load(S_L1_data_path_b)*F_L1_eave_length
Ay_time_a = np.load(S_a_time_path)
Ay_time_b = np.load(S_b_time_path)
Ay_n_data = np.load(S_n_data_path)
Ay_position_a = np.load(S_a_position_path)[0:1,:]
Ay_position_b = np.load(S_b_position_path)[0:1,:]

F_BL = np.sum( (Ay_position_a-Ay_position_b)**2 )**0.5

Ay_time_a = Ay_time_a[:,3]*3600+Ay_time_a[:,4]*60+Ay_time_a[:,5]
Ay_time_b = Ay_time_b[:,3]*3600+Ay_time_b[:,4]*60+Ay_time_b[:,5]

F_gpsweektime = (float(DOY2GPSweek(15,76))%10)*24*60*60

#Ay_check_array = np.zeros_like(Ay_C1_a)
Ay_check_array = np.where((Ay_C1_a==0.)|(Ay_L1_a==0.)|(Ay_C1_b==0.)|(Ay_L1_a==0.))
Ay_C1_a[Ay_check_array] = 0.
Ay_L1_a[Ay_check_array] = 0.
Ay_C1_b[Ay_check_array] = 0.
Ay_L1_b[Ay_check_array] = 0.

Ay_L_p_a = (Ay_C1_a+Ay_L1_a)*0.5
Ay_L_p_b = (Ay_C1_b+Ay_L1_b)*0.5

Ay_phi_p_SD = Ay_L1_a - Ay_L1_b
Ay_L_p_SD   = Ay_L_p_a - Ay_L_p_b

Ay_receiver_bias_all = np.zeros(len(Ay_L_p_SD))
Ay_receiver_drift_all = np.zeros(len(Ay_L_p_SD))
Ay_d_I_SD_all = np.zeros((len(Ay_L_p_SD),32))
Ay_N_SD_all = np.zeros((len(Ay_L_p_SD),32))

Ay_H_all = np.zeros((64,2+64))
Ay_F_all = np.zeros((2+64,2+64))
Ay_F_all[0:2,0:2] = np.array([[1,I_dt],[0,1]])
Ay_Q_all = np.zeros((2+64,2+64))
Ay_Q_all[0:2,0:2] = np.array([[I_dt * F_sig_b**2 + (1/3.)*I_dt**3 * F_sig_b_dot**2, 0.5*I_dt**2 * F_sig_b_dot**2],
                             [                       0.5*I_dt**2 * F_sig_b_dot**2,        I_dt * F_sig_b_dot**2]])

Ay_P_all = np.zeros((64+2,64+2))

for I_time_chose in range(len(Ay_time_a)):
#for I_time_chose in range(1):   
    F_a_timechose_int = int(Ay_time_a[I_time_chose])
    F_a_timechose_float = Ay_time_a[I_time_chose]%1
    F_a_timechose_total = Ay_time_a[I_time_chose]
    
    F_b_timechose_int = int(Ay_time_b[I_time_chose])
    F_b_timechose_float = Ay_time_b[I_time_chose]%1
    F_b_timechose_total = Ay_time_b[I_time_chose]
    
    '''
    Ay_sate_position_data_all     : 用 F_time_chose_sec_total 找尋該時刻有C1資料的衛星最接近的N檔資料
    Ay_sate_chose                 : 該時刻有的衛星編號 (注意是顛倒的喔!!)
    '''
    Ay_sate_n_data_a = Get_n_data_each_time(I_time_chose,Ay_C1_a,Ay_n_data,F_a_timechose_total)[::-1]
    Ay_sate_chose_a = Ay_sate_n_data_a[:,0].astype('int')-1
    Ay_sate_n_data_b = Get_n_data_each_time(I_time_chose,Ay_C1_b,Ay_n_data,F_b_timechose_total)[::-1]
    Ay_sate_chose_b = Ay_sate_n_data_b[:,0].astype('int')-1
    
    Ay_C1_a_chose = Ay_C1_a[I_time_chose,Ay_sate_chose_a]
    Ay_C1_b_chose = Ay_C1_b[I_time_chose,Ay_sate_chose_b]
    
    '''
    Mobj_sate_cal           : 計算 測站 衛星相關資料 (Mobj)
    Ay_delta_t_sv           : 衛星時終誤差 (s)   (一開始粗略估計,而後求出精準)
    sva                     : 測站 sva
    tgd                     : 測站 tgd
    Ay_xk,Ay_yk,Ay_zk       : 測站所有衛星位置(m) (ECEF)
    '''
    Mobj_sate_cal_a = Satellite_Calculate(Ay_sate_n_data_a)
    Ay_delta_t_sv_a = Mobj_sate_cal_a.get_sate_clock_error(Ay_C1_a_chose,F_a_timechose_int,F_a_timechose_float,F_gpsweektime)
    sva_a = Mobj_sate_cal_a.sva
    tgd_a = Mobj_sate_cal_a.tgd
    (Ay_xk_a,Ay_yk_a,Ay_zk_a,Ay_delta_t_sv_a) = Mobj_sate_cal_a.get_sate_position(
                                            F_a_timechose_int,F_a_timechose_float,
                                            F_gpsweektime,Ay_delta_t_sv_a,Ay_C1_a_chose)    
    Ay_sate_position_a = np.array([Ay_xk_a,Ay_yk_a,Ay_zk_a]).T
    
    Mobj_sate_cal_b = Satellite_Calculate(Ay_sate_n_data_b)
    Ay_delta_t_sv_b = Mobj_sate_cal_b.get_sate_clock_error(Ay_C1_b_chose,F_b_timechose_int,F_b_timechose_float,F_gpsweektime)
    sva_b = Mobj_sate_cal_b.sva
    tgd_b = Mobj_sate_cal_b.tgd
    (Ay_xk_b,Ay_yk_b,Ay_zk_b,Ay_delta_t_sv_b) = Mobj_sate_cal_b.get_sate_position(
                                            F_b_timechose_int,F_b_timechose_float,
                                            F_gpsweektime,Ay_delta_t_sv_b,Ay_C1_b_chose)  
    Ay_sate_position_b = np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T
    
    Ay_geographical_distance_a =((Ay_xk_a-Ay_position_a[0,0])**2+(Ay_yk_a-Ay_position_a[0,1])**2+(Ay_zk_a-Ay_position_a[0,2])**2)**0.5
    Ay_geographical_distance_b =((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5
    
    Ay_obs_phi_p_SD = Ay_phi_p_SD[I_time_chose,Ay_sate_chose_a] - (Ay_geographical_distance_a-Ay_geographical_distance_b)
    Ay_obs_L_p_SD   = Ay_L_p_SD[I_time_chose,Ay_sate_chose_a] - (Ay_geographical_distance_a-Ay_geographical_distance_b)
    
    '''
    衛星仰角
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
    
    
    '''
    q_p_iono
    '''
    Ay_q_p_iono = (F_sig_viono*F_BL/(1-(F_Re*np.cos(Ay_elevation_all)/(F_Re+F_ion_h))**2)**0.5)**2*(1-np.e**(-2*F_alpha_iono*I_dt))/(2*F_alpha_iono)

    '''
    以下2個初始值不太重要  跌代後會收斂
    #'''
    if I_time_chose == 0:
        Mt_X = np.matrix(np.zeros(2+len(Ay_obs_phi_p_SD)*2)).T
        Mt_P = np.matrix(np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2)))   # 狀態協方差矩陣
    else:
        Ay_X = np.zeros((2+len(Ay_obs_phi_p_SD)*2,1))     # (2+2n)*1
        Ay_X[0,0] = Ay_receiver_bias_all[I_time_chose-1]  # 1*1
        Ay_X[1,0] = Ay_receiver_drift_all[I_time_chose-1] # 1*1
        Ay_X[2:2+len(Ay_obs_phi_p_SD),0] = Ay_d_I_SD_all[I_time_chose-1,Ay_sate_chose_a] # n*1
        Ay_X[2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2,0] = Ay_N_SD_all[I_time_chose-1,Ay_sate_chose_a] # n*1
        Mt_X = np.matrix(Ay_X)  # (2+2n)*1
    '''
    模型設定
    Mt_X_(t) = Mt_F*Mt_X(t-1)
    
    此處設定F在沒訊號後 所有沒訊號衛星的新 Mt_X值歸0
    '''
    Ay_F_make = np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2))
    Ay_F_make[:2,:2] = np.array([[1,I_dt],[0,1]])
    Ay_F_make[2:2+len(Ay_obs_phi_p_SD),2:2+len(Ay_obs_phi_p_SD)] = np.eye(len(Ay_obs_phi_p_SD))*(np.e**(-0.3*I_dt))
    Ay_F_make[2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2] = np.eye(len(Ay_obs_phi_p_SD))
    Mt_F = np.matrix(Ay_F_make)
    

#    Ay_Q_make = np.copy(Ay_Q_all)
#    Ay_Q_make[2+Ay_sate_chose_a,2+Ay_sate_chose_a] = Ay_q_p_iono
#    Ay_Q_make[2+Ay_sate_chose_a,2+2*Ay_sate_chose_a] = (F_sig_amb**2)*I_dt
#    Mt_Q = np.matrix(Ay_Q_make)
    Ay_Q_make = np.zeros((2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD)*2))
    Ay_Q_make[:2,:2] = np.array([[I_dt * F_sig_b**2 + (1/3.)*I_dt**3 * F_sig_b_dot**2, 0.5*I_dt**2 * F_sig_b_dot**2],
                                 [                       0.5*I_dt**2 * F_sig_b_dot**2,        I_dt * F_sig_b_dot**2]])
    Ay_Q_make[2:2+len(Ay_obs_phi_p_SD),2:2+len(Ay_obs_phi_p_SD)] = Ay_q_p_iono*np.eye(len(Ay_obs_phi_p_SD))
    Ay_Q_make[2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2,2+len(Ay_obs_phi_p_SD):2+len(Ay_obs_phi_p_SD)*2] = (F_sig_amb**2)*I_dt*np.eye(len(Ay_obs_phi_p_SD))
    Mt_Q = np.matrix(Ay_Q_make)

    '''
    觀測相關
    Mt_Z = Mt_H*Mt_X
    '''
    Ay_H_make = np.zeros((2*len(Ay_obs_phi_p_SD),2+2*len(Ay_obs_phi_p_SD)))
    Ay_H_make[:,0] = 1
    Ay_H_make[:len(Ay_obs_phi_p_SD),2:2+len(Ay_obs_phi_p_SD)] = -np.eye(len(Ay_obs_phi_p_SD))
    Ay_H_make[:len(Ay_obs_phi_p_SD),2+len(Ay_obs_phi_p_SD):] = F_L1_eave_length*np.eye(len(Ay_obs_phi_p_SD))
    Ay_H_make[len(Ay_obs_phi_p_SD):,2+len(Ay_obs_phi_p_SD):] = F_L1_eave_length*0.5*np.eye(len(Ay_obs_phi_p_SD))
    Mt_H = np.matrix(Ay_H_make)  # 觀測矩陣
    
#    Mt_R = np.matrix([[0.0027,                 0],
#                      [                0, 0.1527]])  # 觀測儀器的誤差標準差
#    Ay_R_make = np.zeros((32+32,32+32))
#    Ay_R_make[Ay_sate_chose_a,Ay_sate_chose_a] = 0.27
#    Ay_R_make[32+Ay_sate_chose_a,32+Ay_sate_chose_a] = 3.
#    Mt_R = np.matrix(Ay_R_make)
    Ay_R_make = np.zeros((2*len(Ay_obs_phi_p_SD),2*len(Ay_obs_phi_p_SD)))
    Ay_R_make[len(Ay_obs_phi_p_SD):,len(Ay_obs_phi_p_SD):] = 0.27*np.eye(len(Ay_obs_phi_p_SD))
    Ay_R_make[:len(Ay_obs_phi_p_SD),:len(Ay_obs_phi_p_SD)] = 3.*np.eye(len(Ay_obs_phi_p_SD))
    Mt_R = np.matrix(Ay_R_make)
#    Lst_x_1 = []
#    Lst_x_2 = []
#    Lst_v_1 = []
#    Lst_v_2 = []
#    Lst_a_1 = []
#    Lst_a_2 = []
    
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv((Mt_H*Mt_P_*(Mt_H.T) + Mt_R))
    Mt_Z  = np.matrix( np.concatenate((Ay_phi_p_SD[I_time_chose,Ay_sate_chose_a],Ay_L_p_SD[I_time_chose,Ay_sate_chose_a]))).T
    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
    
    Ay_receiver_bias_all[I_time_chose] = Mt_X[0,0]
    Ay_receiver_drift_all[I_time_chose] = Mt_X[1,0]
    Ay_d_I_SD_all[I_time_chose,Ay_sate_chose_a] = np.array(Mt_X[2:32+2,0])[:,0]
    Ay_N_SD_all[I_time_chose,Ay_sate_chose_a] = np.array(Mt_X[32+2:32+32+2,0])[:,0]
    
    Mt_P  = (np.eye(2+2*32) - Mt_K*Mt_H)*Mt_P_
    
    test = Ay_N_SD
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

