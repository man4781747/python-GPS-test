# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:19:46 2018

@author: owo

卡爾曼濾波器測試練習 - 3
觀測量有 2:
    1. 位置
    2. 速度

假設一汽車在直線上
初始位置 x = 0
速度 v = 0
加速度 a = 1
做直線等加速運動
本次觀測量有位置及速度
其位置觀測誤差的標準差為 5
速度觀測誤差的標準差為 0.5

觀測了 100 秒 
1 秒觀測 1 次


""" 
import numpy as np 
import matplotlib.pyplot as plt

I_a = 1
I_dt = 0.1
I_total_t = 60

I_observe_sig_x = 0.5 
I_observe_sig_v = 1

Ay_Z_x = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2) + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_x
Ay_Z_v = np.arange(0,I_total_t,I_dt)*I_a + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_v

Ay_Z_x_ans = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2)
Ay_Z_v_ans = np.arange(0,I_total_t,I_dt)*I_a
'''
以下2個初始值不太重要  跌代後會收斂
'''
Mt_X = np.matrix([[0,0,0]]).T   # 初始狀態 [位置, 速度, 加速度]
Mt_P = np.matrix([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]])   # 狀態協方差矩陣

Mt_F = np.matrix([[1, I_dt, 0.5*I_dt**2],
                  [0,    1,        I_dt],
                  [0,    0,           1]])          # 狀態轉移矩陣
    
Mt_Q = np.matrix([[1000,      0,      0],
                  [     0, 1000,      0],
                  [     0,      0, 1000]])   # 狀態轉移協方差矩陣

Mt_H = np.matrix([[1, 0, 0],
                  [0, 1, 0]])  # 觀測矩陣

Mt_R = np.matrix([[I_observe_sig_x*1000, 0],
                  [0, I_observe_sig_v*1000]])  # 觀測儀器的誤差標準差

Lst_x = []
Lst_v = []
Lst_a = []

for i in range(len(Ay_Z_x)):
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv((Mt_H*Mt_P_*(Mt_H.T) + Mt_R))
    Mt_X  = Mt_X_ + Mt_K*( np.matrix([[Ay_Z_x[i]],[Ay_Z_v[i]]]) - Mt_H * Mt_X_)
    print( (np.matrix([[Ay_Z_x[i]],[Ay_Z_v[i]]]) - Mt_H * Mt_X_)[0,0] )
    Mt_P  = (np.eye(3) - Mt_K*Mt_H)*Mt_P_
    Lst_x.append(Mt_X[0,0])
    Lst_v.append(Mt_X[1,0])  
    Lst_a.append(Mt_X[2,0])  
    
plt.figure(1)
plt.scatter(Lst_x,Lst_v,s=20,c='red')
plt.scatter(Ay_Z_x,Ay_Z_v,s=20,c='blue')
plt.plot(Ay_Z_x_ans,Ay_Z_v_ans,c='red')

#plt.plot(Ay_Z_a - Ay_Z_v_ans)
#plt.plot(Lst_a - Ay_Z_v_ans)


#plt.scatter(Lst_x,Ay_Z_x_ans,s=10,c='black')
#plt.scatter(Lst_v,Ay_Z_v_ans,s=10,c='red')