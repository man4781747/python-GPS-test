# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 10:35:21 2017

@author: owo
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import xyz2llh
import saastamoinen_model as saamd
import xyz2enu
import get_position
import Satellite_Calculate
import matplotlib.pyplot as plt 

S_event_name = 'Stationary_all'
#S_event_name = 'move_4'

S_rcvr_name = 'rcvr_{0}.dat'.format(S_event_name)
S_eph_name = 'eph_{0}.dat'.format(S_event_name)

##### 讀取檔案 #####
with open(S_rcvr_name) as f:
    rcbr_all = f.read().split()
    rcbr_all = np.asarray([float(i) for i in rcbr_all]).reshape(int(len(rcbr_all)/6),6)
    
with open(S_eph_name) as f:
    eph_all = f.read().split()
    eph_all = np.asarray([float(i) for i in eph_all]).reshape(int(len(eph_all)/24),24)
##### 讀取檔案結束 #####

##### 答案位置 #####
ans_position = np.array([-2956553.15814963,  5076017.18293241,  2476487.71165772]) # 固定站平均位置
#ans_position = np.array([-2955429.08867763,  5075068.90378863,  2475937.47236121]) # move1平均位置
## move_2 與 move_3在移動 無平均位置


L_enutropospheric_delay = []

time_list = list(set(rcbr_all[:,0]))
time_list.sort()
test_position = []
xk_array = np.zeros((32,len(time_list)))
Ay_enutropospheric_delay = np.zeros((len(time_list),32))+np.nan
Ay_cyclesilp_fix = np.zeros((1,32))
Ay_pr = np.zeros((len(time_list),32))
Ay_xyz_all = np.zeros((len(time_list),3))
Ay_enu_all = np.zeros((len(time_list),3))
Ay_llh_all = np.zeros((len(time_list),3))
Ay_sate_num = np.zeros((len(time_list),1))

List_PDOP = []
List_TDOP = []
List_GDOP = []

for time_chose in range(len(time_list)):
#for time_chose in range(2880):
#for time_chose in np.arange(9900,9950,1):
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

#    ## PRN25衛星在 time_chose 205前為壞的
#    if time_chose <= 205:
#        eph = np.delete(eph,np.where(eph[:,1]==25.),0)
#        rcbr = np.delete(rcbr,np.where(rcbr[:,1]==25.),0)

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
    # 修正衛星時間誤差 #
    delta_t_sv = sate_cal.get_sate_clock_error(rcbr[:,2],af0,af1,af2,toc,rcbr[:,0])
    pseudo_range += delta_t_sv*c
    # 修正衛星時間誤差結束 #
#    Ay_pr[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] += pseudo_range+Ay_cyclesilp_fix[0,(rcbr[:,1]-1).astype('int')]
#    Ay_pr[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] += pseudo_range
    
#    if time_chose!=0:
#        Ay_d_pr = Ay_pr[time_chose,:]-Ay_pr[time_chose-1,:]
#        Ay_cyclesilp_fix[0,np.where(Ay_d_pr > 1000000)] = Ay_d_pr[np.where(Ay_d_pr > 1000000)]
#        Ay_pr[time_chose,:] -= Ay_cyclesilp_fix[0]
#        pseudo_range = Ay_pr[time_chose,np.where(Ay_pr[time_chose,:] >0)][0]
    
    
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
    L_enutropospheric_delay.append(enutropospheric_delay)
#    print(pseudo_range)
    pseudo_range -= enutropospheric_delay
