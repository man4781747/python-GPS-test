# -*- coding: utf-8 -*-
"""
Created on Fri May  4 14:54:58 2018

@author: owo
"""

import numpy as np 
import matplotlib.pyplot as plt
from DOY2GPSweek import DOY2GPSweek
from GNSS_positioning_argv_ver2 import *
import xyz2enu
import LDL_decomposition as LDL
import LAMBDA


F_L1_eave_length = (299792458.0/1.57542e9) #(m)

F_phi_obs_error = 0.0019
F_pr_obs_error = 3

I_dt = 30.
'''
測試檔案位置
'''
S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseC1.npy'
S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseL1.npy'
S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseC1.npy'
S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseL1.npy'
S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phasetime.npy'
S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phasetime.npy'
S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15076.npy'
S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'
S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'

#S_C1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseC1.npy'
#S_L1_data_path_a = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phaseL1.npy'
#S_C1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseC1.npy'
#S_L1_data_path_b = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phaseL1.npy'
#S_a_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\pepu15076phasetime.npy'
#S_b_time_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\phase_data\30s\hual15076phasetime.npy'
#S_n_data_path    = r'D:\Ddddd\python\2003\Odata\test\n_data\n_data_15076.npy'
#S_a_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\pepu15076_position.npy'
#S_b_position_path    = r'D:\Ddddd\python\2003\Odata\test\data2015076\position_data\hual15076_position.npy'
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
Ay_position_b = np.load(S_b_position_path)[0:1,:]

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
#%%
#for I_time_chose in range(len(Ay_time_a)):
#for I_time_chose in range(2880):
for I_time_chose in range(100):
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
    
    '''
    不同衛星SD資料做DD,以衛星編號最小的為主
    '''
    Ay_DD_L1_ab = (Ay_SD_L1_ab-Ay_SD_L1_ab[0])[1:]
    Ay_DD_C1_ab = (Ay_SD_C1_ab-Ay_SD_C1_ab[0])[1:]
#    print(Ay_DD_L1_ab)
    '''
    時間分為整數位及小數位來計算
    '''
    F_b_timechose_int = int(Ay_time_b[I_time_chose])
    F_b_timechose_float = Ay_time_b[I_time_chose]%1
    F_b_timechose_total = Ay_time_b[I_time_chose]
    
    '''
    Ay_sate_n_data_b : 依有資料的衛星來選取 n data
    Ay_sate_chose_b  : 選取的衛星編號
    Ay_C1_b_chose    : 相對應衛星的C1資料
    '''
    Ay_sate_n_data_b = Get_n_data_each_time(I_time_chose,Ay_C1_b,Ay_n_data,F_b_timechose_total)[::-1]
    Ay_sate_chose_b = Ay_sate_n_data_b[:,0].astype('int')-1
    Ay_C1_b_chose = Ay_C1_b[I_time_chose,Ay_sate_chose_b]
    
    '''
    Mobj_sate_cal_b       : 計算 測站 衛星相關資料 (Mobj)
    Ay_delta_t_sv_b       : 衛星時終誤差 (s)   (一開始粗略估計,而後求出精準)
    Ay_xk,Ay_yk,Ay_zk       : 測站所有衛星位置(m) (ECEF)
    '''
    Mobj_sate_cal_b = Satellite_Calculate(Ay_sate_n_data_b)
    Ay_delta_t_sv_b = Mobj_sate_cal_b.get_sate_clock_error(Ay_C1_b_chose,F_b_timechose_int,F_b_timechose_float,F_gpsweektime)
    (Ay_xk_b,Ay_yk_b,Ay_zk_b,Ay_delta_t_sv_b) = Mobj_sate_cal_b.get_sate_position(
                                            F_b_timechose_int,F_b_timechose_float,
                                            F_gpsweektime,Ay_delta_t_sv_b,Ay_C1_b_chose)  
    Ay_sate_position_b = np.array([Ay_xk_b,Ay_yk_b,Ay_zk_b]).T
    
    '''
    計算測站與衛星間地理距離
    Ay_geographical_distance_b  : b測站與衛星的地理距離(尚未修自轉)
    '''
    Ay_geographical_distance_b =((Ay_xk_b-Ay_position_b[0,0])**2+(Ay_yk_b-Ay_position_b[0,1])**2+(Ay_zk_b-Ay_position_b[0,2])**2)**0.5
    
    '''
    Ay_LOS_b_x,y,z     : 測站與衛星的單位方向向量
    '''
    
    Ay_LOS_b_x = ((Ay_xk_b-Ay_position_b[0,0])/Ay_geographical_distance_b)
    Ay_LOS_b_y = ((Ay_yk_b-Ay_position_b[0,1])/Ay_geographical_distance_b)
    Ay_LOS_b_z = ((Ay_zk_b-Ay_position_b[0,2])/Ay_geographical_distance_b)

    '''
    以下2個初始值不太重要  跌代後會收斂
    Mt_X : 狀態矩陣 [BL_x ,BL_y ,BL_z ,SD-N]  [3+N,1]
    Mt_P : 狀態協方差矩陣 [3+N,3+N]
    #'''
    if I_time_chose == 0:
