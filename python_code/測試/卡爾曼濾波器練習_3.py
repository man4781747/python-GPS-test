# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:52:20 2018

@author: owo


卡爾曼濾波器測試練習 - 3
觀測量有 2:
    1. 位置 - 1
    2. 速度 - 1
    3. 位置 - 2
    4. 速度 - 2

假設一汽車在直線上
初始位置 x = 0
速度 v = 0
加速度 a = 1
做直線等加速運動
本次觀測量有位置及速度
其位置觀測誤差的標準差分別為 100 , 1
速度觀測誤差的標準差分別為 1 , 100

觀測了 100 秒 
1 秒觀測 1 次


""" 
import numpy as np 
import matplotlib.pyplot as plt

'''
I_a                        :  加速度
I_dt                       :  觀測時間間格
I_total_t                  :  總觀測時間
'''
I_a = 1
I_dt = 1
I_total_t = 100


I_observe_sig_x_1 = 10
I_observe_sig_v_1 = 10
Ay_Z_x_1 = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2) + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_x_1
Ay_Z_v_1 = np.arange(0,I_total_t,I_dt)*I_a + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_v_1

I_observe_sig_x_2 = 1
I_observe_sig_v_2 = 10
Ay_Z_x_2 = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2) + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_x_2
Ay_Z_v_2 = np.arange(0,I_total_t,I_dt)*I_a + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_v_2

Ay_Z_x_ans = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2)
Ay_Z_v_ans = np.arange(0,I_total_t,I_dt)*I_a
'''
以下2個初始值不太重要  跌代後會收斂
'''
Mt_X = np.matrix([[0,0,0,0]]).T   # 初始狀態 [位置-1, 速度-1 , 位置-2, 速度-2]
Mt_P = np.matrix([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])   # 狀態協方差矩陣

Mt_F = np.matrix([[1, I_dt,   0,    0],
                  [0,    1,   0,    0],
                  [0,    0,   1, I_dt],
                  [0,    0,   0,    1]])          # 狀態轉移矩陣
    
Mt_Q = np.matrix([[     1,      0,      0,      0],
                  [     0,      1,      0,      0],
                  [     0,      0,      1,      0],
                  [     0,      0,      0,      1]])   # 狀態轉移協方差矩陣 (值越大越不相信公式模組)

Mt_H = np.matrix([[     1,      0,      0,      0],
                  [     0,      1,      0,      0],
                  [     0,      0,      1,      0],
                  [     0,      0,      0,      1]])  # 觀測矩陣

Mt_R = np.matrix([[I_observe_sig_x_1,                 0,                 0,                 0],
                  [                0, I_observe_sig_v_1,                 0,                 0],
                  [                0,                 0, I_observe_sig_x_2,                 0],
                  [                0,                 0,                 0, I_observe_sig_v_2]])  # 觀測儀器的誤差標準差

Lst_x = []
Lst_v = []

Lst_P_diagonal = []
for i in range(len(Ay_Z_x_ans)):
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
#    Mt_K  = Mt_P_*(Mt_H.T)*((Mt_H*Mt_P_*(Mt_H.T) + Mt_R).T)
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv((Mt_H*Mt_P_*(Mt_H.T) + Mt_R))
    Mt_Z  = np.matrix([[Ay_Z_x_1[i]],
                       [Ay_Z_v_1[i]],
                       [Ay_Z_x_2[i]],
                       [Ay_Z_v_2[i]]])
    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
    Mt_P  = (np.eye(4) - Mt_K*Mt_H)*Mt_P_
    Lst_x.append(Mt_X[0,0])
    Lst_v.append(Mt_X[1,0])  
    Lst_P_diagonal.append(np.sum(Mt_P.diagonal()))
#    Lst_a.append(Mt_X[2,0])  

plt.figure(1)
plt.scatter(Lst_x,Lst_v,s=20,c='red')
plt.scatter(Ay_Z_x_1,Ay_Z_v_1,s=20,c='blue')
plt.scatter(Ay_Z_x_2,Ay_Z_v_2,s=20,c='green')
plt.plot(Ay_Z_x_ans,Ay_Z_v_ans,c='red',ls='--')

#plt.plot(Ay_Z_a - Ay_Z_v_ans)
#plt.plot(Lst_a - Ay_Z_v_ans)


#plt.scatter(Lst_x,Ay_Z_x_ans,s=10,c='black')
#plt.scatter(Lst_v,Ay_Z_v_ans,s=10,c='red')

