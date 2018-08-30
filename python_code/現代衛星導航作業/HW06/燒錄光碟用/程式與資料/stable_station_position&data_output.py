# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:43:05 2018

@author: owo

固定站定位 以及 輸出固定站修正量(DGPS用)資料

目前擁有資料固定的參考站資料:
    1. New_GPS_day2.dat
    2. Stationary_all.dat (此檔案已知定位結果差)
兩筆位置真實位置相同
"""

import numpy as np
import xyz2llh
import saastamoinen_model as saamd
import xyz2enu
import get_position
import Satellite_Calculate


### 檔案名稱以及檔案位置 ###
S_event_name = 'New_GPS_day2'

S_rcvr_name = './rcvr_data/rcvr_{0}.dat'.format(S_event_name)
S_eph_name = './eph_data/eph_{0}.dat'.format(S_event_name)

##### 讀取檔案 #####
with open(S_rcvr_name) as f:
    rcbr_all = f.read().split()
    rcbr_all = np.asarray([float(i) for i in rcbr_all]).reshape(int(len(rcbr_all)/6),6)
    
with open(S_eph_name) as f:
    eph_all = f.read().split()
    eph_all = np.asarray([float(i) for i in eph_all]).reshape(int(len(eph_all)/24),24)


##### 讀取 rcbr 中所有出現過的GPSweek 並不重複的排序　###
time_list = list(set(rcbr_all[:,0]))
time_list.sort()

##### 各項空陣列 ######
Ay_pr = np.zeros((len(time_list),32))
Ay_xyz_all = np.zeros((len(time_list),3))
Ay_enu_all = np.zeros((len(time_list),3))
Ay_llh_all = np.zeros((len(time_list),3))
Ay_sate_num = np.zeros((len(time_list),1))
Ay_xk = np.zeros((len(time_list),32))
Ay_yk = np.zeros((len(time_list),32))
Ay_zk = np.zeros((len(time_list),32))
Ay_gpsweektime = np.zeros((len(time_list),1))

List_TDOP = []
List_GDOP = []
List_PDOP = []

###### 真實位置 ######
Ay_ans = np.array([[-2956546.273,5076002.969,2476491.959]])   

for time_chose in range(len(time_list)):
    print("\r atms-free {0:2.2f}%\r".format(time_chose/len(time_list)*100),end='')
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
        
    ### PRN32衛星在 time_chose 7205到7819為壞的
    if time_chose >= 7205 and time_chose <= 7819:
        eph = np.delete(eph,np.where(eph[:,1]==32.),0)
        rcbr = np.delete(rcbr,np.where(rcbr[:,1]==32.),0)
    
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

    
    # 修正地球自轉誤差 #
    (xk,yk,zk) = sate_cal.Earth_rotation_error( xk,yk,zk , rcbr[:,2] )
    
    # 基本資料 # 
    pseudo_range = np.copy(rcbr[:,2])
    Ay_pr[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = pseudo_range
    
    c    = 299792458.0
    af0 = eph[:, 4]
    af1 = eph[:, 5]
    af2 = eph[:, 6]
    toc = eph[:, 2]
    
    # 修正衛星時間誤差 #
    delta_t_sv = sate_cal.get_sate_clock_error(rcbr[:,2],af0,af1,af2,toc,rcbr[:,0])
    pseudo_range += delta_t_sv*c

    
    Ay_xk[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = xk
    Ay_yk[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = yk
    Ay_zk[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = zk    
    
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
    guess_position = get_position.get_position(pseudo_range,guess_range_list,beacon_position,guess_position)[0]
    ##### 定位結束 #####
    
    
    ##### 修正大氣層誤差 #####
    guess_position_llh = np.zeros((3,len(pseudo_range)))
    for i in range(len(pseudo_range)):
        guess_position_llh[:,i] = np.array([xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()])
    enu_resever_sata = xyz2enu.xyz2enu(np.array([xk,yk,zk]).T,guess_position.T).return_enu()
    elevation = np.arctan2( (enu_resever_sata[:,2]),np.sum(enu_resever_sata[:,0:2]**2,1)**0.5 )
    enutropospheric_delay = saamd.init(guess_position_llh[0,:]*np.pi/180.,
                                       guess_position_llh[1,:]*np.pi/180.,
                                       guess_position_llh[2,:],
                                       elevation,
                                       0.6)
    pseudo_range -= enutropospheric_delay

    
    ##### 修正大氣層誤差結束 #####


    ##### 再次定位 #####
    (guess_position,F_colck_b,F_PDOP,F_TDOP,F_GDOP) = get_position.get_position(pseudo_range[np.where(elevation > 0.2618)],
                                                           guess_range_list[np.where(elevation > 0.2618)],
                                                           beacon_position[:,np.where(elevation > 0.2618)[0]],
                                                           guess_position)
    ##### 再次定位結束 #####
    List_PDOP.append(F_PDOP)
    List_TDOP.append(F_TDOP)
    List_GDOP.append(F_GDOP)
    Ay_enu_all[time_chose] = xyz2enu.xyz2enu(guess_position.T,Ay_ans).return_enu()
    Ay_xyz_all[time_chose] = guess_position.T
    xyz2llh_ = xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()
    Ay_llh_all[time_chose] = np.array([[xyz2llh_[0],xyz2llh_[1],xyz2llh_[2]]])
    Ay_sate_num[time_chose] = len(eph)
    Ay_gpsweektime[time_chose] = time_list[time_chose]

#--------- 輸出DGPS修正量資料-------------
(Ay_xk_,Ay_yk_,Ay_zk_) = (Ay_xk,Ay_yk,Ay_zk)
Ay_xk_[np.where(Ay_xk_ != 0.)] -= Ay_ans[0,0]
Ay_yk_[np.where(Ay_yk_ != 0.)] -= Ay_ans[0,1]
Ay_zk_[np.where(Ay_zk_ != 0.)] -= Ay_ans[0,2]
Ay_True_range = np.zeros_like(Ay_xk) + (Ay_xk**2+Ay_yk**2+Ay_zk**2)**0.5 
Ay_pr_Correction = Ay_pr - Ay_True_range

np.save('./stable_data/stable_station_Correction_{0}.npy'.format(S_event_name),Ay_pr_Correction)

#------- 其他資料輸出 ---------
Ay_time = np.zeros((len(time_list),1))
for i in range(len(time_list)):
    Ay_time[i] = time_list[i]

np.save('./stable_data/{0}_llh_all.npy'.format(S_event_name),Ay_llh_all)
np.save('./stable_data/{0}_xyz_all.npy'.format(S_event_name),Ay_xyz_all)
np.save('./stable_data/{0}_enu_all.npy'.format(S_event_name),Ay_enu_all)
np.save('./stable_data/{0}_sate_num.npy'.format(S_event_name),Ay_sate_num)
np.save('./stable_data/{0}_time.npy'.format(S_event_name),Ay_time)
np.save('./stable_data/{0}_DOP.npy'.format(S_event_name),[List_PDOP,List_TDOP,List_GDOP])
np.save('./stable_data/{0}_gpsweek_sec.npy'.format(S_event_name),Ay_gpsweektime)