#        Mt_X = np.matrix(np.zeros(len(Ay_SD_L1_ab)*3)).T   # 初始狀態 (SD-r ,SD-I ,SD-N)     
        Mt_X = np.matrix(np.zeros(3+len(Ay_SD_L1_ab))).T   # 初始狀態 (BL_x ,BL_y ,BL_z ,SD-N)
        '''
        以下為正解 測試用
        '''
#        Mt_X[0] = 1283.102
#        Mt_X[1] = -1469.089
#        Mt_X[2] = 4296.1
        Mt_X[0] = 1285.102
        Mt_X[1] = -1470.089
        Mt_X[2] = 4396.1
#        Mt_P = np.matrix(np.zeros(((len(Ay_SD_L1_ab)*3),(len(Ay_SD_L1_ab)*3))))   # 狀態協方差矩陣
#        Mt_P = np.matrix(np.zeros(((3+len(Ay_SD_L1_ab)),(3+len(Ay_SD_L1_ab)))))   # 狀態協方差矩陣       
        Mt_P = np.matrix(np.eye(3+len(Ay_SD_L1_ab)))   # 狀態協方差矩陣       
    else:
        Mt_X = np.zeros((3+len(Ay_SD_L1_ab),1))
        Mt_X[:3,0] = Ay_BL_all[I_time_chose-1]
        Mt_X[3:,0] = Ay_N_SD_all[I_time_chose-1,Ay_sate_chose_b]
        Mt_X = np.matrix(Mt_X)
