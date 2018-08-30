# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 16:52:17 2018

@author: owo
卡爾曼濾波器測試練習 - 4
觀測量有 2:
    1. 位置 - 1
    3. 位置 - 2

假設一汽車在直線上
初始位置 x = 0
速度 v = 0
加速度 a = 1
做直線等加速運動
本次觀測量有位置及速度
其位置觀測誤差的標準差分別為 10 , 1

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
I_a = 100
I_dt = 1
I_total_t = 100


I_observe_sig_x_1 = 0.1
Ay_Z_x_1 = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2) + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_x_1

I_observe_sig_x_2 = 1
Ay_Z_x_2 = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2) + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig_x_2

Ay_Z_x_ans = 0.5*I_a*(np.arange(0,I_total_t,I_dt)**2)

'''
以下2個初始值不太重要  跌代後會收斂
'''
Mt_X = np.matrix([[0,0,0,0,0,0]]).T   # 初始狀態 [位置-1, 速度-1, 加速度-1, 位置-2, 速度-2, 加速度-2]
Mt_P = np.matrix([[1, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1]])   # 狀態協方差矩陣

    
'''
模型設定
Mt_X_(t) = Mt_F*Mt_X(t-1)
'''
Mt_F = np.matrix([[1, I_dt, 0.5*I_dt**2,   0,    0,           0],
                  [0,    1,        I_dt,   0,    0,           0],
                  [0,    0,           1,   0,    0,           0],
                  [0,    0,           0,   1, I_dt, 0.5*I_dt**2],
                  [0,    0,           0,   0,    1,        I_dt],
                  [0,    0,           0,   0,    0,           1]])          # 狀態轉移矩陣
    
Mt_Q = np.matrix([[1, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1]]) # 狀態轉移協方差矩陣 (值越大越不相信公式模組)

'''
觀測相關
Mt_Z = Mt_H*Mt_X
'''
Mt_H = np.matrix([[     1,      0,      0,      0,      0,      0],
                  [     0,      0,      0,      1,      0,      0]])  # 觀測矩陣

Mt_R = np.matrix([[I_observe_sig_x_1,                 0],
                  [                0, I_observe_sig_x_2]])  # 觀測儀器的誤差標準差

Lst_x_1 = []
Lst_x_2 = []
Lst_v_1 = []
Lst_v_2 = []
Lst_a_1 = []
Lst_a_2 = []

for i in range(len(Ay_Z_x_ans)):
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv((Mt_H*Mt_P_*(Mt_H.T) + Mt_R))
    Mt_Z  = np.matrix([[Ay_Z_x_1[i]],
                       [Ay_Z_x_2[i]]])
    Mt_X  = Mt_X_ + Mt_K*( Mt_Z - Mt_H * Mt_X_)
    Mt_P  = (np.eye(6) - Mt_K*Mt_H)*Mt_P_
    Lst_x_1.append(Mt_X[0,0])
    Lst_x_2.append(Mt_X[3,0])  
    Lst_v_1.append(Mt_X[1,0])
    Lst_v_2.append(Mt_X[4,0])
    Lst_a_1.append(Mt_X[2,0])
    Lst_a_2.append(Mt_X[5,0])   
    
    
plt.figure(1)
plt.title('x')
plt.plot(Lst_x_1,color='red')
plt.plot(Ay_Z_x_1,color='red',ls='--')
plt.plot(Lst_x_2,color='blue')
plt.plot(Ay_Z_x_2,color='blue',ls='--')
plt.plot(Ay_Z_x_ans,color='black',ls='--')

plt.figure(2)
plt.title('v')
plt.plot([0,I_total_t/I_dt],[0,I_a*I_total_t],color='black')
plt.plot(Lst_v_1,color='red')
plt.plot(Lst_v_2,color='blue')

plt.figure(3)
plt.title('a')
plt.plot([0,I_total_t/I_dt],[I_a,I_a],color='black')
plt.plot(Lst_a_1,color='red')
plt.plot(Lst_a_2,color='blue')

#plt.scatter(Lst_x_1,Lst_v_1,s=20,c='red')
#plt.scatter(Lst_x_2,Lst_v_2,s=20,c='blue')
#plt.scatter(Ay_Z_x_2,Ay_Z_v_2,s=20,c='green')
#plt.plot(Ay_Z_x_ans,Ay_Z_v_ans,c='red',ls='--')