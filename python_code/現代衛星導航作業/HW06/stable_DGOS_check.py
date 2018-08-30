# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 11:04:34 2018

@author: owo
"""

import numpy as np
import xyz2llh
import saastamoinen_model as saamd
import xyz2enu
import get_position
import os
import Satellite_Calculate
import matplotlib.pyplot as plt 

S_event_name = 'New_base'

S_rcvr_name = './rcvr_data/New_base_rcvr.dat'
S_eph_name = './eph_data/New_base_eph.dat'

S_save_path = './{0}_data/'.format(S_event_name)
if os.path.exists(S_save_path) == False:
    os.makedirs(S_save_path)
    
Ay_ans = np.array([[-2956546.085,5075999.542,2476495.653]])

L_enutropospheric_delay = []

time_list = list(set(rcbr_all[:,0]))
time_list.sort()

Ay_enutropospheric_delay = np.zeros((len(time_list),32))+np.nan
Ay_cyclesilp_fix = np.zeros((1,32))
Ay_pr = np.zeros((len(time_list),32))
Ay_xyz_all = np.zeros((len(time_list),3))
Ay_enu_all = np.zeros((len(time_list),3))
Ay_llh_all = np.zeros((len(time_list),3))
Ay_sate_num = np.zeros((len(time_list),1))
Ay_xk = np.zeros((len(time_list),32))
Ay_yk = np.zeros((len(time_list),32))
Ay_zk = np.zeros((len(time_list),32))

List_PDOP = []
List_TDOP = []
List_GDOP = []
###########################################################################################
###################基準站DGPS檢查#################################################
###########################################################################################
    ##### 讀取檔案 #####
with open(S_rcvr_name) as f:
    rcbr_all = f.read().split()
    rcbr_all = np.asarray([float(i) for i in rcbr_all]).reshape(int(len(rcbr_all)/6),6)
    
with open(S_eph_name) as f:
    eph_all = f.read().split()
    eph_all = np.asarray([float(i) for i in eph_all]).reshape(int(len(eph_all)/24),24)
##### 讀取檔案結束 #####

Ay_Correction_data = np.load('./stable_data/stable_station_Correction.npy')
Ay_Correction_data[Ay_Correction_data==0]=np.nan
Ay_time_base = np.load('./stable_data/Stationary_all_gpsweek_sec.npy')

L_enutropospheric_delay = []
time_list = list(set(rcbr_all[:,0]))
time_list.sort()
#time_list.sort(key=np.ndarray.tolist(rcbr_all[:,0]).index)
test_position = []
xk_array = np.zeros((32,len(time_list)))
Ay_xyz_all = np.zeros((len(time_list),3))
Ay_enu_all = np.zeros((len(time_list),3))
Ay_llh_all = np.zeros((len(time_list),3))
Ay_sate_num = np.zeros((len(time_list),1))
Ay_time = np.zeros((len(time_list),1))

List_PDOP = []
List_TDOP = []
List_GDOP = []

for time_chose in range(len(time_list)):
    print("\r not atms-free {0:2.2f}%\r".format(time_chose/len(time_list)*100),end='')
    rcbr = rcbr_all[np.where((rcbr_all[:,0] == time_list[time_chose])&(rcbr_all[:,1] < 50)) ,:][0]
    eph  = np.zeros((len(rcbr[:,0]),24))
    List_recheck = []
    for i in range(len(rcbr[:,0])):
        eph_sata_each = eph_all[np.where(eph_all[:,1] == rcbr[i,1])]
        if len(eph_sata_each) == 0.:
            List_recheck.append(i)
        else:
            resver_sata_d_time = abs(eph_sata_each[:,0]-rcbr[0,0])
            eph_sata_each_return = eph_sata_each[np.where(resver_sata_d_time == np.min(resver_sata_d_time) ),:][0][0:1,:]
            eph[i] = eph_sata_each_return
    eph = np.delete(eph,List_recheck,0)
    rcbr = np.delete(rcbr,List_recheck,0)  
    
    for i in range(len(rcbr)):
        rcbr[i,2] -= Ay_Correction_data[time_chose,int(rcbr[i,1])-1]
        
    ### PRN32衛星在 time_chose 7205到7819為壞的
    if time_chose >= 7205 and time_chose <= 7819:
        eph = np.delete(eph,np.where(eph[:,1]==32.),0)
        rcbr = np.delete(rcbr,np.where(rcbr[:,1]==32.),0)

    ##### 衛星軌道及時間誤差推算 #####
    
    # 基本資料 # 
    M0   = eph[:,11]    # (s)
    dn   = eph[:,10]                # (r/s)
    e    = eph[:, 8]                 # (-)
    sqrta = eph[:,9]                # (m**0.5)
    i0   = eph[:,14]                # (r)
    omg0 = eph[:,13]                # (r)
    w    = eph[:,12]                # (r)
    odot = eph[:,15]                # (r/s)
    idot = eph[:,16]                # (r/s)
    cuc  = eph[:,18]                # (r)
    cus  = eph[:,17]                # (r)
    crc  = eph[:,22]                # (m)
    crs  = eph[:,21]                # (m)
    cic  = eph[:,20]                # (r)
    cis  = eph[:,19]                # (r)
    toe  = eph[:, 3]                # (s)
    
    # 計算衛星位置 #
    sate_cal = Satellite_Calculate.Satellite_Calculate()
    (xk,yk,zk) = sate_cal.get_sate_position(M0,dn,e,sqrta,i0,omg0,w,odot,idot,
                                            cuc,cus,crc,crs,cic,cis,toe,
                                            rcbr[:,0],rcbr[:,2])

    # 計算衛星位置結束 #
   
    (xk,yk,zk) = sate_cal.Earth_rotation_error( xk,yk,zk , rcbr[:,2] )
    
    # 基本資料 # 
    pseudo_range = np.copy(rcbr[:,2])
    c    = 299792458.0
    af0 = eph[:, 4]
    af1 = eph[:, 5]
    af2 = eph[:, 6]
    toc = eph[:, 2]
##     修正衛星時間誤差 #
#    delta_t_sv = sate_cal.get_sate_clock_error(rcbr[:,2],af0,af1,af2,toc,rcbr[:,0])
#    pseudo_range += delta_t_sv*c
#    # 修正衛星時間誤差結束 #


    ##### 衛星軌道及時間誤差推算結束 #####
    
    beacon_position = np.array([xk,yk,zk])
    
    test_point_x = 0.
    test_point_y = 0.
    test_point_z = 0.
    
    guess_position = np.array([[test_point_x],[test_point_y],[test_point_z]])  ##猜測位置
    
    # 計算猜測點距離 #
    guess_range_list_first = np.copy(beacon_position)
    for nn in range(len(guess_range_list_first[0,:])):
        guess_range_list_first[:,nn] -= guess_position[:,0]
    guess_range_list = np.sum((guess_range_list_first)**2,0)**0.5
    
    ##### 定位 #####
    (guess_position,F_colck_b,F_PDOP,F_TDOP,F_GDOP) = get_position.get_position(pseudo_range,
                                                           guess_range_list,
                                                           beacon_position,
                                                           guess_position)
    ##### 定位結束 #####

    guess_position_llh = np.zeros((3,len(pseudo_range)))
    for i in range(len(pseudo_range)):
        guess_position_llh[:,i] = np.array([xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()])
    enu_resever_sata = xyz2enu.xyz2enu(np.array([xk,yk,zk]).T,guess_position.T).return_enu()
    elevation = np.arctan2( (enu_resever_sata[:,2]),np.sum(enu_resever_sata[:,0:2]**2,1)**0.5 )

    ##### 再次定位 #####
    (guess_position,F_colck_b,F_PDOP,F_TDOP,F_GDOP) = get_position.get_position(pseudo_range[np.where(elevation > 0.2618)],
                                                           guess_range_list[np.where(elevation > 0.2618)],
                                                           beacon_position[:,np.where(elevation > 0.2618)[0]],
                                                           guess_position)
    

    List_PDOP.append(F_PDOP)
    List_TDOP.append(F_TDOP)
    List_GDOP.append(F_GDOP)
    Ay_enu_all[time_chose] = xyz2enu.xyz2enu(guess_position.T,Ay_ans).return_enu()
    Ay_xyz_all[time_chose] = guess_position.T
    xyz2llh_ = xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()
    Ay_llh_all[time_chose] = np.array([[xyz2llh_[0],xyz2llh_[1],xyz2llh_[2]]])
    Ay_sate_num[time_chose] = len(eph)
    
Ay_time = np.zeros((len(time_list),1))
for i in range(len(time_list)):
    Ay_time[i] = time_list[i]/60./60-24.+8.

np.save('{0}{1}_DGPS_check_llh_all.npy'.format(S_save_path,S_event_name),Ay_llh_all)
np.save('{0}{1}_DGPS_check_xyz_all.npy'.format(S_save_path,S_event_name),Ay_xyz_all)
np.save('{0}{1}_DGPS_check_enu_all.npy'.format(S_save_path,S_event_name),Ay_enu_all)
np.save('{0}{1}_DGPS_check_sate_num.npy'.format(S_save_path,S_event_name),Ay_sate_num)
np.save('{0}{1}_DGPS_check_time.npy'.format(S_save_path,S_event_name),Ay_time)
np.save('{0}{1}_DGPS_check_DOP.npy'.format(S_save_path,S_event_name),[List_PDOP,List_TDOP,List_GDOP])
