# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:27:43 2017

@author: owo
"""
import numpy as np
import math
import xyz2llh
import xyz2enu

class Positioning:
    def __init__(self,pseudo_range,guess_range_list,beacon_position,guess_position):
        i = 0
        self.List_clock_fix = []
        self.pseudo_range = pseudo_range
        self.guess_range_list = guess_range_list
        self.beacon_position = beacon_position
        self.guess_position = guess_position
        
        while np.sum((self.pseudo_range-self.guess_range_list)**2)**0.5 > 5. and i < 20:
            beacon_location = np.copy(self.beacon_position)
            guess_range_list_first = np.copy(self.beacon_position)
            for nn in range(len(guess_range_list_first[0,:])):
                guess_range_list_first[:,nn] -= self.guess_position[:,0]
            self.guess_range_list = np.sum((guess_range_list_first)**2,0)**0.5
        
            self.H = np.asmatrix(np.zeros((len(self.guess_range_list),4)))
            for m in range(len(self.guess_range_list)):
                self.H[m,:] = np.matrix([[(self.guess_position[0,0]-beacon_location[0,m])/self.guess_range_list[m],
                                     (self.guess_position[1,0]-beacon_location[1,m])/self.guess_range_list[m],
                                     (self.guess_position[2,0]-beacon_location[2,m])/self.guess_range_list[m],1.]])
        
            
            fix_position = np.array(np.linalg.inv(self.H.T*self.H)*self.H.T*  (np.matrix([(self.pseudo_range- self.guess_range_list).T]).T) )
            
            self.guess_position[0:3,0] = self.guess_position[0:3,0] + fix_position[0:3,0]
            
            self.pseudo_range -= fix_position[3,0]
            self.List_clock_fix.append(fix_position[3,0])
            i += 1
        M_HH = np.linalg.inv(self.H.T*self.H)
        self.F_PDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2])**0.5
        self.F_TDOP = (M_HH[3,3])**0.5
        self.F_GDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2]+M_HH[3,3])**0.5

    def Positioning_results(self):
        return (self.guess_position,sum(self.List_clock_fix),self.F_PDOP,self.F_TDOP,self.F_GDOP)
    
class Satellite_Calculate:
    def __init__(self):
        self.F_c    = 299792458.0
        self.F_mu   = 3.986005*(10**14)    #μ    (m**3/s**2)
        self.F_omge = 7.2921151467*(10**-5)    # (r/s)
    
    def get_sate_position(self,Ay_M0,Ay_dn,e,Ay_sqrta,Ay_i0,Ay_omg0,w,Ay_odot,Ay_idot,Ay_cuc,Ay_cus,Ay_crc,Ay_crs,Ay_cic,Ay_cis,Ay_toe,recever_time,pseudo_range):
        self.Ay_sqrta = Ay_sqrta
        self.e = e
        a = self.Ay_sqrta**2                    # (m)
        n0 = (self.F_mu/(a**3))**0.5           # (r/s)
        n = n0 + Ay_dn                     # (r/s)
        Ay_tk = recever_time - Ay_toe - pseudo_range/self.F_c       # (s)

        Ay_tk[np.where(Ay_tk > 302400)] -= 604800
        Ay_tk[np.where(Ay_tk <-302400)] += 604800
        
        Ay_mk = Ay_M0 + n*Ay_tk                  # (s)
        def fun_test(x,sata_num):
            return Ay_mk[sata_num]-(x-self.e[sata_num]*np.sin(x))
        self.Ay_Ek = np.zeros(len(Ay_mk))
        for i in range(len(Ay_mk)):
            test_num = 0
            while abs(fun_test(test_num,i)) > 0.000000000001:
                test_num += fun_test(test_num,i)
            self.Ay_Ek[i] = test_num
            
        Ay_Vk = np.arctan2((((1-self.e**2)**0.5)*np.sin(self.Ay_Ek)/(1-self.e*np.cos(self.Ay_Ek))),((np.cos(self.Ay_Ek)-self.e)/(1-self.e*np.cos(self.Ay_Ek))))
        Ay_PHk = Ay_Vk + w
        Ay_dAy_Uk = Ay_cus*np.sin(2*Ay_PHk)+Ay_cuc*np.cos(2*Ay_PHk)
        Ay_dAy_Rk = Ay_crs*np.sin(2*Ay_PHk)+Ay_crc*np.cos(2*Ay_PHk)
        Ay_dAy_Ik = Ay_cis*np.sin(2*Ay_PHk)+Ay_cic*np.cos(2*Ay_PHk)
        Ay_Uk = Ay_PHk + Ay_dAy_Uk
        
        Ay_Rk = a*(1-self.e*np.cos(self.Ay_Ek))+Ay_dAy_Rk
        Ay_Ik = Ay_i0 + Ay_dAy_Ik + (Ay_idot)*Ay_tk
        
        Ay_xk_ = Ay_Rk*np.cos(Ay_Uk)
        Ay_yk_ = Ay_Rk*np.sin(Ay_Uk)
        
        Ay_omgk = Ay_omg0 + (Ay_odot - self.F_omge)*Ay_tk - self.F_omge*Ay_toe
        
        xk = Ay_xk_*np.cos(Ay_omgk) - Ay_yk_*np.cos(Ay_Ik)*np.sin(Ay_omgk)
        yk = Ay_xk_*np.sin(Ay_omgk) + Ay_yk_*np.cos(Ay_Ik)*np.cos(Ay_omgk)
        zk = Ay_yk_*np.sin(Ay_Ik)

        return (xk,yk,zk)
    
    def get_sate_clock_error(self,pseudo_range,af0,af1,af2,toc,recever_time):
        F = -4.442807633e-10
        t_sv = recever_time - pseudo_range/self.F_c        
        delta_t_sv = ( af0 + af1*(t_sv-toc) + af2*((t_sv-toc)**2) + F*(self.e**self.Ay_sqrta)*np.sin(self.Ay_Ek) )
        
        return delta_t_sv
    
    def Earth_rotation_error(self,xk,yk,zk,pseudo_range):
        sate_position_before_fix = np.array([xk,yk,zk])
        omega = 7.2921151467e-5
        sate_position_after_fix = np.copy(sate_position_before_fix)
        for i in range(len(sate_position_before_fix[0])):
            deltat = pseudo_range[i]/299792458
            theta = omega*deltat
            rotmat = np.matrix([[ np.cos(theta) , np.sin(theta) ,0],
                                [-np.sin(theta) , np.cos(theta) ,0],
                                [0              , 0             ,1]])
            sate_position_after_fix[:,i] = np.asarray(rotmat*(np.asmatrix(sate_position_before_fix[:,i]).T))[:,0]
        return (sate_position_after_fix[0,:],
                sate_position_after_fix[1,:],
                sate_position_after_fix[2,:])
        
class Error_module:
    def __init__(self):
        pass
    
    def saastamoinen_model(self,lat,lon,alt,elevation,relative_humidity):
        humi = relative_humidity

        temp0 = 15.

        hgt = np.copy(alt)    
        hgt[np.where(alt < 0.)] = 0.

        pres = 1013.25*(1.0-(2.2557e-5*hgt)**5.2568)
        temp = temp0-(6.5e-3)*hgt+273.16
        e = 6.108*humi*np.exp((17.15*temp-4684.0)/(temp-38.45))
        z = math.pi/2.0 - elevation
        trph = 0.0022768*pres/(1.0 - 0.00266*np.cos(2.0*lat) - 0.00028*hgt/1000)/np.cos(z)
        trpw = 0.0022768*(1255.0/temp + 0.05) * e/np.cos(z)
        return_ans = trph+trpw
        return_ans[np.where((alt < -100.)|(alt > 10000.)|(elevation <= 0.))] = 0.
        
        return return_ans
    
    def iono_model(self,sTEC,pseudo_range):
        pass
    
class ez2do_every_thing:
    '''
    注意!!!
    測試用 目前只支援30s資料
    '''
    def __init__(self,I_year,I_doy,S_station_name,F_elevation_filter=0.,If_ionofree=True,If_tropospherefree=True):
        import GNSS_positioning as Gp
        
        Ay_navigation_data = np.load('./test_data/n_data_{0:02d}{1:03d}.npy'.format(I_year,I_doy))
        Ay_pr_data = np.load('./test_data/{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_station_name))[:,:32]
        self.Ay_sTEC_data = np.load('./test_data/s{1}{0:03d}.npy'.format(I_doy,S_station_name))[:,:32]
        
        self.Ay_ans_position = np.load('./test_data/{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_station_name))[0,:]
        
        #-------------- 修正sTEC造成之誤差 --------------------
        '''
        在做任何定位前先將TEC誤差量去除(如果已知的話)
        '''
        if If_ionofree:
            Ay_pr_data[np.where(self.Ay_sTEC_data == 0.)] = 0.
            Ay_TEC_range = 40.3/((1575.42*(10**6))**2)*self.Ay_sTEC_data[np.where(Ay_pr_data!=0.)]*(10**16)
            Ay_pr_data[np.where(Ay_pr_data!=0.)] -= Ay_TEC_range
    
        self.Ay_sTEC_data[np.where(self.Ay_sTEC_data==0.)] = np.nan
        #--------------- N檔紀錄gps week time中第一項之時間 ------------
        F_gpsweektime_fst = Ay_navigation_data[0,18]
        
#        self.List_PDOP = []
#        self.List_TDOP = []
#        self.List_GDOP = []
#        self.Ay_ENU  = np.zeros((0,3))
#        self.Ay_position = np.zeros((0,3))
#        self.List_timelist = []
        self.Ay_DOP  = np.zeros((2880,3))
        self.Ay_ENU  = np.zeros((2880,3))
        self.Ay_position = np.zeros((2880,3))
        self.Ay_timelist = np.zeros((2880,1))
        self.Ay_satecount = np.zeros((2880,2))
        
        
        
        for I_time_chose in range(2880):
            S_info = "\r{0} ,Y:{1:02d} ,D:{2:03d} ,Elevation:{5:2.2f} ,ionofree:{4} ,now in {3:2.2f}%\r".format(S_station_name,
                        I_year,
                        I_doy,
                        (I_time_chose/2880.)*100 
                        ,str(If_ionofree),
                        F_elevation_filter)
            print(S_info,end='')
#        for I_time_chose in range(1):
            #----------- 整理出當前時間所有收到的衛星的軌道參數 -----
            '''
            最終輸出整理排序後所有有收到的對星之軌道參數
            Ay_sate_position_data_all  (N * 32) N為衛星數
            '''
            Ay_sate_position_data_all = np.zeros((0,38))
            F_time_chose_sec = I_time_chose*30.
            for I_sate_num in np.where(Ay_pr_data[I_time_chose,:] != 0)[0]+1:
                Ay_n_data_each_sate = Ay_navigation_data[np.where(Ay_navigation_data[:,0]==I_sate_num),:][0]
                F_time_in_sec = Ay_n_data_each_sate[:,4]*60*60 + Ay_n_data_each_sate[:,5]*60 + Ay_n_data_each_sate[:,6]
                try:
                    Ay_sate_position_data = Ay_n_data_each_sate[np.where(F_time_in_sec <= F_time_chose_sec)[0][-1]:np.where(F_time_in_sec <= F_time_chose_sec)[0][-1]+1,:]
                except:
                    Ay_sate_position_data = Ay_n_data_each_sate[0:1,:]
                Ay_sate_position_data_all = np.concatenate((Ay_sate_position_data,Ay_sate_position_data_all))
            self.Ay_timelist[I_time_chose,:] = F_time_chose_sec
    
            Ay_pseudo_range = np.zeros(len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0]))
            self.Ay_satecount[I_time_chose,0] = len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0])
            if len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0]) >= 4:    
                '''
                若同時刻接收衛星數少於4顆(不含4)才定位
                '''
                
                #--------- 整理出當前時間所有收到的衛星的C1偽距 -----
                '''
                最終輸出整理且排序後所有收到的衛星的偽距
                Ay_pseudo_range (N,)  N為衛星數
                '''
                for i in range( len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0]) ):
                    Ay_pseudo_range[i] = Ay_pr_data[I_time_chose,int(Ay_sate_position_data_all[i,0])-1 ] 
                
            
                #-------- 軌道參數 -----------
                crs  = Ay_sate_position_data_all[:,11]                # (m)
                dn   = Ay_sate_position_data_all[:,12]                # (r/s)
                M0   = Ay_sate_position_data_all[:,13]                # (s)
                cuc  = Ay_sate_position_data_all[:,14]                # (r)
                e    = Ay_sate_position_data_all[:,15]                # (-)
                cus  = Ay_sate_position_data_all[:,16]                # (r)
                sqrta = Ay_sate_position_data_all[:,17]                # (m**0.5)
                toe  = Ay_sate_position_data_all[:,18]                # (s)
                cic  = Ay_sate_position_data_all[:,19]                # (r)
                omg0 = Ay_sate_position_data_all[:,20]                # (r)
                cis  = Ay_sate_position_data_all[:,21]                # (r)
                i0   = Ay_sate_position_data_all[:,22]                # (r)
                crc  = Ay_sate_position_data_all[:,23]                # (m)
                w    = Ay_sate_position_data_all[:,24]                # (r)
                odot = Ay_sate_position_data_all[:,25]                # (r/s)
                idot = Ay_sate_position_data_all[:,26]                # (r/s)
                af0  = Ay_sate_position_data_all[:,7]
                af1  = Ay_sate_position_data_all[:,8]
                af2  = Ay_sate_position_data_all[:,9]
                toc  = toe 
                c    = 299792458.0
                
                Mobj_sate_cal = Gp.Satellite_Calculate()
                
                #-------- 利用軌道參數算出粗略衛星位置 -----------
                '''
                (Ay_xk,Ay_yk,Ay_zk) 為各顆有接收到的衛星X Y Z位置且排序
                Ay_xk    (N,)
                Ay_yk    (N,)
                Ay_zk    (N,)
                '''
                (Ay_xk,Ay_yk,Ay_zk) = Mobj_sate_cal.get_sate_position(M0,dn,e,sqrta,i0,omg0,w,odot,idot,
                                                        cuc,cus,crc,crs,cic,cis,toe,
                                                        F_time_chose_sec+F_gpsweektime_fst,Ay_pseudo_range)
                
                #---------- 修正地球自轉造成衛星位置推算誤差 --------------
                '''
                最終輸出整理且排序後所有收到的衛星X Y Z位置且排序並地球自轉造成衛星位置推算誤差
                Ay_xk    (N,)
                Ay_yk    (N,)
                Ay_zk    (N,)
                '''
                (Ay_xk,Ay_yk,Ay_zk) = Mobj_sate_cal.Earth_rotation_error(Ay_xk,Ay_yk,Ay_zk,Ay_pseudo_range)
                
                #-------- 修正衛星時間誤差造成偽距誤差 -----------
                Ay_delta_t_sv = Mobj_sate_cal.get_sate_clock_error(Ay_pseudo_range,af0,af1,af2,toc,F_time_chose_sec+F_gpsweektime_fst)
                Ay_pseudo_range += Ay_delta_t_sv*c
                
                #-------- 創造猜測位置點座標 -------
                F_test_point_x = 0.
                F_test_point_y = 0.
                F_test_point_z = 0.
                Ay_guess_position = np.array([[F_test_point_x],[F_test_point_y],[F_test_point_z]])
                
                #------- 計算猜測點與衛星之距離 -----
                Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
                Ay_guess_range_list_first = np.copy(Ay_beacon_position)
                for nn in range(len(Ay_guess_range_list_first[0,:])):
                    Ay_guess_range_list_first[:,nn] -= Ay_guess_position[:,0]
                Ay_guess_range_list = np.sum((Ay_guess_range_list_first)**2,0)**0.5
                
                #-------- 定位 -----------
                Mobj_get_position_fst = Gp.Positioning(Ay_pseudo_range,Ay_guess_range_list,Ay_beacon_position,Ay_guess_position)
                Ay_guess_position = Mobj_get_position_fst.Positioning_results()[0]
                
                Ay_guess_position_llh = np.zeros((3,len(Ay_pseudo_range)))
                for i in range(len(Ay_pseudo_range)):
                    Ay_guess_position_llh[:,i] = np.array([xyz2llh.xyz2llh(Ay_guess_position[0],Ay_guess_position[1],Ay_guess_position[2]).xyz()])
                Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
                if If_tropospherefree:
                    #-------- 消除大氣誤差 -------
                    Mobj_error_cal = Gp.Error_module()
                    Ay_enutropospheric_delay = Mobj_error_cal.saastamoinen_model(Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                                 Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                                 Ay_guess_position_llh[2,:],
                                                                                 Ay_elevation,
                                                                                 0.6)
                    Ay_pseudo_range -= Ay_enutropospheric_delay
                
                #--------- 再次定位 -------
#                print(np.shape(Ay_pseudo_range[np.where(Ay_elevation>=0.2618)]),
#                      np.shape(Ay_guess_range_list[np.where(Ay_elevation>=0.2618)]),
#                      np.shape(Ay_beacon_position[:,np.where(Ay_elevation>=0.2618)[0]]),np.shape(Ay_elevation))
                F_elevation_filter_2tan = np.tan(F_elevation_filter*np.pi/180)
                self.Ay_satecount[I_time_chose,1] = len(Ay_pseudo_range[np.where(Ay_elevation>=F_elevation_filter_2tan)]) 
                if len(Ay_pseudo_range[np.where(Ay_elevation>=F_elevation_filter_2tan)]) >= 4:
                    self.Mobj_get_position_2nd = Gp.Positioning(Ay_pseudo_range[np.where(Ay_elevation>=F_elevation_filter_2tan)],
                                                                Ay_guess_range_list[np.where(Ay_elevation>=F_elevation_filter_2tan)],
                                                                Ay_beacon_position[:,np.where(Ay_elevation>=F_elevation_filter_2tan)[0]],
                                                                Ay_guess_position)
                    Ay_guess_position = self.Mobj_get_position_2nd.Positioning_results()[0]
                    self.Ay_DOP[I_time_chose,:]  = np.array([[self.Mobj_get_position_2nd.Positioning_results()[2],
                                                              self.Mobj_get_position_2nd.Positioning_results()[3],
                                                              self.Mobj_get_position_2nd.Positioning_results()[4]]])
                    self.Ay_ENU[I_time_chose,:]  = xyz2enu.xyz2enu(np.array([self.Mobj_get_position_2nd.Positioning_results()[0][:,0]]),
                                   np.array([self.Ay_ans_position])
                                   ).return_enu()
                    self.Ay_position[I_time_chose,:] = np.array([self.Mobj_get_position_2nd.Positioning_results()[0][:,0]])
                else:
                    self.Ay_DOP[I_time_chose,:]  = np.zeros((1,3))+np.nan
                    self.Ay_ENU[I_time_chose,:]  = np.zeros((1,3))+np.nan
                    self.Ay_position[I_time_chose,:] = np.zeros((1,3))+np.nan
            else:
                self.Ay_DOP[I_time_chose,:]  = np.zeros((1,3))+np.nan
                self.Ay_ENU[I_time_chose,:]  = np.zeros((1,3))+np.nan
                self.Ay_position[I_time_chose,:] = np.zeros((1,3))+np.nan
                    
#            print(self.Ay_ans_position-Ay_guess_position.T)
    def DOP(self):
        return self.Ay_DOP

    def position(self):
        return self.Ay_position
    
    def PPP_position(self):
        return self.Ay_ans_position
    
    def ENU(self):
        return self.Ay_ENU

    def Time_list(self):
        return self.Ay_timelist
    
    def Sate_tatal_num(self):
        return self.Ay_satecount
    
    def sTEC(self):
        return self.Ay_sTEC_data
if __name__ == '__main__':
    '''
    已下為畫圖用 目前限定使用30s的資料 只有GPS衛星
    EX: 
      python3.5 GNSS_positioning.py 15 73 aknd 15.
    '''
    import GNSS_positioning as Gp
    import matplotlib.pyplot as plt 
    import os
    
    I_year = 15
    I_doy = 72
    S_station_name = 'aknd'
    F_Elevation = 15.
#    TF_ionofree = 1 == 1
    
    test = Gp.ez2do_every_thing(I_year,I_doy,S_station_name,F_Elevation,False)
    Dop = test.DOP()
    Position = test.position()
    Ppp = test.PPP_position()
    Enu = test.ENU()
    Time_list = test.Time_list()
    dp = np.sum(Enu**2,1)**0.5

    test_ionofree = Gp.ez2do_every_thing(I_year,I_doy,S_station_name,F_Elevation)
    Dop_ionofree = test_ionofree.DOP()
    Position_ionofree = test_ionofree.position()
    Ppp_ionofree = test_ionofree.PPP_position()
    Enu_ionofree = test_ionofree.ENU()
    Time_list_ionofree = test_ionofree.Time_list()
    dp_ionofree = np.sum(Enu_ionofree**2,1)**0.5

    test_ionofree_0 = Gp.ez2do_every_thing(I_year,I_doy,S_station_name)
    Dop_ionofree_0 = test_ionofree_0.DOP()
    Position_ionofree_0 = test_ionofree_0.position()
    Ppp_ionofree_0 = test_ionofree_0.PPP_position()
    Enu_ionofree_0 = test_ionofree_0.ENU()
    Time_list_ionofree_0 = test_ionofree_0.Time_list()
    dp_ionofree_0 = np.sum(Enu_ionofree_0**2,1)**0.5
    
    test_notionofree_0 = Gp.ez2do_every_thing(I_year,I_doy,S_station_name,0.,False)
    Dop_notionofree_0 = test_notionofree_0.DOP()
    Position_notionofree_0 = test_notionofree_0.position()
    Ppp_notionofree_0 = test_notionofree_0.PPP_position()
    Enu_notionofree_0 = test_notionofree_0.ENU()
    Time_list_notionofree_0 = test_notionofree_0.Time_list()
    dp_notionofree_0 = np.sum(Enu_notionofree_0**2,1)**0.5       
    
    Sate_tatal_num = test_ionofree.Sate_tatal_num()
    sTEC_data = test_notionofree_0.sTEC()
    
#%%
    S_savefig_path = './test_data/position_fig/'.format(I_year,I_doy,S_station_name)
    if not os.path.isdir(S_savefig_path):
        os.mkdir(S_savefig_path)
    ###
    Fig_0 = plt.figure(0,figsize=(18,10))
    plt.subplot(2,1,1)
    plt.title('20{0:02d} {1:03d} {2}    sTEC'.format(I_year,I_doy,S_station_name))
    for i in range(32):
        plt.plot(Time_list/3600.,sTEC_data[:,i])
    plt.xlim(0,24)
    
    plt.subplot(2,1,2)
    plt.title('20{0:02d} {1:03d} {2}    Sate_num_count'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,Sate_tatal_num,lw=1)
    
    plt.savefig(S_savefig_path+'20{0:02d}{1:03d}{2}SateandTEC.png'.format(I_year,I_doy,S_station_name))
    plt.clf()
    
    ###
    Fig_1 = plt.figure(1,figsize=(18,10))
    plt.subplot(2,1,1)
    plt.title('20{0:02d} {1:03d} {2}    total Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,dp_ionofree,color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,dp_ionofree_0,color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,50)
    plt.subplot(2,1,2)
    plt.plot(Time_list/3600.,dp,color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,dp_notionofree_0,color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,50)
    plt.savefig(S_savefig_path+'20{0:02d}{1:03d}{2}totalPositioningerror.png'.format(I_year,I_doy,S_station_name))
    plt.clf()
    
    ###
    Fig_2 = plt.figure(2,figsize=(18,10))
    plt.subplot(3,2,1)
    plt.title('20{0:02d} {1:03d} {2}    E Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Enu_ionofree[:,0],color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,Enu_ionofree_0[:,0],color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(-30,30)
    
    plt.subplot(3,2,3)
    plt.title('20{0:02d} {1:03d} {2}    N Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Enu_ionofree[:,1],color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,Enu_ionofree_0[:,1],color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(-30,30)
    
    plt.subplot(3,2,5)
    plt.title('20{0:02d} {1:03d} {2}    U Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Enu_ionofree[:,2],color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,Enu_ionofree_0[:,2],color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(-50,50) 
    
    plt.subplot(3,2,2)
    plt.title('20{0:02d} {1:03d} {2}    E Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Enu[:,0],color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,Enu_notionofree_0[:,0],color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(-30,30)
    
    plt.subplot(3,2,4)
    plt.title('20{0:02d} {1:03d} {2}    N Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Enu[:,1],color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,Enu_notionofree_0[:,1],color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(-30,30)
    
    plt.subplot(3,2,6)
    plt.title('20{0:02d} {1:03d} {2}    U Positioning error'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Enu[:,2],color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,Enu_notionofree_0[:,2],color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(-50,50) 
    plt.savefig(S_savefig_path+'20{0:02d}{1:03d}{2}ENUPositioningerror.png'.format(I_year,I_doy,S_station_name))
    plt.clf()
    
    ###
    Fig_3 = plt.figure(3,figsize=(18,10))
    plt.subplot(3,2,1)
    plt.title('20{0:02d} {1:03d} {2}    PDOP'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Dop_ionofree[:,0],color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,Dop_ionofree_0[:,0],color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,10)
    
    plt.subplot(3,2,3)
    plt.title('20{0:02d} {1:03d} {2}    TDOP'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Dop_ionofree[:,1],color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,Dop_ionofree_0[:,1],color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,10)
    
    plt.subplot(3,2,5)
    plt.title('20{0:02d} {1:03d} {2}    GDOP'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Dop_ionofree[:,2],color='pink',label='ionofree',lw=1)
    plt.plot(Time_list/3600.,Dop_ionofree_0[:,2],color='red',label='ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,20) 
    
    plt.subplot(3,2,2)
    plt.title('20{0:02d} {1:03d} {2}    PDOP'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Dop[:,0],color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,Dop_notionofree_0[:,0],color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,10)
    
    plt.subplot(3,2,4)
    plt.title('20{0:02d} {1:03d} {2}    TDOP'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Dop[:,1],color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,Dop_notionofree_0[:,1],color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,10)
    
    plt.subplot(3,2,6)
    plt.title('20{0:02d} {1:03d} {2}    GDOP'.format(I_year,I_doy,S_station_name))
    plt.plot(Time_list/3600.,np.zeros(len(Time_list)),lw=1,color = 'black')
    plt.plot(Time_list/3600.,Dop[:,2],color='gray',label='not ionofree',lw=1)
    plt.plot(Time_list/3600.,Dop_notionofree_0[:,2],color='black',label='not ionofree all Elevation',lw=1)
    plt.legend()
    plt.xlim(0,24)
    plt.ylim(0,20) 
    plt.savefig(S_savefig_path+'20{0:02d}{1:03d}{2}DOPPositioningerror.png'.format(I_year,I_doy,S_station_name))
    plt.clf()