# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:27:43 2017

@author: owo


"""
import numpy as np
import math
import xyz2llh
import xyz2enu
from scipy import ndimage

global S_phase_data_path
global S_aeosv_data_path
global S_n_data_path
global S_ans_position_path

S_phase_data_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/phase_data/'
S_aeosv_data_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/aeosv_data/'
S_n_data_path = '/pub3/man4781747/GPS_data/n_data/'
S_ans_position_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/position_data/'
S_DGPS_Correction_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/DGPS_Correction_data/'
S_GIMRIM_TEC_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/GIM_svTEC/'

S_phase_data_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/phase_data/'
S_aeosv_data_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/aeosv_data/'
S_n_data_path = 'D:/Ddddd/python/2003/Odata/test/n_data/'
S_ans_position_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/position_data/'
S_DGPS_Correction_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/DGPS_Correction_data/'
S_GIMRIM_TEC_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/GIM_svTEC/'


class DGPS:
    def __init__(self,I_year,I_doy):
        self.I_doy = I_doy
        self.I_year = I_year
        
    def Make_DGPS_Correction_Data(self,S_station_name):
        import os
        from DOY2GPSweek import DOY2GPSweek 
        
        if os.path.exists(S_DGPS_Correction_path.format(self.I_year,self.I_doy)) == False:
            os.makedirs(S_DGPS_Correction_path.format(self.I_year,self.I_doy))
        
        Ay_navigation_data = np.load(S_n_data_path.format(self.I_year,self.I_doy)+'n_data_{0:02d}{1:03d}.npy'.format(self.I_year,self.I_doy))
        Ay_pr_data = np.load(S_phase_data_path.format(self.I_year,self.I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(self.I_year,self.I_doy,S_station_name))[:,:32]
        Ay_ans_position = np.load(S_ans_position_path.format(self.I_year,self.I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(self.I_year,self.I_doy,S_station_name))[0,:]
        Ay_time_data = np.load(S_phase_data_path.format(self.I_year,self.I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(self.I_year,self.I_doy,S_station_name))[:,0:6]
        Ay_time_data_sec = Ay_time_data[:,3]*3600.+Ay_time_data[:,4]*60.+Ay_time_data[:,5]
        
        
        
        Ay_DGPS_Correction_all = np.zeros((len(Ay_time_data_sec),32))
        
        F_GPSweek_sec = float(DOY2GPSweek(self.I_year,self.I_doy)[4])*3600*24
#        Ay_time = np.arange(F_GPSweek_sec,F_GPSweek_sec+2880*30,30)
                
        for I_time_chose in range(len(Ay_time_data_sec)):
            S_info = "\r{0} ,Y:{1:02d} ,D:{2:03d} Make_DGPS_Correction_Data ,now in {3:2.2f}%\r".format(S_station_name,
                        self.I_year,
                        self.I_doy,
                        (I_time_chose/2880.)*100 )
            print(S_info,end='')

            #----------- 整理出當前時間所有收到的衛星的軌道參數 -----
            '''
            最終輸出整理排序後所有有收到的對星之軌道參數
            Ay_sate_position_data_all  (N * 32) N為衛星數
            '''
            Ay_sate_position_data_all = np.zeros((0,38))
            F_time_chose_sec = Ay_time_data_sec[I_time_chose]
            for I_sate_num in np.where(Ay_pr_data[I_time_chose,:] != 0)[0]+1:
                Ay_n_data_each_sate = Ay_navigation_data[np.where(Ay_navigation_data[:,0]==I_sate_num),:][0]
                F_time_in_sec = Ay_n_data_each_sate[:,4]*60*60 + Ay_n_data_each_sate[:,5]*60 + Ay_n_data_each_sate[:,6]
                try:
                    Ay_sate_position_data = Ay_n_data_each_sate[np.where(F_time_in_sec <= F_time_chose_sec)[0][-1]:np.where(F_time_in_sec <= F_time_chose_sec)[0][-1]+1,:]
                except:
                    Ay_sate_position_data = Ay_n_data_each_sate[0:1,:]
                Ay_sate_position_data_all = np.concatenate((Ay_sate_position_data,Ay_sate_position_data_all))
            
            Ay_pseudo_range = np.zeros(len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0]))
                
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
        
            Mobj_sate_cal = Satellite_Calculate()   
            (Ay_xk,Ay_yk,Ay_zk) = Mobj_sate_cal.get_sate_position(M0,dn,e,sqrta,i0,omg0,w,odot,idot,
                                                                cuc,cus,crc,crs,cic,cis,toe,
                                                                F_time_chose_sec+F_GPSweek_sec,Ay_pseudo_range)
            #---------- 修正地球自轉造成衛星位置推算誤差 --------------
            '''
            最終輸出整理且排序後所有收到的衛星X Y Z位置且排序並地球自轉造成衛星位置推算誤差
            Ay_xk    (N,)
            Ay_yk    (N,)
            Ay_zk    (N,)
            '''
            (Ay_xk,Ay_yk,Ay_zk) = Mobj_sate_cal.Earth_rotation_error(Ay_xk,Ay_yk,Ay_zk,Ay_pseudo_range)
                
            Ay_Truerange = ((Ay_xk - Ay_ans_position[0])**2+(Ay_yk - Ay_ans_position[1])**2+(Ay_zk - Ay_ans_position[2])**2)**0.5
            
            Ay_DGPS_Correction_all[I_time_chose,(Ay_sate_position_data_all[:,0]-1).astype('int')] = Ay_pseudo_range-Ay_Truerange
        
        Ay_DGPS_output_all = np.zeros((2880,32))
        for i in range(2880):
            if len(Ay_time_data_sec[np.where(Ay_time_data_sec==i*30)]) != 0:
                Ay_DGPS_output_all[i,:] = Ay_DGPS_Correction_all[np.where(Ay_time_data_sec==i*30)[0],:]
                
            elif len(Ay_time_data_sec[np.where(Ay_time_data_sec==i*30)]) == 0:
                if len(np.where(Ay_time_data_sec > i*30)[0]) != 0 and len(np.where(Ay_time_data_sec < i*30)[0]) != 0:
                    t_1 = Ay_DGPS_Correction_all[np.where(Ay_time_data_sec < i*30)[0][-1]]
                    t_2 = Ay_DGPS_Correction_all[np.where(Ay_time_data_sec > i*30)[0][0]]
                    for k in range(32):
                        if t_1[k] != 0 and t_2[k] != 0:
                            Ay_DGPS_output_all[i,k] = t_1[k]+(t_2[k]-t_1[k])*((i*30-Ay_time_data_sec[np.where(Ay_time_data_sec < i*30)[0][-1]])/(Ay_time_data_sec[np.where(Ay_time_data_sec > i*30)[0][0]]-Ay_time_data_sec[np.where(Ay_time_data_sec < i*30)[0][-1]]))
                        elif t_1[k] == 0 and t_2[k] != 0:
#                            Ay_DGPS_output_all[i,k] = t_2[k]
                            Ay_DGPS_output_all[i,k] = 0
                        elif t_1[k] != 0 and t_2[k] == 0:
                            Ay_DGPS_output_all[i,k] = t_1[k]
                elif len(np.where(Ay_time_data_sec > i*30)[0]) == 0:
                    Ay_DGPS_output_all[i,:] = Ay_DGPS_Correction_all[np.where(Ay_time_data_sec < i*30)[0][-1],:]
        np.save(S_DGPS_Correction_path.format(self.I_year,self.I_doy)+'{0}{1:02d}{2:03d}DGPS_Correction_data.npy'.format(S_station_name,self.I_year,self.I_doy),Ay_DGPS_output_all)
        
#    def DGPS_Positioning(self,S_station_name,S_station_name_base):
        
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
        '''
        此為上課版本
        '''

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


#        print(xk)
        return (xk,yk,zk)
    
#        '''
#        此為仿照rtklib版本
#        '''    
#        Ay_tk = recever_time - Ay_toe
#        Ay_M = Ay_M0 + ( (F_mu/((Ay_sqrta)**2)**3 )**0.5 + Ay_dn) * Ay_tk
        
        
    
    def get_sate_clock_error(self,pseudo_range,af0,af1,af2,toc,recever_time):
        '''
        此為原先上課版本
        ''' 
#        F = -4.442807633e-10
#        t_sv = recever_time - pseudo_range/self.F_c        
#        delta_t_sv = ( af0 + af1*(t_sv-toc) + af2*((t_sv-toc)**2) + F*(self.e**self.Ay_sqrta)*np.sin(self.Ay_Ek) )
#        
#        return delta_t_sv
    
        '''
        此為仿照rtklib版本
        '''    
        Ay_t = recever_time - toc
        
        for i in range(2):
            Ay_t -= af0 + af1*Ay_t+af2*(Ay_t**2)
        return af0 + af1*Ay_t+af2*(Ay_t**2)
    
        '''
        結論 兩個好像沒差多少...
        '''
    
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
    
    def iono_model_broadcast(self,I_year,I_doy,Ay_lat,Ay_lon,Ay_elevation_angle,Ay_enu_resever_sate,F_SPG_time_sec):
        '''
        http://www.navipedia.net/index.php/Klobuchar_Ionospheric_Model
        '''
        
        Ay_iono_broadcast = np.load(S_n_data_path.format(I_year,I_doy)+'n_data_{0:02d}{1:03d}_ion.npy'.format(I_year,I_doy))
        
        Ay_earth_centred_angle = 0.0137/(Ay_elevation_angle+0.11)-0.022
        
        Ay_azimuth = np.arctan2(Ay_enu_resever_sate[:,0], Ay_enu_resever_sate[:,1])
        Ay_azimuth[np.where(Ay_azimuth<0)] += 360.
        
        Ay_IPP_lat = Ay_lat+Ay_earth_centred_angle*np.cos(Ay_azimuth)
        Ay_IPP_lat[np.where(Ay_IPP_lat > 0.416)] = 0.416
        Ay_IPP_lat[np.where(Ay_IPP_lat < -0.416)] = -0.416
        
        Ay_IPP_lon = Ay_lon + Ay_earth_centred_angle*np.sin(Ay_azimuth)/np.cos(Ay_IPP_lat)
        
        Ay_geomagnetic_lat = Ay_IPP_lat + 0.064*np.cos(Ay_IPP_lon - 1.617)
        
        Ay_IPP_LT = 43200*Ay_IPP_lon + F_SPG_time_sec
        Ay_IPP_LT[np.where(Ay_IPP_LT >= 86400)] -= 86400
        Ay_IPP_LT[np.where(Ay_IPP_LT < 0)] += 86400
        
        Ay_amplitude_of_ionospheric_delay = np.sum( (np.meshgrid(np.zeros((1,len(Ay_IPP_LT))),Ay_iono_broadcast[0,:])[1])*Ay_geomagnetic_lat,0)
        Ay_amplitude_of_ionospheric_delay[np.where(Ay_amplitude_of_ionospheric_delay < 0)] = 0
        
        Ay_period_of_ionospheric_delay = np.sum( (np.meshgrid(np.zeros((1,len(Ay_IPP_LT))),Ay_iono_broadcast[1,:])[1])*Ay_geomagnetic_lat,0)
        Ay_period_of_ionospheric_delay[np.where(Ay_period_of_ionospheric_delay < 72000)] = 72000
        
        Ay_phase_of_ionospheric_delay = 2*np.pi*(Ay_IPP_LT-50400.)/Ay_period_of_ionospheric_delay
        
        Ay_slant_factor = 1+16*(0.53-Ay_elevation_angle)**3
        
        Ay_ionospheric_time_delay = np.zeros((len(Ay_IPP_LT)))
    

        Ay_ionospheric_time_delay[np.where(abs(Ay_phase_of_ionospheric_delay) <= 1.57)] = ((5*10**-9)+np.sum( (np.meshgrid(np.zeros((1,len(Ay_IPP_LT))),Ay_iono_broadcast[0,:])[1])*Ay_geomagnetic_lat,0)*
                                                                                            (1-Ay_phase_of_ionospheric_delay**2/2+Ay_phase_of_ionospheric_delay**4/24))*Ay_slant_factor

        Ay_ionospheric_time_delay[np.where(abs(Ay_phase_of_ionospheric_delay) > 1.57)] = (5*10**-9)*Ay_slant_factor
        
        return Ay_ionospheric_time_delay
class ez2do_every_thing:
    '''
    注意!!!
    測試用 目前只支援30s資料
    '''
    def __init__(self,I_year,I_doy,S_station_name,F_elevation_filter=0.,If_ionofree=True,S_ionofree_model_type='C1P2',If_tropospherefree=True,S_DGPS='No'):
#        import GNSS_positioning_argv as Gp
        
        Ay_navigation_data = np.load(S_n_data_path.format(I_year,I_doy)+'n_data_{0:02d}{1:03d}.npy'.format(I_year,I_doy))
        Ay_pr_data = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_station_name))[:,:32]
        self.Ay_ans_position = np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_station_name))[0,:]
        Ay_time_data = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_year,I_doy,S_station_name))[:,0:6]
        Ay_time_data_sec = Ay_time_data[:,3]*3600.+Ay_time_data[:,4]*60.+Ay_time_data[:,5]
        
        if S_DGPS != 'No' and type(S_DGPS) != list:
            If_ionofree = False
            If_tropospherefree = False
            Ay_DGPS_Correction_end = np.zeros((len(Ay_time_data_sec),32))
            Ay_DGPS_Correction_Data = np.load(S_DGPS_Correction_path.format(I_year,I_doy)+'{0}{1:02d}{2:03d}DGPS_Correction_data.npy'.format(S_DGPS,I_year,I_doy))
            Ay_time_data_loc = Ay_time_data_sec/30.
            for i in range(len(Ay_time_data_sec)):
                if Ay_time_data_loc[i]%1 == 0:
                    Ay_DGPS_Correction_end[i,:] = Ay_DGPS_Correction_Data[int(Ay_time_data_loc[i]),:]
                else:
                    t_1 = int(Ay_time_data_loc[i])
                    t_2 = int(Ay_time_data_loc[i])+1
                    for j in range(32):
                        if not Ay_DGPS_Correction_Data[t_1,j] == 0 and not Ay_DGPS_Correction_Data[t_2,j] == 0:
                            Ay_DGPS_Correction_end[i,j] = Ay_DGPS_Correction_Data[t_1,j]+(Ay_DGPS_Correction_Data[t_2,j]-Ay_DGPS_Correction_Data[t_1,j])*((Ay_time_data_loc[i]-t_1)/(t_2-t_1))
                        elif Ay_DGPS_Correction_Data[t_1,j] == 0 and not Ay_DGPS_Correction_Data[t_2,j] == 0:
                            Ay_DGPS_Correction_end[i,j] = Ay_DGPS_Correction_Data[t_2,j]
                        elif not Ay_DGPS_Correction_Data[t_1,j] == 0 and Ay_DGPS_Correction_Data[t_2,j] == 0:
                            Ay_DGPS_Correction_end[i,j] = Ay_DGPS_Correction_Data[t_1,j]                 

            Ay_pr_data[np.where(Ay_DGPS_Correction_end == 0.)] = 0.
            Ay_DGPS_Correction_end[np.where(Ay_pr_data == 0.)] = 0.
            Ay_pr_data = Ay_pr_data - Ay_DGPS_Correction_end
            
        elif type(S_DGPS) == list:
            If_ionofree = False
            If_tropospherefree = False
            Ay_all_DGPS_Corr_data = np.zeros((len(S_DGPS),2880,32))
            Ay_range = np.zeros(len(S_DGPS))
            for i in range(len(S_DGPS)):
                Ay_range[i] = 1/(np.sum(np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_DGPS[i]))[0,:]-self.Ay_ans_position)**2)**0.5
#                print(np.shape(np.load(S_DGPS_Correction_path.format(I_year,I_doy)+'{0}{1:02d}{2:03d}DGPS_Correction_data.npy'.format(S_DGPS[i],I_year,I_doy))))
#                print(S_DGPS_Correction_path.format(I_year,I_doy)+'{0}{1:02d}{2:03d}DGPS_Correction_data.npy'.format(S_DGPS[i],I_year,I_doy))
                Ay_all_DGPS_Corr_data[i] = np.load(S_DGPS_Correction_path.format(I_year,I_doy)+'{0}{1:02d}{2:03d}DGPS_Correction_data.npy'.format(S_DGPS[i],I_year,I_doy))
                Ay_all_DGPS_Corr_data[i] *= Ay_range[i]
#            print(np.sum(Ay_range))
            Ay_all_DGPS_Corr_data /= np.sum(Ay_range)
            Ay_all_DGPS_Corr_data[np.where(Ay_all_DGPS_Corr_data==0)]=np.nan
            Ay_all_DGPS_Corr_data_Fin = np.sum(Ay_all_DGPS_Corr_data,0)
            Ay_all_DGPS_Corr_data_Fin[np.isnan(Ay_all_DGPS_Corr_data_Fin)] = 0.
            Ay_pr_data[np.where(Ay_all_DGPS_Corr_data_Fin == 0.)] = 0.
            Ay_all_DGPS_Corr_data_Fin[np.where(Ay_pr_data == 0.)] = 0.
            Ay_pr_data = Ay_pr_data - Ay_all_DGPS_Corr_data_Fin

        #-------------- 修正sTEC造成之誤差 --------------------
        '''
        在做任何定位前先將TEC誤差量去除(如果已知的話)
        '''
        if If_ionofree and S_ionofree_model_type!='broadcast':
            if S_ionofree_model_type != 'C1P2':
                if S_ionofree_model_type=='minyang':
                    print(S_aeosv_data_path.format(I_year,I_doy)+'30s/'+'s{1}{0:03d}.npy'.format(I_doy,S_station_name))
                    self.Ay_sTEC_data = np.load(S_aeosv_data_path.format(I_year,I_doy)+'30s/'+'s{1}{0:03d}.npy'.format(I_doy,S_station_name))[:,:32]
                elif S_ionofree_model_type=='GIM' or S_ionofree_model_type=='RIM':
                    self.Ay_sTEC_data = np.load(S_GIMRIM_TEC_path.format(I_year,I_doy)+'s{0}{1:02d}{2:03d}_{3}.npy'.format(S_station_name,I_year,I_doy,S_ionofree_model_type))
    
                Ay_time_data_loc = Ay_time_data_sec/30.
                Ay_TEC_fit = np.zeros((len(Ay_pr_data),32))
                for i in range(len(Ay_pr_data)):
                    if Ay_time_data_sec[i]%30 == 0:
                        Ay_TEC_fit[i] = self.Ay_sTEC_data[int(Ay_time_data_sec[i]/30),:]
                    else:
                        t_1 = int(Ay_time_data_loc[i])
                        t_2 = int(Ay_time_data_loc[i])+1
                        for j in range(32):
                            if not self.Ay_sTEC_data[t_1,j] == 0 and not self.Ay_sTEC_data[t_2,j] == 0:
                                Ay_TEC_fit[i,j] = self.Ay_sTEC_data[t_1,j]+(self.Ay_sTEC_data[t_2,j]-self.Ay_sTEC_data[t_1,j])*((Ay_time_data_loc[i]-t_1)/(t_2-t_1))
                            elif self.Ay_sTEC_data[t_1,j] == 0 and not self.Ay_sTEC_data[t_2,j] == 0:
                                Ay_TEC_fit[i,j] = self.Ay_sTEC_data[t_2,j]
                            elif not self.Ay_sTEC_data[t_1,j] == 0 and self.Ay_sTEC_data[t_2,j] == 0:
                                Ay_TEC_fit[i,j] = self.Ay_sTEC_data[t_1,j]   
                                
                                
                Ay_pr_data[np.where(Ay_TEC_fit == 0.)] = 0.
                Ay_TEC_range = 40.3/((1575.42*(10**6))**2)*Ay_TEC_fit[np.where(Ay_pr_data!=0.)]*(10**16)
                Ay_pr_data[np.where(Ay_pr_data!=0.)] -= Ay_TEC_range
        
                self.Ay_sTEC_data[np.where(self.Ay_sTEC_data==0.)] = np.nan
            
            elif S_ionofree_model_type == 'C1P2':
                I_f_C1 = 1575.42
                I_f_P2 = 1227.6
                Ay_pr_data_P2 = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseP2.npy'.format(I_year,I_doy,S_station_name))[:,:32]
                Ay_pr_data_C1 = Ay_pr_data
                Ay_pr_data_C1[np.where(Ay_pr_data_P2==0)]=0
                Ay_pr_data_P2[np.where(Ay_pr_data_C1==0)]=0
                Ay_pr_data_C1[np.where(Ay_pr_data_C1==0)]=np.nan
                Ay_pr_data_P2[np.where(Ay_pr_data_P2==0)]=np.nan             
                Ay_pr_data = I_f_C1**2/(I_f_C1**2-I_f_P2**2)*Ay_pr_data_C1 - I_f_P2**2/(I_f_C1**2-I_f_P2**2)*Ay_pr_data_P2
                Ay_pr_data[np.isnan(Ay_pr_data)] = 0
                
        #--------------- N檔紀錄gps week time中第一項之時間 ------------
        F_gpsweektime_fst = Ay_navigation_data[0,18]
        
#        self.List_PDOP = []
#        self.List_TDOP = []
#        self.List_GDOP = []
#        self.Ay_ENU  = np.zeros((0,3))
#        self.Ay_position = np.zeros((0,3))
#        self.List_timelist = []
        self.Ay_DOP  = np.zeros((len(Ay_pr_data[:,0]),3))
        self.Ay_ENU  = np.zeros((len(Ay_pr_data[:,0]),3))
        self.Ay_position = np.zeros((len(Ay_pr_data[:,0]),3))
        self.Ay_timelist = np.zeros((len(Ay_pr_data[:,0]),1))
        self.Ay_satecount = np.zeros((len(Ay_pr_data[:,0]),2))
        
        
        
        for I_time_chose in range(len(Ay_pr_data[:,0])):
#        for I_time_chose in range(1):
            S_info = "\r{0} ,Y:{1:02d} ,D:{2:03d} ,Elevation:{5:2.2f} ,ionofree:{4} ,now in {3:2.2f}%\r".format(S_station_name,
                        I_year,
                        I_doy,
                        (I_time_chose/float(len(Ay_pr_data[:,0])))*100 
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
            F_time_chose_sec = Ay_time_data_sec[I_time_chose]
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
                
                Mobj_sate_cal = Satellite_Calculate()
                
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
#                print(Ay_pseudo_range)
                #---------- 修正地球自轉造成衛星位置推算誤差 --------------
                '''
                最終輸出整理且排序後所有收到的衛星X Y Z位置且排序並地球自轉造成衛星位置推算誤差
                Ay_xk    (N,)
                Ay_yk    (N,)
                Ay_zk    (N,)
                '''
                (Ay_xk,Ay_yk,Ay_zk) = Mobj_sate_cal.Earth_rotation_error(Ay_xk,Ay_yk,Ay_zk,Ay_pseudo_range)
                
                #-------- 修正衛星時間誤差造成偽距誤差 -----------
                if S_DGPS == 'No':
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
                Mobj_get_position_fst = Positioning(Ay_pseudo_range,Ay_guess_range_list,Ay_beacon_position,Ay_guess_position)
                Ay_guess_position = Mobj_get_position_fst.Positioning_results()[0]
                
                Ay_guess_position_llh = np.zeros((3,len(Ay_pseudo_range)))
#                print(Ay_guess_position[0],Ay_guess_position[1],Ay_guess_position[2])
                for i in range(len(Ay_pseudo_range)):
                    Ay_guess_position_llh[:,i] = np.array([xyz2llh.xyz2llh(Ay_guess_position[0],Ay_guess_position[1],Ay_guess_position[2]).xyz()])
                Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
                if If_tropospherefree:
                    #-------- 消除大氣誤差 -------
                    Mobj_error_cal = Error_module()
                    Ay_enutropospheric_delay = Mobj_error_cal.saastamoinen_model(Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                                 Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                                 Ay_guess_position_llh[2,:],
                                                                                 Ay_elevation,
                                                                                 0.6)
                    Ay_pseudo_range -= Ay_enutropospheric_delay
                    
                if S_ionofree_model_type == 'broadcast' and If_ionofree:
                    Mobj_error_cal = Error_module()
                    Ay_ionospheric_time_delay = Mobj_error_cal.iono_model_broadcast(I_year,
                                                                                    I_doy,
                                                                                    Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                                    Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                                    Ay_elevation,
                                                                                    Ay_enu_resever_sate[:,0:2],
                                                                                    F_time_chose_sec+F_gpsweektime_fst
                                                                                    )
#                    print(Ay_ionospheric_time_delay*c)
                    Ay_pseudo_range -= Ay_ionospheric_time_delay*c
                #--------- 再次定位 -------
                F_elevation_filter_2tan = np.tan(F_elevation_filter*np.pi/180)
                self.Ay_satecount[I_time_chose,1] = len(Ay_pseudo_range[np.where(Ay_elevation>=F_elevation_filter_2tan)]) 
                if len(Ay_pseudo_range[np.where(Ay_elevation>=F_elevation_filter_2tan)]) >= 4:
                    self.Mobj_get_position_2nd = Positioning(Ay_pseudo_range[np.where(Ay_elevation>=F_elevation_filter_2tan)],
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
#                    print(Ay_xk)
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
      python3.5 GNSS_positioning_argv.py 15 73 aknd 15.
    '''

####
#  'broadcast'     'C1P2'

    I_year = 15
    I_day = 76
##    print("test = ez2do_every_thing(15,73,'sun1')")
#    test = ez2do_every_thing(I_year,I_day,'sun1',15.,If_ionofree=True,S_ionofree_model_type='C1P2')
#    test_ENU = test.ENU()
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_C1P2.npy'.format(I_day),test_ENU)
#
#    test = ez2do_every_thing(I_year,I_day,'sun1',15.,If_ionofree=True,S_ionofree_model_type='broadcast')
#    test_ENU = test.ENU()
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_broadcast.npy'.format(I_day),test_ENU)
#
#
#    test = ez2do_every_thing(I_year,I_day,'sun1',15.,If_ionofree=False)
#    test_ENU = test.ENU()
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_noionfree.npy'.format(I_day),test_ENU) 

###
    test = ez2do_every_thing(I_year,I_day,'sun1',15.)
    test_ENU = test.ENU()
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\woos_sin_{0:03d}_DGPS.npy'.format(I_day),test_ENU)

######
#    I_day = 77
#    I_year = 15
#    DGPS(I_year,I_day).Make_DGPS_Correction_Data('fenp')
    
