# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:28:55 2018

@author: owo

卡爾曼濾波器測試練習

假設一汽車在直線上
初始位置 x = 0
速度 v = 1
做直線等速運動
本次觀測量只有觀測車車的位置
其觀測誤差的標準差為 1
觀測了 100 秒 
1 秒觀測 1 次


"""
import numpy as np 
import matplotlib.pyplot as plt

I_dt = 1
I_total_t = 60
I_observe_sig = 10
I_v = 0

Ay_Z = np.arange(0,I_total_t,I_dt)*I_v +  + np.random.randn(len(np.arange(0,I_total_t,I_dt)))*I_observe_sig

Ay_Z_ans = np.arange(0,I_total_t,I_dt)*I_v
'''
以下2個初始值不太重要  跌代後會收斂
'''
Mt_X = np.matrix([[0,0]]).T   # 初始狀態 [位置, 速度]
Mt_P = np.matrix([[1, 0],
                  [0 ,1]])   # 狀態協方差矩陣


Mt_F = np.matrix([[1, I_dt],
                  [0, 1]])          # 狀態轉移矩陣
Mt_Q = np.matrix([[0.0001, 0],
                  [0 ,0.0001]])   # 狀態轉移協方差矩陣

Mt_H = np.matrix([[1, 0]])  # 觀測矩陣
I_R = I_observe_sig                   # 觀測儀器的誤差標準差

Lst_test_1 = []
Lst_test_2 = []

for i in range(len(Ay_Z)):
    Mt_X_ = Mt_F*Mt_X
    Mt_P_ = Mt_F*Mt_P*(Mt_F.T) + Mt_Q
    Mt_K  = Mt_P_*(Mt_H.T)*np.linalg.inv((Mt_H*Mt_P_*(Mt_H.T) + I_R))
    Mt_X  = Mt_X_ + Mt_K*( np.matrix([[Ay_Z[i]]]) - Mt_H * Mt_X_)
    Mt_P  = (np.eye(2) - Mt_K*Mt_H)*Mt_P_
    Lst_test_1.append(Mt_X[0,0])
    Lst_test_2.append(Mt_X[1,0])    

plt.scatter(Lst_test_1,Lst_test_2)
#plt.scatter(Lst_test_1,np.arange(0,I_total_t,I_dt)*I_v)
#plt.scatter(1,Ay_Z)