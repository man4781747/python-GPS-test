# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:38:48 2018

@author: owo

觀測站:New_GPS_day2_out ,DGPS固定站: New_GPS_day2
做DGPS後smooth後輸出的資料圖形化用的程式
"""

import numpy as np
import matplotlib.pyplot as plt 

S_data_path = "./New_GPS_day2_out_data/"
Ay_time = np.load(S_data_path+'New_GPS_day2_out_DGPS_time.npy')[:,0]+24
test_no = np.load(S_data_path+'New_GPS_day2_out_DGPS_enu_all_smooth_False_10.npy')
test_5 = np.load(S_data_path+'New_GPS_day2_out_DGPS_enu_all_smooth_True_5.npy')
test_10 = np.load(S_data_path+'New_GPS_day2_out_DGPS_enu_all_smooth_True_10.npy')
test_100 = np.load(S_data_path+'New_GPS_day2_out_DGPS_enu_all_smooth_True_100.npy')
test_1000 = np.load(S_data_path+'New_GPS_day2_out_DGPS_enu_all_smooth_True_1000.npy')
test_2000 = np.load(S_data_path+'New_GPS_day2_out_DGPS_enu_all_smooth_True_2000.npy')

for i in range(3):
    plt.figure(1)
    plt.subplot(3,1,i+1)
    plt.plot(Ay_time,test_no[:,i],lw=1,label='No smooth')
    plt.plot(Ay_time,test_5[:,i],lw=1,label='M=5')
    plt.plot(Ay_time,test_10[:,i],lw=1,label='M=10')
    plt.plot(Ay_time,test_100[:,i],lw=1,label='M=100')
    plt.plot(Ay_time,test_1000[:,i],lw=1,label='M=1000')
    plt.plot(Ay_time,test_2000[:,i],lw=1,label='M=2000')
    plt.ylim(-15,15)
    plt.ylabel('m')
    plt.legend()
    plt.xlim(min(Ay_time),max(Ay_time))
plt.subplot(3,1,1)
plt.title('E,N,U')
plt.subplot(3,1,3)
plt.xlabel('LT')
Ay_not_DGPS = np.load(S_data_path+'New_GPS_day2_out_atmsfree_enu_all.npy')
Ay_not_DGPS_base = np.load('./stable_data/New_GPS_day2_enu_all.npy')


S_data_path = "./New_GPS_day2_out_data/"
Ay_time = np.load(S_data_path+'New_GPS_day2_out_DGPS_time.npy')[:,0]+24
test_no_DOP = np.load(S_data_path+'New_GPS_day2_out_DGPS_DOP_smooth_False_10.npy')
test_5_DOP = np.load(S_data_path+'New_GPS_day2_out_DGPS_DOP_smooth_True_5.npy')
test_10_DOP = np.load(S_data_path+'New_GPS_day2_out_DGPS_DOP_smooth_True_10.npy')
test_100_DOP = np.load(S_data_path+'New_GPS_day2_out_DGPS_DOP_smooth_True_100.npy')
test_1000_DOP = np.load(S_data_path+'New_GPS_day2_out_DGPS_DOP_smooth_True_1000.npy')
test_2000_DOP = np.load(S_data_path+'New_GPS_day2_out_DGPS_DOP_smooth_True_2000.npy')

for i in range(3):
    plt.figure(2)
    plt.subplot(3,1,i+1)
    plt.plot(Ay_time,test_no_DOP[i,:],lw=1,label='No smooth')
    plt.plot(Ay_time,test_5_DOP[i,:],lw=1,label='M=5')
    plt.plot(Ay_time,test_10_DOP[i,:],lw=1,label='M=10')
    plt.plot(Ay_time,test_100_DOP[i,:],lw=1,label='M=100')
    plt.plot(Ay_time,test_1000_DOP[i,:],lw=1,label='M=1000')
    plt.plot(Ay_time,test_2000_DOP[i,:],lw=1,label='M=2000')
    plt.ylabel('m')
    plt.legend()
    plt.xlim(min(Ay_time),max(Ay_time))
plt.subplot(3,1,1)
plt.title('PDOP,TDOP,GDOP')
plt.subplot(3,1,3)
plt.xlabel('LT')
Ay_not_DGPS_DOP = np.load(S_data_path+'New_GPS_day2_out_atmsfree_DOP.npy')
base_time = np.load('./stable_data/New_GPS_day2_time.npy')
Ay_not_DGPS_base_DOP = np.load('./stable_data/New_GPS_day2_DOP.npy')