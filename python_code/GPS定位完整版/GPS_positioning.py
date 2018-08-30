# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 17:41:45 2017

@author: owo
"""
import numpy as np
import matplotlib.pyplot as plt 
import xyz2llh
#from scipy.interpolate import interp2d
import xyz2enu
import saastamoinen_model as saamd
import get_position
import GNSS_positioning as Gp
import os
#import llh2xyz

I_year = 15
I_doy = 73
I_rate = 30

List_phase_station_name = []                           
for filenames in os.listdir('./data20{0:02d}{1:03d}/phase_data/{2}s/'.format(I_year,I_doy,I_rate)): 
    if os.path.isfile('./data20{0:02d}{1:03d}/phase_data/{2}s/{3}'.format(I_year,I_doy,I_rate,filenames)):
        if filenames[4:] == '{0:02d}{1:03d}phaseL1.npy'.format(I_year,I_doy):
            List_phase_station_name.append(filenames[0:4])
List_aeosv_station_name = []                           
for filenames in os.listdir('./data20{0:02d}{1:03d}/aeosv_data/{2}s/'.format(I_year,I_doy,I_rate)): 
    if os.path.isfile('./data20{0:02d}{1:03d}/aeosv_data/{2}s/{3}'.format(I_year,I_doy,I_rate,filenames)):
        if filenames[0]=='s' and filenames[5:12]=='{0:03d}.npy'.format(I_doy):
            List_aeosv_station_name.append(filenames[1:5])
List_all_name_list = list(set(List_phase_station_name)&set(List_aeosv_station_name))

### n檔 ###
n_data = np.load(r'./data20{0:02d}{1:03d}/n_data_{0:02d}{1:03d}.npy'.format(I_year,I_doy))
##########
test_1_all = []
test_1_name = []

List_all_name_list = ['aknd']

for S_data_name in List_all_name_list:
    try:
        C1_data_load = np.load(r'./data20{0:02d}{1:03d}/phase_data/{2}s/{3}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,I_rate,S_data_name))[:,:32]
        L1_data_load = np.load(r'./data20{0:02d}{1:03d}/phase_data/{2}s/{3}{0:02d}{1:03d}phaseL1.npy'.format(I_year,I_doy,I_rate,S_data_name))[:,:32]
        
        sTEC_data = np.load(r'./data20{0:02d}{1:03d}/aeosv_data/{2}s/s{3}{1:03d}.npy'.format(I_year,I_doy,I_rate,S_data_name))[:,:32]
        
        C1_data_load[np.where(sTEC_data == 0.)] = 0.
        TEC_range = 40.3/((1575.42*(10**6))**2)*sTEC_data[np.where(C1_data_load!=0.)]*(10**16)
        C1_data_load[np.where(C1_data_load!=0.)] -= TEC_range
        
        
        
        
        position_list = []
        test_1 = []
        
        Ay_position_data_xyz = np.load(r'./data20{0:02d}{1:03d}/position_data/{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_data_name))[0:1,:]
#        Ay_position_data_enu = llh2xyz.llh2xyz(Ay_position_data_llh).return_xyz()
    #    test = np.array([[-2973030.6557],[5076079.2277],[2456681.3751]])
        test = Ay_position_data_xyz.T
        
        #### sp3 #######
        #sp3_data_load = np.load('gbm18355_sp3_data.npy')
        #sp3_time_load = np.load('gbm18355_sp3_time.npy')
        #sp3_fit_navigation_data = np.zeros((4,32,2880))
        #for sata_num in range(len(sp3_data_load[0,:,0])):
        #    for xyzt_chose_num in range(4):
        ##        fit_go = interp2d(np.array([sp3_time_load]),np.array([np.arange(0,2880,1)]),sp3_data_load[:,sata_num,xyzt_chose_num])
        #        fit_go = interp2d(np.arange(len(sp3_data_load[0,:,0])),sp3_time_load,sp3_data_load[:,:,xyzt_chose_num])
        #        sp3_fit_navigation_data[xyzt_chose_num] = fit_go(np.arange(len(sp3_data_load[0,:,0])),np.arange(0,2880,1)*30).T
        #############
        
        
        Ay_end_position_enu = np.zeros((0,3))
        Ay_end_position_llh = np.zeros((0,3))
        gps_week_time_in_o_fst = n_data[0,18]
        xk_array = np.zeros((32,2880))
        yk_array = np.zeros((32,2880))
        zk_array = np.zeros((32,2880))
        pr_array = np.zeros((32,2880))
        
        I_smooth_num = 10
        I_smooth_count = 0
        
        List_PDOP = []
        List_TDOP = []
        List_GDOP = []
        List_colck_b = []
        
        for time_chose in range(10):
#        for time_chose in np.arange(1100,1130,1):
        #### 求衛星位置 sp3檔用###
        #    pseudo_range = C1_data_load[time_chose,np.where(C1_data_load[time_chose,:] != 0)][0]
        #    xk = sp3_fit_navigation_data[0,np.where(C1_data_load[time_chose,:] != 0),time_chose][0].T*1000
        #    yk = sp3_fit_navigation_data[1,np.where(C1_data_load[time_chose,:] != 0),time_chose][0].T*1000
        #    zk = sp3_fit_navigation_data[2,np.where(C1_data_load[time_chose,:] != 0),time_chose][0].T*1000
        #    pseudo_range -= sp3_fit_navigation_data[3,np.where(C1_data_load[time_chose,:] != 0),time_chose][0]*299792.458*(10**-6)
        #    print(sp3_fit_navigation_data[3,np.where(C1_data_load[time_chose,:] != 0),time_chose][0]*299792458.*(10**-6))
        ########################
        ##    
        ### 求衛星位置 n檔用###
            sata_position_data_end = np.zeros((0,38))
            time_chose_sec = time_chose*30.
            for sata_num in np.where(C1_data_load[time_chose,:] != 0)[0]+1:
                n_data_each_sata = n_data[np.where(n_data[:,0] == sata_num),:][0]
                time_in_sec = n_data_each_sata[:,4]*60*60+n_data_each_sata[:,5]*60+n_data_each_sata[:,6]
                try:
                    sata_position_data = n_data_each_sata[np.where(time_in_sec <= time_chose_sec)[0][-1]:np.where(time_in_sec <= time_chose_sec)[0][-1]+1,:]
                except:
    #                print('n data incomplete?')
                    sata_position_data = n_data_each_sata[0:1,:]
                sata_position_data_end = np.concatenate((sata_position_data,sata_position_data_end))
            # 基本資料 # 
            
            pseudo_range = np.zeros(len(np.where(C1_data_load[time_chose,:] != 0.)[0]))
            if len(np.where(C1_data_load[time_chose,:] != 0.)[0]) >= 4:
                for i in range( len(np.where(C1_data_load[time_chose,:] != 0.)[0]) ):
                    pseudo_range[i] = C1_data_load[time_chose,int(sata_position_data_end[i,0])-1 ] 
            
                crs  = sata_position_data_end[:,11]                # (m)
                dn   = sata_position_data_end[:,12]                # (r/s)
                M0   = sata_position_data_end[:,13]                # (s)
                cuc  = sata_position_data_end[:,14]                # (r)
                e    = sata_position_data_end[:,15]                # (-)
                cus  = sata_position_data_end[:,16]                # (r)
                sqrta = sata_position_data_end[:,17]                # (m**0.5)
                toe  = sata_position_data_end[:,18]                # (s)
                cic  = sata_position_data_end[:,19]                # (r)
                omg0 = sata_position_data_end[:,20]                # (r)
                cis  = sata_position_data_end[:,21]                # (r)
                i0   = sata_position_data_end[:,22]                # (r)
                crc  = sata_position_data_end[:,23]                # (m)
                w    = sata_position_data_end[:,24]                # (r)
                odot = sata_position_data_end[:,25]                # (r/s)
                idot = sata_position_data_end[:,26]                # (r/s)
                
                
                # 計算衛星位置 #
                sate_cal = Gp.Satellite_Calculate()
                (xk,yk,zk) = sate_cal.get_sate_position(M0,dn,e,sqrta,i0,omg0,w,odot,idot,
                                                        cuc,cus,crc,crs,cic,cis,toe,
                                                        time_chose_sec + gps_week_time_in_o_fst,pseudo_range)
                
                # 計算衛星位置結束 #
                
                
                # 修正地球自轉影響 #
                (xk,yk,zk) = sate_cal.Earth_rotation_error( xk,yk,zk , pseudo_range )
                # 修正地球自轉影響結束 #
                
                # 修正衛星時間誤差 #
                
                af0 = sata_position_data_end[:,7]
                af1 = sata_position_data_end[:,8]
                af2 = sata_position_data_end[:,9]
                toc = toe
                c    = 299792458.0
                # 修正衛星時間誤差 #
                delta_t_sv = sate_cal.get_sate_clock_error(pseudo_range,af0,af1,af2,toc,time_chose_sec + gps_week_time_in_o_fst)
                pseudo_range += delta_t_sv*c
                # 修正衛星時間誤差結束 #
            
                    
                ### ###
                
                ### 定位 ###
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
                #
                
                ##### 定位 #####
                guess_position = get_position.get_position(pseudo_range,guess_range_list,beacon_position,guess_position)[0]
                ##### 定位結束 #####
            
                ##### 消除大氣誤差 #####
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
                ##### 消除大氣誤差結束 #####
                
                ##### Carrier Smooth Code Measurements #####
                
            #    if I_smooth_count > 10:
            #        
            #    else:
            #        
                    
                
                ##### 再次定位 #####
                (guess_position,F_colck_b,F_PDOP,F_TDOP,F_GDOP) = get_position.get_position(pseudo_range[np.where(elevation>=0.2618)],guess_range_list[np.where(elevation>=0.2618)],
                                                                        beacon_position[:,np.where(elevation>=0.2618)[0]],guess_position)
            #    (guess_position,F_colck_b,F_PDOP,F_TDOP,F_GDOP) = get_position.get_position(pseudo_range,guess_range_list,
            #                                                                                beacon_position,guess_position)
                ##### 再次定位結束 #####
            
                print(np.sum((test - guess_position)**2)**0.5)
                Ay_end_position_enu = np.concatenate((Ay_end_position_enu,xyz2enu.xyz2enu(guess_position.T,test.T).return_enu()))
            #    Ay_end_position_llh = np.concatenate((Ay_end_position_llh,xyz2llh.xyz2llh(guess_position[0],guess_position[1],guess_position[2]).xyz()))
                
            
                List_PDOP.append(F_PDOP)
                List_TDOP.append(F_TDOP)
                List_GDOP.append(F_GDOP)
                List_colck_b.append(F_colck_b)
                test_1.append(np.sum((test - guess_position)**2)**0.5)
                I_smooth_count += 1
    #            xk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = pseudo_range
                xk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = xk
                yk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = yk
                zk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = zk
                pr_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = pseudo_range
                
            else:
                print('not enouge sate')     
                Ay_end_position_enu = np.concatenate((Ay_end_position_enu,np.array([[999,999,999]])))
                List_PDOP.append(999)
                List_TDOP.append(999)
                List_GDOP.append(999)
                List_colck_b.append(999)
                test_1.append(999)
                xk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = 999
                yk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = 999
                zk_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = 999
                pr_array[sata_position_data_end[:,0].astype('int')-1,time_chose] = 999
                
                
                
            test_1_all.append(test_1)
            test_1_name.append(S_data_name)
            
    except:
        print(S_data_name)


###### 最終結果繪圖 #####
#plt.figure(0)
#plt.subplot(4,1,1)
#plt.plot(np.arange(0,24,24/2880.),Ay_end_position_enu[:,0])
#plt.ylabel('m')
#plt.title('E')
#plt.subplot(4,1,2)
#plt.plot(np.arange(0,24,24/2880.),Ay_end_position_enu[:,1])
#plt.ylabel('m')
#plt.title('N')
#plt.subplot(4,1,3)
#plt.plot(np.arange(0,24,24/2880.),Ay_end_position_enu[:,2])
#plt.ylabel('m')
#plt.title('U')
#plt.subplot(4,1,4)
#plt.plot(np.arange(0,24,24/2880.),test_1)
#plt.xlabel('UT')
#
#plt.figure(1)
#plt.plot(np.arange(0,24,24/2880.),List_colck_b)
#plt.xlabel('Sec of Week')
#plt.ylabel('m')
#plt.title('clock bias estimates')