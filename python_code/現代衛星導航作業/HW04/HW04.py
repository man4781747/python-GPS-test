# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 10:35:21 2017

@author: owo
"""

import numpy as np
import xyz2llh
import get_position
import Satellite_Calculate
import xyz2enu
import saastamoinen_model as saamd

with open('rcvr.dat') as f:
#    test = np.asarray(f.read().split(' \t'))
    rcbr = f.read().split()
#    [print(i) for i in test]
    rcbr = np.asarray([float(i) for i in rcbr]).reshape(11,6)
    
with open('eph.dat') as f:
    eph_fst = f.read().split()
    eph_fst = np.asarray([float(i) for i in eph_fst]).reshape(11,24)
    eph = np.copy(eph_fst)
    for i in range(len(rcbr)):
        eph[i,:] = eph_fst[np.where(eph_fst[:,1]==rcbr[i,1]),:]
        
ans = np.array([-2957014. ,5075859., 2476270.])        

### 衛星軌道推算 ###

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


#c    = 299792458.0
#mu   = 3.986005*(10**14)    #μ    (m**3/s**2)
#omge = 7.2921151467*(10**-5)    # (r/s)
###
#
## 運算過程 #
#a = sqrta**2                    # (m)
#n0 = (mu/(a**3))**0.5           # (r/s)
#n = n0 + dn                     # (r/s)
#tk = rcbr[:,0] - toe - rcbr[:,2]/c       # (s)
#
#mk = M0 + n*tk                  # (s)
#
#
#def fun_test(x,sata_num):
#    return mk[sata_num]-(x-e[sata_num]*np.sin(x))
#Ek = np.zeros(len(mk))
#for i in range(len(mk)):
#    test_num = 0
#    while abs(fun_test(test_num,i)) > 0.000000000001:
#        test_num += fun_test(test_num,i)
#    Ek[i] = test_num
#    
#Vk = np.arctan2((((1-e**2)**0.5)*np.sin(Ek)/(1-e*np.cos(Ek))),((np.cos(Ek)-e)/(1-e*np.cos(Ek))))
#
#PHk = Vk + w
#dUk = cus*np.sin(2*PHk)+cuc*np.cos(2*PHk)
#dRk = crs*np.sin(2*PHk)+crc*np.cos(2*PHk)
#dIk = cis*np.sin(2*PHk)+cic*np.cos(2*PHk)
#Uk = PHk + dUk
#
#Rk = a*(1-e*np.cos(Ek))+dRk
#Ik = i0 + dIk + (idot)*tk
#
#xk_ = Rk*np.cos(Uk)
#yk_ = Rk*np.sin(Uk)
#
#omgk = omg0 + (odot - omge)*tk - omge*toe
#
#xk = xk_*np.cos(omgk) - yk_*np.cos(Ik)*np.sin(omgk)
#yk = xk_*np.sin(omgk) + yk_*np.cos(Ik)*np.cos(omgk)
#zk = yk_*np.sin(Ik)

# 衛星位置運算結束 #

# 修正地球自轉影響 #
(xk,yk,zk) = sate_cal.Earth_rotation_error( xk,yk,zk , rcbr[:,2] )
# 修正地球自轉影響結束 #

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


### 定位 ###
beacon_position = np.array([xk,yk,zk])


position_list_end = np.zeros((0,3))

test_point_x = -2950000.
test_point_y = 5070000.
test_point_z = 2470000.
#test_time = 0.

# ρ-ρ #

guess_position = np.array([[test_point_x],[test_point_y],[test_point_z]])  ##猜測位置

# 計算猜測點距離 #
guess_range_list_first = np.copy(beacon_position)
for nn in range(len(guess_range_list_first[0,:])):
    guess_range_list_first[:,nn] -= guess_position[:,0]
guess_range_list = np.sum((guess_range_list_first)**2,0)**0.5

##


test_position = []
i = 0

#guess_position = get_position.get_position(pseudo_range,guess_range_list,beacon_position,guess_position)

while np.sum((pseudo_range-guess_range_list.T)**2)**0.5 > 10. and i < 10:
#for i in range(100):
#    print(i)
    beacon_location = np.copy(beacon_position)
    guess_range_list_first = np.copy(beacon_position)
    for nn in range(len(guess_range_list_first[0,:])):
        guess_range_list_first[:,nn] -= guess_position[:,0]
    guess_range_list = np.sum((guess_range_list_first)**2,0)**0.5

    H = np.asmatrix(np.zeros((len(guess_range_list),4)))
    for m in range(len(guess_range_list)):
        H[m,:] = np.matrix([[(guess_position[0,0]-beacon_location[0,m])/guess_range_list[m],
                             (guess_position[1,0]-beacon_location[1,m])/guess_range_list[m],
                             (guess_position[2,0]-beacon_location[2,m])/guess_range_list[m],1.]])

    
    fix_position = np.array(np.linalg.inv(H.T*H)*H.T*  (np.matrix([(pseudo_range- guess_range_list).T]).T) )
    
    guess_position[0:3,0] = guess_position[0:3,0] + fix_position[0:3,0]
    
    pseudo_range -= fix_position[3,0]
#        guess_position[3,0] = guess_position[3,0] + fix_position[3,0]
    test_position.append(fix_position[3,0])
    i += 1
    
###### 修正大氣層誤差 #####
#guess_position_llh = np.zeros((3,len(pseudo_range)))
#for i in range(len(pseudo_range)):
#    guess_position_llh[:,i] = np.array([xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()])
#enu_resever_sata = xyz2enu.xyz2enu(np.array([xk,yk,zk]).T,guess_position.T).return_enu()
#elevation = np.arctan2( (enu_resever_sata[:,2]),np.sum(enu_resever_sata[:,0:2]**2,1)**0.5 )
#enutropospheric_delay = saamd.init(guess_position_llh[0,:]*np.pi/180.,
#                                   guess_position_llh[1,:]*np.pi/180.,
#                                   guess_position_llh[2,:],
#                                   elevation,
#                                   0.5)
##L_enutropospheric_delay.append(enutropospheric_delay)
#pseudo_range -= enutropospheric_delay

test_1_tro = (77.6*(10**-6))*43*1013/5./(273+20)*1000
test_2_tro = 0.373*(0.5)*12/5./(273+20)*1000
pseudo_range -= (test_1_tro+test_2_tro)
##### 修正大氣層誤差結束 #####
i = 0

#guess_position = get_position.get_position(pseudo_range,guess_range_list,beacon_position,guess_position)

while np.sum((pseudo_range-guess_range_list.T)**2)**0.5 > 1. and i < 10:
#for i in range(100):
#    print(i)
    beacon_location = np.copy(beacon_position)
    guess_range_list_first = np.copy(beacon_position)
    for nn in range(len(guess_range_list_first[0,:])):
        guess_range_list_first[:,nn] -= guess_position[:,0]
    guess_range_list = np.sum((guess_range_list_first)**2,0)**0.5

    H = np.asmatrix(np.zeros((len(guess_range_list),4)))
    for m in range(len(guess_range_list)):
        H[m,:] = np.matrix([[(guess_position[0,0]-beacon_location[0,m])/guess_range_list[m],
                             (guess_position[1,0]-beacon_location[1,m])/guess_range_list[m],
                             (guess_position[2,0]-beacon_location[2,m])/guess_range_list[m],1.]])

    
    fix_position = np.array(np.linalg.inv(H.T*H)*H.T*  (np.matrix([(pseudo_range- guess_range_list).T]).T) )
    
    guess_position[0:3,0] = guess_position[0:3,0] + fix_position[0:3,0]
    
    pseudo_range -= fix_position[3,0]
#        guess_position[3,0] = guess_position[3,0] + fix_position[3,0]
    test_position.append(fix_position[3,0])
    i += 1

print( np.sum((ans-guess_position.T)**2)**0.5 )