#        
        Mt_P = np.matrix(np.zeros((3+len(Ay_SD_L1_ab),3+len(Ay_SD_L1_ab))))
        Mt_P[:3,:3] = Ay_P_all[:3,:3]
        for i in range(len(Ay_sate_chose_b)):
            for j in range(len(Ay_sate_chose_b)):
                Mt_P[3+i,3+j] = Ay_P_all[3+Ay_sate_chose_b[i],3+Ay_sate_chose_b[j]]
                
                
    '''
    模型設定
    Mt_X_(t) = Mt_F*Mt_X(t-1)
    Mt_F : [3+N ,3+N ]
    Mt_Q : [3+N ,3+N ]
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
    Ay_D[:,0] = 1
    Ay_D[:,1:] = np.eye(len(Ay_DD_L1_ab))*-1
#    Mt_D = np.matrix(Ay_D)
    Ay_H_make = np.zeros((2*len(Ay_DD_L1_ab),3+len(Ay_SD_L1_ab)))
    
    Ay_H_make[:len(Ay_DD_L1_ab),0] = -Ay_LOS_b_x[0]+Ay_LOS_b_x[1:]
    Ay_H_make[len(Ay_DD_L1_ab):,0] = -Ay_LOS_b_x[0]+Ay_LOS_b_x[1:]
    Ay_H_make[:len(Ay_DD_L1_ab),1] = -Ay_LOS_b_y[0]+Ay_LOS_b_y[1:]
    Ay_H_make[len(Ay_DD_L1_ab):,1] = -Ay_LOS_b_y[0]+Ay_LOS_b_y[1:]
    Ay_H_make[:len(Ay_DD_L1_ab),2] = -Ay_LOS_b_z[0]+Ay_LOS_b_z[1:]
    Ay_H_make[len(Ay_DD_L1_ab):,2] = -Ay_LOS_b_z[0]+Ay_LOS_b_z[1:]
    Ay_H_make[:len(Ay_DD_L1_ab),3:] = Ay_D*F_L1_eave_length
    
    
#    Ay_H_make = np.zeros((2*len(Ay_DD_L1_ab),3*len(Ay_SD_L1_ab)))
#    Ay_H_make[:len(Ay_DD_L1_ab),:len(Ay_SD_L1_ab)] = Ay_D
#    Ay_H_make[len(Ay_DD_L1_ab):,:len(Ay_SD_L1_ab)] = Ay_D
#    Ay_H_make[:len(Ay_DD_L1_ab),len(Ay_SD_L1_ab):len(Ay_SD_L1_ab)*2] = -Ay_D
#    Ay_H_make[len(Ay_DD_L1_ab):,len(Ay_SD_L1_ab):len(Ay_SD_L1_ab)*2] = Ay_D
#    Ay_H_make[:len(Ay_DD_L1_ab),len(Ay_SD_L1_ab)*2:len(Ay_SD_L1_ab)*3] = Ay_D*F_L1_eave_length

    Mt_H = np.matrix(Ay_H_make)  # 觀測矩陣
    
    Mt_R = np.matrix(np.zeros((2*len(Ay_DD_L1_ab),2*len(Ay_DD_L1_ab))))
    Mt_phi_obs_error = np.matrix(np.eye(len(Ay_SD_L1_ab))*2*F_phi_obs_error**2)
    Mt_pr_obs_error  = np.matrix(np.eye(len(Ay_SD_C1_ab))*2*F_pr_obs_error**2) 
    Mt_R[:len(Ay_DD_L1_ab),:len(Ay_DD_L1_ab)] = np.matrix(Ay_D)*Mt_phi_obs_error*(np.matrix(Ay_D).T)
    Mt_R[len(Ay_DD_L1_ab):,len(Ay_DD_L1_ab):] = np.matrix(Ay_D)*Mt_pr_obs_error*(np.matrix(Ay_D).T)
    
    
    

    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv(Mt_H*Mt_P_*(Mt_H.T) + Mt_R)
    Mt_Z  = np.matrix( np.concatenate((Ay_DD_L1_ab,Ay_DD_C1_ab))).T
#    Mt_Z  = np.matrix( np.concatenate((Ay_obs_L_p_SD,Ay_obs_phi_p_SD))).T
    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
    Mt_P  = (np.eye(3+len(Ay_SD_L1_ab)) - Mt_K*Mt_H)*Mt_P_
    
    Ay_N_SD_all[I_time_chose,Ay_sate_chose_b] = np.array(Mt_X)[3:,0]
    Ay_BL_all[I_time_chose] = np.array(Mt_X)[:3,0]
    
    Ay_P_all[:3,:3] = Mt_P[:3,:3]
    
    for i in range(len(Ay_sate_chose_b)):
        for j in range(len(Ay_sate_chose_b)):
            Ay_P_all[3+Ay_sate_chose_b[i],3+Ay_sate_chose_b[j]] = Mt_P[3+i,3+j]
    
#    print(np.array(Mt_H[:len(Ay_DD_L1_ab),0:3]*(np.matrix([[1283.102,-1469.089,4296.1]]).T)))
#    print(Ay_DD_L1_ab+np.array(Mt_H[:len(Ay_DD_L1_ab),0:3]*(np.matrix([[1283.10199506,-1469.08949944,4296.10006949]]).T))[:,0])
    
#    
#    Ay_test[I_time_chose,Ay_sate_chose_a] = np.array(Mt_H * Mt_X_)[:len(Ay_obs_phi_p_SD),0]
#    
#    Ay_receiver_bias_all[I_time_chose] = Mt_X[0,0]
#    Ay_receiver_drift_all[I_time_chose] = Mt_X[1,0]
#    Ay_d_I_SD_all[I_time_chose,Ay_sate_chose_a] = np.array(Mt_X[2:len(Ay_obs_phi_p_SD)+2,0])[:,0]
#    Ay_N_SD_all[I_time_chose,Ay_sate_chose_a] = np.array(Mt_X[len(Ay_obs_phi_p_SD)+2:len(Ay_obs_phi_p_SD)*2+2,0])[:,0]
#    
#    Ay_D = np.zeros((len(Ay_obs_phi_p_SD)-1,len(Ay_obs_phi_p_SD)))
#    Ay_D[:,0] = -1
#    Ay_D[:,1:] = np.eye(len(Ay_obs_phi_p_SD)-1)
#    Mt_D = np.matrix(Ay_D)
#    
#    Mt_N_DD = Mt_D*Mt_X[2+len(Ay_obs_phi_p_SD):]
#    Mt_P_N_DD = Mt_D*Mt_P[2+len(Ay_obs_phi_p_SD):,2+len(Ay_obs_phi_p_SD):]*(Mt_D.T)
#    
#    Mt_L,Mt_D = LDL.D_L_design(Mt_P_N_DD)
#    Ay_a_ = np.array(Mt_N_DD.T)
#    Ay_LAMBDA_chose = LAMBDA.search(Ay_a_,10,Mt_D,Mt_L)
#    print(Ay_LAMBDA_chose[0])
##    Ay_N_DD = np.array(Mt_X[3+len(Ay_obs_phi_p_SD):] - Mt_X[2+len(Ay_obs_phi_p_SD)])
#  
#    for I_i_chose in range(int(len(Ay_obs_phi_p_SD)/2)):
#        for I_j_chose in range(int(len(Ay_obs_phi_p_SD)/2)):
#            Ay_P_all[Ay_sate_chose_a[I_i_chose],Ay_sate_chose_a[I_j_chose]] = Mt_P[I_i_chose,I_j_chose]
#            Ay_P_all[32+Ay_sate_chose_a[I_i_chose],32+Ay_sate_chose_a[I_j_chose]] = Mt_P[int(len(Ay_obs_phi_p_SD)/2)+I_i_chose,
#                    int(len(Ay_obs_phi_p_SD)/2)+I_j_chose]
#
#    Ay_P_all_test[I_time_chose] = Ay_P_all
#    Ay_obs_phi_p_SD_all[I_time_chose,Ay_sate_chose_a] = Ay_obs_phi_p_SD
#    Ay_obs_L_p_SD_all[I_time_chose,Ay_sate_chose_a] = Ay_obs_L_p_SD
##    test_sum = np.sum(Ay_P_all.diagonal())
#    test_Lst.append(np.sum(Ay_P_all.diagonal()))
#    test = Ay_N_SD_all
#Ay_obs_phi_p_SD_KALMAN = test[:,1]*F_L1_eave_length
#Ay_obs_phi_p_SD_KALMAN[np.where(Ay_obs_phi_p_SD_KALMAN==0)]=np.nan
#Ay_obs_phi_p_SD_KALMAN += Ay_receiver_bias_all
#Ay_obs_phi_p_SD_KALMAN -= Ay_d_I_SD_all[:,1]
#plt.plot(Ay_obs_phi_p_SD_KALMAN)
#Ay_obs_phi_p_SD_all[np.where(Ay_obs_phi_p_SD_all==0)]=np.nan