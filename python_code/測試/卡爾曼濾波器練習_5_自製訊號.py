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

F_sig_b_dot = 0
F_sig_b = 0.01
F_Re = 6371000.       # earth radius (m)
F_ion_h = 325000.      # ionsphere hight (m)

F_L1_eave_length = (299792458.0/1.57542e9) #(m)
I_dt = 30.

F_alpha_iono = 1/150   #(1/30 ~ 1/300)
F_sig_viono = 1/100.
F_sig_amb = 0.001

F_phi_meansure_error = 0.03
F_L_meansure_error = 0.03

Ay_time = np.arange(0,2880*30.,30.)
F_gpsweektime = (float(DOY2GPSweek(15,76))%10)*24*3600

Ay_n_data = np.load(r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15076.npy')
S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'
S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\pepu15076_position.npy'
Ay_position_a = np.load(S_a_position_path)[0:1,:]
Ay_position_b = np.load(S_b_position_path)[0:1,:]

Ay_C1_fake = np.zeros((2880,10)) 
Ay_C1_fake[:,0:10] = 1
Ay_sate_position_x = np.zeros((2880,10))
Ay_sate_position_y = np.zeros((2880,10))
Ay_sate_position_z = np.zeros((2880,10))

F_clock_bias_a  = 1000.
F_clock_drift_a = 0.
F_clock_bias_b  = 100.
F_clock_drift_b = 0.

#Ay_clock_delay_a = np.zeros(2880) + np.arange(0,F_clock_drift_a*2880,F_clock_drift_a)
#Ay_clock_delay_b = np.zeros(2880) + np.arange(0,F_clock_drift_b*2880,F_clock_drift_b)
Ay_clock_delay_a = np.zeros((2880,1))+F_clock_bias_a
Ay_clock_delay_b = np.zeros((2880,1))+F_clock_bias_b
Ay_clock_delay_SD_ans = Ay_clock_delay_a - Ay_clock_delay_b
Ay_clock_delay_a_obs = Ay_clock_delay_a+np.random.randn(2880,1)*F_sig_b
Ay_clock_delay_b_obs = Ay_clock_delay_b+np.random.randn(2880,1)*F_sig_b
Ay_clock_delay_SD_obs = Ay_clock_delay_a_obs+Ay_clock_delay_b_obs
Ay_clock_delay_SD_KALMAN = np.zeros((2880,1))

Ay_d_I_ans = np.zeros((2880,10))
Ay_d_I_ans[0] = np.arange(1,11,1)*1000

for I_ii in range(2879):
    Ay_d_I_ans[I_ii+1] = Ay_d_I_ans[I_ii]*(np.e**(-I_dt*F_alpha_iono))



Ay_N_SD_ans = np.zeros((2880,10)) + 100
Ay_N_SD_obs = Ay_N_SD_ans + np.random.randn(2880,10)*F_sig_amb
Ay_N_SD_KALMAN = np.zeros((2880,10))

for I_time_chose in range(2880):
    F_a_timechose_total = Ay_time[I_time_chose]
    Ay_sate_n_data_a = Get_n_data_each_time(I_time_chose,Ay_C1_fake[:,0:10],Ay_n_data,F_a_timechose_total)[::-1]
    Ay_sate_chose_a = Ay_sate_n_data_a[:,0].astype('int')-1
    
    Mobj_sate_cal_a = Satellite_Calculate(Ay_sate_n_data_a)
    Ay_delta_t_sv_a = Mobj_sate_cal_a.get_sate_clock_error(Ay_C1_fake[I_time_chose,0:10],F_a_timechose_total,0,F_gpsweektime)
    (Ay_xk_a,Ay_yk_a,Ay_zk_a,Ay_delta_t_sv_a) = Mobj_sate_cal_a.get_sate_position(
                                            F_a_timechose_total,0,
                                            F_gpsweektime,Ay_delta_t_sv_a,Ay_C1_fake[I_time_chose,0:10])    
    
    Ay_sate_position_x[I_time_chose,:] = Ay_xk_a
    Ay_sate_position_y[I_time_chose,:] = Ay_yk_a
    Ay_sate_position_z[I_time_chose,:] = Ay_zk_a
    
Ay_geolength_a = ((Ay_sate_position_x - Ay_position_a[0,0])**2+(Ay_sate_position_y - Ay_position_a[0,1])**2+(Ay_sate_position_z - Ay_position_a[0,2])**2)**0.5
Ay_geolength_b = ((Ay_sate_position_x - Ay_position_b[0,0])**2+(Ay_sate_position_y - Ay_position_b[0,1])**2+(Ay_sate_position_z - Ay_position_b[0,2])**2)**0.5

Ay_phi_p_SD_ans = Ay_d_I_ans +F_L1_eave_length*Ay_N_SD_ans + Ay_clock_delay_SD_ans

Ay_phi_p_SD_obs = Ay_d_I_ans + F_L1_eave_length*Ay_N_SD_obs + Ay_clock_delay_SD_obs + np.random.randn(2880,10)*F_phi_meansure_error
#Ay_phi_p_SD_obs = Ay_d_I_ans + F_L1_eave_length*Ay_N_SD + Ay_clock_delay_SD_ans

Ay_L_p_SD_ans = 0.5*F_L1_eave_length*Ay_N_SD_ans + Ay_clock_delay_SD_ans

Ay_L_p_SD_obs = 0.5*F_L1_eave_length*Ay_N_SD_obs + Ay_clock_delay_SD_obs + np.random.randn(2880,10)*F_L_meansure_error
#Ay_L_p_SD_obs = 0.5*F_L1_eave_length*Ay_N_SD + Ay_clock_delay_SD_ans

Ay_input = np.concatenate((Ay_phi_p_SD_obs,Ay_L_p_SD_obs),1)
#    Ay_sate_position_a = np.array([Ay_xk_a,Ay_yk_a,Ay_zk_a]).T

'''
以下2個初始值不太重要  跌代後會收斂
'''
Mt_X = np.matrix(np.zeros((2+10+10,1)))
Mt_P = np.matrix(np.zeros((2+10+10,2+10+10)))   # 狀態協方差矩陣

    
'''
模型設定
Mt_X_(t) = Mt_F*Mt_X(t-1)
'''
Mt_F_make = np.zeros((2+10*2,2+10*2))
Mt_F_make[:2,:2] = np.array([[1,I_dt],[0,1]])
Mt_F_make[2:2+10,2:2+10] = np.eye(10)*(np.e**(-I_dt*F_alpha_iono))
Mt_F_make[2+10:2+10*2,2+10:2+10*2] = np.eye(10)
Mt_F = np.matrix(Mt_F_make)

#Mt_Q_make = np.zeros((2+10*2,2+10*2))
#Mt_Q_make[:2,:2] = np.array([[I_dt * F_sig_b**2 + (1/3.)*I_dt**3 * F_sig_b_dot**2, 0.5*I_dt**2 * F_sig_b_dot**2],
#                         [                       0.5*I_dt**2 * F_sig_b_dot**2,        I_dt * F_sig_b_dot**2]])
#Mt_Q_make[2:2+10,2:2+10] = np.eye(10) * Ay_q_p_iono
#Mt_Q_make[2+10:2+10*2,2+10:2+10*2] = np.eye(10)*(F_sig_amb**2)*I_dt
#Mt_Q = np.matrix(Mt_Q_make)
Mt_Q = np.matrix(np.eye(2+10*2))*1
Mt_Q[:2,:2] = np.matrix([[F_sig_b**2*I_dt + F_sig_b_dot**2*I_dt**3/3 , F_sig_b_dot**2*I_dt**2/2],
                         [F_sig_b_dot**2*I_dt**2/2                   , F_sig_b_dot**2*I_dt]])
Mt_Q[2+10:2+10*2,2+10:2+10*2] = np.eye(10)*F_sig_amb**2*I_dt
'''
觀測相關
Mt_Z = Mt_H*Mt_X
'''
Mt_H_make = np.zeros((2*10,2+2*10))
Mt_H_make[:,0] = 1
Mt_H_make[:10,2:10+2] = -np.eye(10)
Mt_H_make[:10,10+2:10*2+2] = np.eye(10)*F_L1_eave_length
Mt_H_make[10:,10+2:10*2+2] = np.eye(10)*F_L1_eave_length*0.5
Mt_H = np.matrix(Mt_H_make)  # 觀測矩陣

Ay_R_make = np.zeros((20,20))
Ay_R_make[:10,:10] = np.eye(10)*F_phi_meansure_error
Ay_R_make[10:20,10:20] = np.eye(10)*F_phi_meansure_error
Mt_R = np.matrix(Ay_R_make)


for i in range(2880):
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv((Mt_H*Mt_P_*(Mt_H.T) + Mt_R))
    Mt_Z  = np.matrix(Ay_input[i]).T
    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
    Mt_P  = (np.eye(20+2) - Mt_K*Mt_H)*Mt_P_  
    Ay_N_SD_KALMAN[i,:] = np.array(Mt_X[12:22,0])[:,0]
    Ay_clock_delay_SD_KALMAN[i] = Mt_X[0,0]
    
plt.figure(1)
plt.title('N')
plt.plot(Ay_N_SD_obs[:,3])
plt.plot(Ay_N_SD_KALMAN[:,1])

plt.figure(2)
plt.title('t')
plt.plot(Ay_clock_delay_SD_obs)
plt.plot(Ay_clock_delay_SD_KALMAN)

Ay_L_p_SD_obs_test = 0.5*F_L1_eave_length*Ay_N_SD_obs + Ay_clock_delay_SD_obs
Ay_L_p_SD_KALMAN = 0.5*F_L1_eave_length*Ay_N_SD_KALMAN + Ay_clock_delay_SD_KALMAN
plt.figure(3)
plt.title('test')
plt.plot(Ay_L_p_SD_obs_test[:,0])
plt.plot(Ay_L_p_SD_KALMAN[:,0])
#Ay_phi_p_SD_KALMAN = Ay_d_I_KALMAN + F_L1_eave_length*Ay_N_SD_KALMAN + Ay_clock_delay_SD_KALMAN