#    test = enutropospheric_delay
#    print(enutropospheric_delay)
    
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
#    print(np.sum((ans_position - guess_position.T)**2)**0.5)

    Ay_enutropospheric_delay[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = pseudo_range
    test_position.append(F_colck_b)
    Ay_enu_all[time_chose] = xyz2enu.xyz2enu(guess_position.T,np.array([ans_position])).return_enu()
    Ay_xyz_all[time_chose] = guess_position.T
    xyz2llh_ = xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()
#    print(xyz2llh_[0],xyz2llh_[1],xyz2llh_[2][0])
    Ay_llh_all[time_chose] = np.array([[xyz2llh_[0],xyz2llh_[1],xyz2llh_[2]]])
    Ay_sate_num[time_chose] = len(eph)
    
Ay_time = np.zeros((len(time_list),1))
for i in range(len(time_list)):
    Ay_time[i] = time_list[i]/60./60-24.+8.

np.save('{0}_atmsfree_llh_all.npy'.format(S_event_name),Ay_llh_all)
np.save('{0}_atmsfree_xyz_all.npy'.format(S_event_name),Ay_xyz_all)
np.save('{0}_atmsfree_enu_all.npy'.format(S_event_name),Ay_enu_all)
np.save('{0}_atmsfree_sate_num.npy'.format(S_event_name),Ay_sate_num)
np.save('{0}_atmsfree_time.npy'.format(S_event_name),Ay_time)
np.save('{0}_atmsfree_DOP.npy'.format(S_event_name),[List_PDOP,List_TDOP,List_GDOP])

plt.figure(1, figsize=(5, 10))
plt.subplot(3,1,1)
plt.plot(Ay_time,List_PDOP,label='atmosfree',lw=1)
#plt.ylim(0,5)
plt.title('move_1 PDOP')
plt.ylabel('m')
plt.subplot(3,1,2)
plt.plot(Ay_time,List_TDOP,label='atmosfree',lw=1)
#plt.ylim(0,5)
plt.title('move_1 TDOP')
plt.ylabel('m')
plt.subplot(3,1,3)
plt.plot(Ay_time,List_GDOP,label='atmosfree',lw=1)
#plt.ylim(0,5)
plt.title('move_1 GDOP')
plt.xlabel('LT')
plt.ylabel('m')

plt.figure(2, figsize=(6, 4))
plt.plot(Ay_time,Ay_sate_num,label='atmosfree',lw=1)
plt.xlabel('LT')
plt.ylabel('num of satellite')
#%%
###########################################################################################
###################不做大氣修正#################################################
###########################################################################################
    ##### 讀取檔案 #####
with open(S_rcvr_name) as f:
    rcbr_all = f.read().split()
    rcbr_all = np.asarray([float(i) for i in rcbr_all]).reshape(int(len(rcbr_all)/6),6)
    
with open(S_eph_name) as f:
    eph_all = f.read().split()
    eph_all = np.asarray([float(i) for i in eph_all]).reshape(int(len(eph_all)/24),24)
##### 讀取檔案結束 #####


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
    
    ### PRN25衛星在 time_chose 205前為壞的
    if time_chose <= 205:
        eph = np.delete(eph,np.where(eph[:,1]==25.),0)
        rcbr = np.delete(rcbr,np.where(rcbr[:,1]==25.),0)

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
    # 修正衛星時間誤差 #
    delta_t_sv = sate_cal.get_sate_clock_error(rcbr[:,2],af0,af1,af2,toc,rcbr[:,0])
    pseudo_range += delta_t_sv*c
    # 修正衛星時間誤差結束 #
    
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

    test_position.append(F_colck_b)
    Ay_enu_all[time_chose] = xyz2enu.xyz2enu(guess_position.T,np.array([ans_position])).return_enu()
    Ay_xyz_all[time_chose] = guess_position.T
    xyz2llh_ = xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()
#    print(xyz2llh_[0],xyz2llh_[1],xyz2llh_[2][0])
    Ay_llh_all[time_chose] = np.array([[xyz2llh_[0],xyz2llh_[1],xyz2llh_[2]]])
    Ay_sate_num[time_chose] = len(eph)
    
Ay_time = np.zeros((len(time_list),1))
for i in range(len(time_list)):
    Ay_time[i] = time_list[i]/60./60-24.+8.

np.save('{0}_notatmsfree_llh_all.npy'.format(S_event_name),Ay_llh_all)
np.save('{0}_notatmsfree_xyz_all.npy'.format(S_event_name),Ay_xyz_all)
np.save('{0}_notatmsfree_enu_all.npy'.format(S_event_name),Ay_enu_all)
np.save('{0}_notatmsfree_sate_num.npy'.format(S_event_name),Ay_sate_num)
np.save('{0}_notatmsfree_time.npy'.format(S_event_name),Ay_time)
np.save('{0}_notatmsfree_DOP.npy'.format(S_event_name),[List_PDOP,List_TDOP,List_GDOP])

plt.figure(1, figsize=(5, 10))
plt.subplot(3,1,1)
plt.plot(Ay_time,List_PDOP,label='not atmosfree',lw=1)
plt.subplot(3,1,2)
plt.plot(Ay_time,List_TDOP,label='not atmosfree',lw=1)
plt.subplot(3,1,3)
plt.plot(Ay_time,List_GDOP,label='not atmosfree',lw=1)

plt.figure(2, figsize=(6, 4))
plt.plot(Ay_time,Ay_sate_num,label='not atmosfree',lw=1)

#%%
###########################################################################################
###################  DPGS修正大氣項   #################################################
###########################################################################################
##### 讀取檔案 #####
with open(S_rcvr_name) as f:
    rcbr_all = f.read().split()
    rcbr_all = np.asarray([float(i) for i in rcbr_all]).reshape(int(len(rcbr_all)/6),6)
    
with open(S_eph_name) as f:
    eph_all = f.read().split()
    eph_all = np.asarray([float(i) for i in eph_all]).reshape(int(len(eph_all)/24),24)
    
Ay_enutropospheric_delay_base = np.load('stable_fix_sata_atm.npy')
Ay_enutropospheric_delay_base[np.where(Ay_enutropospheric_delay_base == 0.)] = np.nan
Ay_time_base = np.load('stable_fix_sata_time.npy')
##### 讀取檔案結束 #####

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
#for time_chose in range(2880):
#for time_chose in np.arange(9950,9970,1):
    print("\r use stable atms-free {0:2.2f}%\r".format(time_chose/len(time_list)*100),end='')
#    print(time_chose)
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
    
    ### PRN25衛星在 time_chose 205前為壞的
    if time_chose <= 205:
        eph = np.delete(eph,np.where(eph[:,1]==25.),0)
        rcbr = np.delete(rcbr,np.where(rcbr[:,1]==25.),0)

    ##### 修正大氣層誤差以基準站 #####
    F_timechose = time_list[time_chose]
    Ay_time_chose = Ay_time_base[np.where((Ay_time_base > F_timechose-1)&(Ay_time_base < 1+F_timechose))[0],:]
    Ay_atmdelay_chose = Ay_enutropospheric_delay_base[np.where((Ay_time_base > F_timechose-1)&(Ay_time_base < 1+F_timechose))[0],:]
    Ay_atmdelay_Fin = Ay_atmdelay_chose[0,:]+(Ay_atmdelay_chose[1,:]-Ay_atmdelay_chose[0,:])*(F_timechose-Ay_time_chose[0]/Ay_time_chose[1]-Ay_time_chose[0])
    for i in range(len(rcbr)):
        rcbr[i,2] -= Ay_atmdelay_Fin[int(rcbr[i,1]-1)]
    eph = eph[np.where(rcbr[:,2] > 0.)]
    rcbr = rcbr[np.where(rcbr[:,2] > 0.)]
    
    if len(eph) >0:
        ##### 修正大氣層誤差結束 #####
        
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
        # 修正衛星時間誤差 #
        delta_t_sv = sate_cal.get_sate_clock_error(rcbr[:,2],af0,af1,af2,toc,rcbr[:,0])
        pseudo_range += delta_t_sv*c
        # 修正衛星時間誤差結束 #
        
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
    #    print(np.sum((ans_position - guess_position.T)**2)**0.5)
    
    #    Ay_enutropospheric_delay[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = enutropospheric_delay
        test_position.append(F_colck_b)
        Ay_enu_all[time_chose] = xyz2enu.xyz2enu(guess_position.T,np.array([ans_position])).return_enu()
        Ay_xyz_all[time_chose] = guess_position.T
        xyz2llh_ = xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()
    #    print(xyz2llh_[0],xyz2llh_[1],xyz2llh_[2][0])
        Ay_llh_all[time_chose] = np.array([[xyz2llh_[0],xyz2llh_[1],xyz2llh_[2]]])
        Ay_sate_num[time_chose] = len(eph)
    else:
        List_PDOP.append(np.nan)
        List_TDOP.append(np.nan)
        List_GDOP.append(np.nan)
    #    print(np.sum((ans_position - guess_position.T)**2)**0.5)
    
    #    Ay_enutropospheric_delay[(np.zeros_like(eph[:,1])+time_chose).astype('int'),(eph[:,1]-1).astype('int')] = enutropospheric_delay
        test_position.append(np.nan)
        Ay_enu_all[time_chose] = np.nan
        Ay_xyz_all[time_chose] = np.nan
        Ay_llh_all[time_chose] = np.nan
        Ay_sate_num[time_chose] = len(eph)
        
        
Ay_time = np.zeros((len(time_list),1))
for i in range(len(time_list)):
    Ay_time[i] = time_list[i]/60./60-24.+8.

np.save('{0}_stableatmsfree_llh_all.npy'.format(S_event_name),Ay_llh_all)
np.save('{0}_stableatmsfree_xyz_all.npy'.format(S_event_name),Ay_xyz_all)
np.save('{0}_stableatmsfree_enu_all.npy'.format(S_event_name),Ay_enu_all)
np.save('{0}_stableatmsfree_sate_num.npy'.format(S_event_name),Ay_sate_num)
np.save('{0}_stableatmsfree_time.npy'.format(S_event_name),Ay_time)
np.save('{0}_stableatmsfree_DOP.npy'.format(S_event_name),[List_PDOP,List_TDOP,List_GDOP])

plt.figure(1, figsize=(5, 10))
plt.subplot(3,1,1)
plt.plot(Ay_time,List_PDOP,label='DGPS',lw=1)
plt.legend()
plt.subplot(3,1,2)
plt.plot(Ay_time,List_TDOP,label='DGPS',lw=1)
#plt.ylim(0,5)
plt.legend()
plt.subplot(3,1,3)
plt.plot(Ay_time,List_GDOP,label='DGPS',lw=1)
#plt.ylim(0,5)
plt.legend()
plt.savefig('move_1_DOP_notatmfree.png',lw=1)

plt.figure(2, figsize=(6, 4))
plt.plot(Ay_time,Ay_sate_num,label='DGPS',lw=1)
plt.legend()
plt.savefig('move_1_num_of_satellite_notatmfree.png')