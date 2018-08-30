# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:20:16 2018

@author: owo
"""

import numpy as np
import math
import xyz2llh
import xyz2enu
#from scipy import ndimage
from DOY2GPSweek import DOY2GPSweek
from Satellite_Calculate import Satellite_Calculate

global S_phase_data_path
global S_aeosv_data_path
global S_n_data_path
global S_ans_position_path
global F_f1_hz
global F_f2_hz 
global F_err_cbias # code bias error std (m)
global F_std_brdcclk # error of broadcast clock (m)
global F_EFACT_GPS  # error factor: GPS 
global F_ERR_BRDCI  # broadcast iono model error factor
global F_ERR_SAAS
global F_OMGE       # /* earth angular velocity (IS-GPS) (rad/s) */
global F_C

F_err_cbias = 0.3  # code bias error std (m)
F_f1_hz = 1575.42
F_f2_hz = 1227.6
F_std_brdcclk = 30.0 # error of broadcast clock (m)
F_EFACT_GPS = 1.0  # error factor: GPS 
F_ERR_BRDCI = 0.5
F_ERR_SAAS = 0.3   # /* saastamoinen model error std (m) */
F_OMGE = 7.2921151467E-5  # /* earth angular velocity (IS-GPS) (rad/s) */
F_C = 299792458.0

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

def Get_n_data_each_time(I_time_chose,Ay_pr_data,Ay_navigation_data,F_time_chose_sec_total):
    Ay_sate_position_data_all = np.zeros((0,38))
    for I_sate_num in np.where(Ay_pr_data[I_time_chose,:] != 0)[0]+1:
        Ay_n_data_each_sate = Ay_navigation_data[np.where(Ay_navigation_data[:,0]==I_sate_num),:][0]
        F_time_in_sec = Ay_n_data_each_sate[:,4]*60*60 + Ay_n_data_each_sate[:,5]*60 + Ay_n_data_each_sate[:,6]
        try:
            Ay_sate_position_data = Ay_n_data_each_sate[np.where(F_time_in_sec <= F_time_chose_sec_total)[0][-1]:np.where(F_time_in_sec <= F_time_chose_sec_total)[0][-1]+1,:]
        except:
            Ay_sate_position_data = Ay_n_data_each_sate[0:1,:]
        Ay_sate_position_data_all = np.concatenate((Ay_sate_position_data,Ay_sate_position_data_all))
        
    return Ay_sate_position_data_all
        
        
class Error_variance:
    def __init__(self):
        self.F_CCPER = 100.  # code/carrier‐phase error ratio
        self.F_a = 0.003 # carrier‐phase error factor a (m)
        self.F_b = 0.003 # carrier‐phase error factor b (m)
        
    def varerr(self,Ay_elevation,S_ionofree_model_type):
        Ay_varr = F_EFACT_GPS*self.F_CCPER**2*( self.F_a**2 + (self.F_b**2)/np.sin(Ay_elevation))
        if S_ionofree_model_type == 'C1P2':
            Ay_varr *= 3.0**2
        
        return Ay_varr*F_EFACT_GPS
    
    def vare(self,Ay_sva):
        '''
        測試用記得砍
        以下
        '''
#        Ay_sva = np.zeros_like(Ay_sva)  ##### 測試用記得砍  
        '''
        以上
        測試用記得砍
        '''
        Lst_ura_value = [2.4,3.4,4.85,6.85,9.65,13.65,24.0,48.0,96.0,192.0,384.0,768.0,1536.0,3072.0,6144.0]
        Ay_ura = np.zeros_like(Ay_sva)
        for i in range(len(Ay_ura)):
            if Ay_sva[i] < 0 or Ay_sva[i] > 15:
                Ay_ura[i] = 6144.0**2
            else:
                Ay_ura[i] = Lst_ura_value[int(Ay_sva[i])]**2
        return(Ay_ura)
    
    def vmeas(self):
        return 0.3**2  # code bias error std (m)
    
    def vion(self,I_i,S_ionofree_model_type,Ay_ion,S_DGPS):
        if I_i == 0 or S_DGPS != 'No':
            S_ionofree_model_type = 'broadcast'
        if S_ionofree_model_type == 'broadcast':
            Ay_vion = (Ay_ion * F_ERR_BRDCI)**2
            
        elif S_ionofree_model_type == 'C1P2':
            Ay_vion = 0
        
        elif S_ionofree_model_type == 'No':
            Ay_vion = (5.0)**2   ## ERR_ION     5.0         /* ionospheric delay std (m) */
        
        
        return Ay_vion
    
    def vtrp(self,I_i,S_tropospherefree_model_type,Ay_elevation):
        if I_i == 0:
            S_tropospherefree_model_type = 'saastamoinen'
            
        if S_tropospherefree_model_type == 'saastamoinen':
            Ay_vtrp = (F_ERR_SAAS/(np.sin(Ay_elevation)+0.1) )**2
        
        elif S_tropospherefree_model_type == 'No':
            Ay_vtrp = 3.0**2
            
        return Ay_vtrp
    

class Positioning:
    def __init__(self,pseudo_range,guess_range_list,guess_range_list_fix_rot,beacon_position,guess_position,Ay_error_variance_all):
        self.List_clock_fix = []
        self.pseudo_range = pseudo_range
        self.guess_range_list = guess_range_list
        self.beacon_position = beacon_position
        self.guess_position = guess_position
        self.guess_range_list_fix_rot = guess_range_list_fix_rot
        for kk in range(1):
            beacon_location = np.copy(self.beacon_position)
            self.H = np.asmatrix(np.zeros((len(self.guess_range_list),4)))

            for m in range(len(self.guess_range_list)):
#                if m == len(self.guess_range_list)-1:
#                    print(self.guess_position[0,0]-beacon_location[0,m])
                self.H[m,:] = np.matrix([[(self.guess_position[0,0]-beacon_location[0,m])/self.guess_range_list[m],
                                     (self.guess_position[1,0]-beacon_location[1,m])/self.guess_range_list[m],
                                     (self.guess_position[2,0]-beacon_location[2,m])/self.guess_range_list[m],1.]]/(Ay_error_variance_all[m])**0.5 )

            fix_position = np.array(np.linalg.inv(self.H.T*self.H)*self.H.T*  (np.matrix([((self.pseudo_range- self.guess_range_list_fix_rot)/(Ay_error_variance_all)**0.5 ).T]).T) )
            self.guess_position[0:3,0] = self.guess_position[0:3,0] + fix_position[0:3,0]
            
#            print(fix_position)
            
            self.pseudo_range -= fix_position[3,0]

            self.List_clock_fix.append(fix_position[3,0])

        M_HH = np.linalg.inv(self.H.T*self.H)
        self.F_PDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2])**0.5
        self.F_TDOP = (M_HH[3,3])**0.5
        self.F_GDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2]+M_HH[3,3])**0.5
        self.Ay_fix_position = fix_position[0:3,0]
        
        
        
        
    def Positioning_results(self):
        return (self.guess_position,sum(self.List_clock_fix),self.Ay_fix_position,self.F_PDOP,self.F_TDOP,self.F_GDOP)
    
class Error_module:
    def __init__(self):
        pass
    
    def saastamoinen_model(self,lat,lon,alt,elevation,relative_humidity):
        
#        if alt < -100 or alt > 1E4:
#            return 0
        humi = relative_humidity

        temp0 = 15.

        hgt = np.copy(alt)    
        hgt[np.where(alt < 0.)] = 0.
        pres = 1013.25*((1.0 - 2.2557e-5*hgt)**5.2568)
        temp = temp0-(6.5e-3)*hgt+273.16

#        print((17.15*temp-4684.0)/(temp-38.45))
        e = 6.108*humi*np.exp((17.15*temp-4684.0)/(temp-38.45))

#        print(pres[-1],temp[-1],e[-1])
        
        z = math.pi/2.0 - elevation

        trph = 0.0022768*pres/(1.0 - 0.00266*np.cos(2.0*lat*np.pi/180.) - 0.00028*hgt/1000)/np.cos(z)
        trpw = 0.002277*(1255.0/temp + 0.05) * e/np.cos(z)
        return_ans = trph+trpw

        return_ans[np.where((alt < -100.)|(alt > 10000.)|(elevation <= 0.))] = 0.
        return return_ans
    
    def iono_model_broadcast(self,I_year,I_doy,Ay_lat,Ay_lon,Ay_elevation_angle,Ay_enu_resever_sate,F_SPG_time_sec):
        '''
        http://www.navipedia.net/index.php/Klobuchar_Ionospheric_Model
        '''
        
        Ay_iono_broadcast = np.load(S_n_data_path.format(I_year,I_doy)+'n_data_{0:02d}{1:03d}_ion.npy'.format(I_year,I_doy))
        
#        print(Ay_elevation_angle[-1]/math.pi)
        Ay_earth_centred_angle = 0.0137/(Ay_elevation_angle/math.pi+0.11)-0.022
#        print('psi = {0}'.format(Ay_earth_centred_angle[-1]))  
        
        Ay_azimuth = np.arctan2(Ay_enu_resever_sate[:,0], Ay_enu_resever_sate[:,1])
        Ay_azimuth[np.where(Ay_azimuth<0)] += 360.
#        print(Ay_azimuth[-1])

        Ay_IPP_lat = Ay_lat/math.pi+Ay_earth_centred_angle*np.cos(Ay_azimuth)
        Ay_IPP_lat[np.where(Ay_IPP_lat > 0.416)] = 0.416
        Ay_IPP_lat[np.where(Ay_IPP_lat < -0.416)] = -0.416
#        print('phi = {0}'.format(Ay_IPP_lat[-1]))
        
        Ay_IPP_lon = Ay_lon/math.pi + Ay_earth_centred_angle*np.sin(Ay_azimuth)/np.cos(Ay_IPP_lat*math.pi)
#        print('lam = ' + str(Ay_IPP_lon[-1]))
        
        Ay_geomagnetic_lat = Ay_IPP_lat + 0.064*np.cos( (Ay_IPP_lon - 1.617)*math.pi)
#        print('phi_2 = '+str(Ay_geomagnetic_lat[-1]))
        
        Ay_IPP_LT = 43200*Ay_IPP_lon + F_SPG_time_sec
        Ay_IPP_LT[np.where(Ay_IPP_LT >= 86400)] -= 86400
        Ay_IPP_LT[np.where(Ay_IPP_LT < 0)] += 86400
#        print('tt = '+str(Ay_IPP_LT[-1]))
        
        
#        Ay_amplitude_of_ionospheric_delay = np.sum( (np.meshgrid(np.zeros((1,len(Ay_IPP_LT))),Ay_iono_broadcast[0,:])[1])*Ay_geomagnetic_lat,0)
#        Ay_amplitude_of_ionospheric_delay[np.where(Ay_amplitude_of_ionospheric_delay < 0)] = 0
        Ay_amplitude_of_ionospheric_delay = Ay_iono_broadcast[0,0] + Ay_geomagnetic_lat*(Ay_iono_broadcast[0,1]+Ay_geomagnetic_lat*(Ay_iono_broadcast[0,2]+Ay_geomagnetic_lat*Ay_iono_broadcast[0,3]) )
        Ay_amplitude_of_ionospheric_delay[np.where(Ay_amplitude_of_ionospheric_delay < 0)] = 0
#        print('amp = '+str(Ay_amplitude_of_ionospheric_delay[-1]))
        
#        Ay_period_of_ionospheric_delay = np.sum( (np.meshgrid(np.zeros((1,len(Ay_IPP_LT))),Ay_iono_broadcast[1,:])[1])*Ay_geomagnetic_lat,0)
#        Ay_period_of_ionospheric_delay[np.where(Ay_period_of_ionospheric_delay < 72000)] = 72000
        Ay_period_of_ionospheric_delay = Ay_iono_broadcast[1,0] + Ay_geomagnetic_lat*(Ay_iono_broadcast[1,1]+Ay_geomagnetic_lat*(Ay_iono_broadcast[1,2]+Ay_geomagnetic_lat*Ay_iono_broadcast[1,3]) )
        Ay_period_of_ionospheric_delay[np.where(Ay_period_of_ionospheric_delay < 72000)] = 72000
#        print('per = ' + str(Ay_period_of_ionospheric_delay[-1]))
        
        ## Ay_phase_of_ionospheric_delay
        Ay_x = 2*np.pi*(Ay_IPP_LT-50400.)/Ay_period_of_ionospheric_delay ## Ay_phase_of_ionospheric_delay
        
        Ay_slant_factor = 1+16*(0.53-Ay_elevation_angle/math.pi)**3
#        print('f = '+str(Ay_slant_factor[-1]))
        
        Ay_ionospheric_time_delay = np.zeros((len(Ay_IPP_LT)))
#        print('x = '+str(Ay_x[-1]))
#        print(Ay_x)
#        print(Ay_amplitude_of_ionospheric_delay)
#        print(Ay_slant_factor)
        
        for i in range(len(Ay_x)):
            if abs(Ay_x[i]) <= 1.57:
                Ay_ionospheric_time_delay[i] = ((5*10**-9)+Ay_amplitude_of_ionospheric_delay[i]*(1+Ay_x[i]*Ay_x[i]*
                                           (-0.5+Ay_x[i]*Ay_x[i]/24.))  )*Ay_slant_factor[i]*F_C
            else:
                Ay_ionospheric_time_delay[i] = (5*10**-9)*Ay_slant_factor[i]*F_C
#        Ay_ionospheric_time_delay[np.where(abs(Ay_x) <= 1.57)] = ((5*10**-9)+Ay_amplitude_of_ionospheric_delay*(1+Ay_x*Ay_x*
#                                           (-0.5+Ay_x*Ay_x/24.))  )*Ay_slant_factor*F_C

#        Ay_ionospheric_time_delay[np.where(abs(Ay_x) > 1.57)] = (5*10**-9)*Ay_slant_factor*F_C
#        
        return Ay_ionospheric_time_delay

def DGPS_info(I_time_chose,Ay_pr_data_DGPS,Ay_ans_position_DGPS,Ay_time_data_DGPS):
    pass

def ez2do_every_thing(I_year,I_doy,S_station_name,F_elevation_filter=15.,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='No'):

    '''
    讀取測站基本資料
    
    Ay_navigation_data     : 測站 n檔資料
    Ay_pr_data             : 測站 o檔所得 C1 偽距
    Ay_ans_position        : 測站 PPP 定位後位置
    Ay_time_data           : 測站 o檔所得資料點時間
    Ay_time_data_sec       : 測站 Ay_time_data 轉換單位為 秒
    
    '''
    Ay_navigation_data = np.load(S_n_data_path.format(I_year,I_doy)+'n_data_{0:02d}{1:03d}.npy'.format(I_year,I_doy))
    Ay_pr_data = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_station_name))[:,:32]
    Ay_ans_position = np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_station_name))[0,:]
    Ay_time_data = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_year,I_doy,S_station_name))[:,0:6]
    Ay_time_data_sec = Ay_time_data[:,3]*3600.+Ay_time_data[:,4]*60.+Ay_time_data[:,5]

    '''
    若 S_ion_model=='C1P2' (雙頻組合)  則讀取測站 P2 資訊
    
    Ay_P2_data             : 測站 o檔所得 P2 偽距
    
    此處會比對 Ay_P2_data 及 Ay_pr_data
    只留下共同對應擁有的資料
    '''
    if S_ion_model=='C1P2':
       Ay_P2_data = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseP2.npy'.format(I_year,I_doy,S_station_name))[:,:32]
       Ay_P2_data[np.where(Ay_pr_data==0)]=0
       Ay_pr_data[np.where(Ay_P2_data==0)]=0    
    
    
    '''
    若 S_ion_model != 'No' (執行DGPS) 
    
    Ay_pr_data_DGPS        : 基站 o檔所得 C1 偽距
    Ay_ans_position_DGPS   : 基站 PPP 定位後位置
    Ay_time_data_DGPS      : 基站 o檔所得資料點時間
    Ay_time_data_sec_DGPS  : 基站 Ay_time_data_DGPS 轉換單位為 秒
    '''
    if (S_DGPS != 'No' & type(S_DGPS) != list) :
        Ay_pr_data_DGPS = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_DGPS))[:,:32]
        Ay_ans_position_DGPS = np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_DGPS))[0,:]
        Ay_time_data_DGPS = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_year,I_doy,S_DGPS))[:,0:6]
        Ay_time_data_sec_DGPS = Ay_time_data_DGPS[:,3]*3600.+Ay_time_data_DGPS[:,4]*60.+Ay_time_data_DGPS[:,5]
    
    
    if type(S_DGPS) == list:
        List_pr_data_WADGPS = []
        List_ans_position_WADGPS = []
        List_time_data_sec_WADGPS = []
        for I_list in range(len(S_DGPS)):
            List_pr_data_WADGPS.add(np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phaseC1.npy'.format(I_year,I_doy,S_DGPS[I_list]))[:,:32])
            List_ans_position_WADGPS.add(np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,S_DGPS[I_list]))[0,:])
            Ay_time_data_WADGPS = np.load(S_phase_data_path.format(I_year,I_doy)+'30s/'+'{2}{0:02d}{1:03d}phasetime.npy'.format(I_year,I_doy,S_DGPS[I_list]))[:,0:6]
            List_time_data_sec_WADGPS.add(Ay_time_data_WADGPS[:,3]*3600.+Ay_time_data_WADGPS[:,4]*60.+Ay_time_data_WADGPS[:,5])
    
    
    '''
    I_loop_num      : 沒啥特殊 只為後面第一個猜測點不要重設用
    test            : 單站定位後結果 (ENU)
    test_DGPS       : DGPS定位後結果 (ENU)
    ''' 
    I_loop_num = 0
    test = np.zeros((len(Ay_pr_data[:,0]),3))
    test_DGPS = np.zeros((len(Ay_pr_data[:,0]),3))
    
    '''
    進入 單站定位迴圈
    '''
    
    for I_time_chose in range(len(Ay_pr_data[:,0])):
#    for I_time_chose in range(1):
#    for I_time_chose in np.zeros(1).astype('int')+332:
#    for I_time_chose in np.arange(330,340,1):
        try:
            S_info = "\r{0} ,Y:{1:02d} ,D:{2:03d} ,Elevation:{5:2.2f} ,ionofree:{4} ,DGPS:{6} ,now in {3:2.2f}%\r".format(S_station_name,
                        I_year,
                        I_doy,
                        (I_time_chose/float(len(Ay_pr_data[:,0])))*100 
                        ,S_ion_model,
                        F_elevation_filter,
                        S_DGPS)
            print(S_info,end='')

            '''
            最終輸出整理排序後所有有收到的對星之軌道參數
            Ay_sate_position_data_all  (N * 32) N為衛星數
            '''

            '''
            F_time_chose_sec_int     : 接收機時間 整數部分
            F_time_chose_sec_decimal : 接收機時間 小數部分
            F_time_chose_sec_total   : 接收機時間 總和
            '''
            F_time_chose_sec_int = int(Ay_time_data_sec[I_time_chose])
            F_time_chose_sec_decimal = Ay_time_data_sec[I_time_chose]%1
            F_time_chose_sec_total = F_time_chose_sec_int + F_time_chose_sec_decimal

            '''
            Ay_sate_position_data_all     : 用 F_time_chose_sec_total 找尋該時刻有C1資料的衛星最接近的N檔資料
            Ay_sate_chose                 : 該時刻有的衛星編號 (注意是顛倒的喔!!)
            '''
            Ay_sate_position_data_all = Get_n_data_each_time(I_time_chose,Ay_pr_data,Ay_navigation_data,F_time_chose_sec_total)
            Ay_sate_chose = Ay_sate_position_data_all[:,0]
            
            
            '''
            Ay_pseudo_range          : 依時間選取的測站 C1 偽距的房間
            Ay_pseudo_range_P2       : 若 S_ion_model=='C1P2' 依時間選取的測站 P2 偽距的房間
            '''
            
            Ay_pseudo_range = np.zeros(len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0])) 
            if S_ion_model=='C1P2':
                Ay_pseudo_range_P2 = np.zeros(len(np.where(Ay_P2_data[I_time_chose,:] != 0.)[0]))
            
            
            '''
            若同時刻接收衛星數少於4顆(不含4)才定位
            '''
            if len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0]) >= 4:    
                
                '''
                Ay_pseudo_range          : 依時間選取的測站 C1 偽距
                Ay_pseudo_range_P2       : 若 S_ion_model=='C1P2' 依時間選取的測站 P2 偽距
                '''
                for i in range( len(np.where(Ay_pr_data[I_time_chose,:] != 0.)[0]) ):
                    Ay_pseudo_range[i] = Ay_pr_data[I_time_chose,int(Ay_sate_position_data_all[i,0])-1 ] 
                if S_ion_model=='C1P2':
                    for i in range( len(np.where(Ay_P2_data[I_time_chose,:] != 0.)[0]) ):
                        Ay_pseudo_range_P2[i] = Ay_P2_data[I_time_chose,int(Ay_sate_position_data_all[i,0])-1 ] 
            
                '''
                F_gpsweektime_fst       : 該天 GPSWeek (秒)
                Ay_resever_time_delay   : 接收站時鐘誤差量 (m)  (疊代用)
                '''
                F_gpsweektime_fst = (float(DOY2GPSweek(I_year,I_doy))%10)*24*60*60  
                Ay_resever_time_delay = 0
                
                '''
                Mobj_sate_cal           : 計算 測站 衛星相關資料 (Mobj)
                Ay_delta_t_sv           : 衛星時終誤差 (s)   (一開始粗略估計,而後求出精準)
                sva                     : 測站 sva
                tgd                     : 測站 tgd
                Ay_xk,Ay_yk,Ay_zk       : 測站所有衛星位置(m) (ECEF)
                '''
                Mobj_sate_cal = Satellite_Calculate(Ay_sate_position_data_all)
                Ay_delta_t_sv = Mobj_sate_cal.get_sate_clock_error(Ay_pseudo_range,F_time_chose_sec_int,F_time_chose_sec_decimal,F_gpsweektime_fst)
                sva = Mobj_sate_cal.sva
                tgd = Mobj_sate_cal.tgd
                (Ay_xk,Ay_yk,Ay_zk,Ay_delta_t_sv) = Mobj_sate_cal.get_sate_position(
                                                        F_time_chose_sec_int,F_time_chose_sec_decimal,
                                                        F_gpsweektime_fst,Ay_delta_t_sv,Ay_pseudo_range)    
                
#                '''
#                測試用
#                '''
#                (Ay_xk,Ay_yk,Ay_zk) = Mobj_sate_cal.Earth_rotation_error(Ay_xk,Ay_yk,Ay_zk,Ay_pseudo_range)
                
                
                '''
                Mobj_error_variance           : 計算 測站 測量偽距的品質 (Mobj)
                Ay_vare                       : N檔有的訊號品質資訊
                Ay_vmeas                      : 訊號固有品質
                '''
                Mobj_error_variance = Error_variance()
                Ay_vare = Mobj_error_variance.vare(sva)
                Ay_vmeas = Mobj_error_variance.vmeas()
                
                '''
                Ay_guess_position     : 猜測點
                                        一開始訂為 (0.0000000001,0,0) (m)
                                        F_test_point_x 不能為 0 (不然 np.arctan2 算不出來)
                Ay_elevation          : 衛星仰角
                                        一開始都為 90 度
                Ay_enu_resever_sate   : 猜測點與衛星的ENU (算方位角用)
                Ay_fix_position       : 猜測點修正量(m) (x,y,z)
                                        三軸皆小於 1e-4 時停止疊代
                TF_tgd_fix            : 偽距修正 TRG 用
                I_loop_break          : 防止無線定位疊代 LOOP 最大值
                '''
                if I_loop_num == 0:
                    F_test_point_x = 0.000000001
                    F_test_point_y = 0.
                    F_test_point_z = 0.
                    Ay_guess_position = np.array([[F_test_point_x],[F_test_point_y],[F_test_point_z]])
                Ay_elevation = np.zeros(len(Ay_xk)) + np.pi/2
                Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                Ay_fix_position = np.array([100,100,100])
                TF_tgd_fix = True
                I_loop_break = 0
                while abs(Ay_fix_position[0]) > 1e-4 or abs(Ay_fix_position[1]) > 1e-4 or abs(Ay_fix_position[2]) > 1e-4:
                    
                    '''
                    Ay_guess_position_llh     : 猜測點的 llh (度,度,m)
                    '''
                    Ay_guess_position_llh = np.zeros((3,len(Ay_pseudo_range)))
                    for j in range(len(Ay_pseudo_range)):
                        Ay_guess_position_llh[:,j] = np.array([xyz2llh.xyz2llh(Ay_guess_position[0],Ay_guess_position[1],Ay_guess_position[2]).xyz()])
                    
                    '''
                    Ay_varerr       : 衛星系統,衛星訊號造成的品質差異
                    '''
                    Ay_varerr = Mobj_error_variance.varerr(Ay_elevation,S_ion_model)
                    
                    '''
                    Mobj_delay             : 電離層及對流層誤差的 Mobj
                    
                    Ay_dion                : 電離層修正量
                                             若 S_ion_model == 'broadcast' 或是 S_DGPS != 'No' 時
                                             用 broadcast 修正電離層誤差
                                             若 是 "雙頻組合" 則 Ay_dion = 0
                    Ay_vion                : 電離層造成品質差異
                    Ay_dtrp                : 對流層誤差修正量
                                             若 S_trp_model == 'saastamoinen'
                                             使用 saastamoinen model 修正對流層誤差
                    Ay_vtrp                : 對流層造成品質差異       
                    Ay_error_variance_all  : 所有品質影響量總和
                                             Ay_varerr + Ay_vmeas + Ay_vare + Ay_vion + Ay_vtrp
                    '''
                    Mobj_delay = Error_module()
                    if S_ion_model == 'broadcast' or S_DGPS != 'No':
                        Ay_dion = Mobj_delay.iono_model_broadcast(I_year,I_doy,
                                                                  Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                  Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                  Ay_elevation,
                                                                  Ay_enu_resever_sate,
                                                                  F_time_chose_sec_total
                                                                  )
                    else:
                        Ay_dion = 0
                    Ay_vion = Mobj_error_variance.vion(i,S_ion_model,Ay_dion,S_DGPS)
                    if S_trp_model == 'saastamoinen':
                        Ay_dtrp = Mobj_delay.saastamoinen_model(Ay_guess_position_llh[0,:]*np.pi/180.,
                                                                Ay_guess_position_llh[1,:]*np.pi/180.,
                                                                Ay_guess_position_llh[2,:],
                                                                Ay_elevation,
                                                                0.6)
                    else:  
                        Ay_dtrp = 0
                    Ay_vtrp = Mobj_error_variance.vtrp(i,S_trp_model,Ay_elevation)
                    Ay_error_variance_all = Ay_varerr + Ay_vmeas + Ay_vare + Ay_vion + Ay_vtrp 
                    Ay_error_variance_all = np.zeros_like(Ay_error_variance_all)+1

                    '''
                    Ay_beacon_position        : 衛星位置(m) ECEF
                    Ay_guess_range_list_first : 猜測點與衛星 ECEF 差異向量
                    Ay_guess_range_list       : 猜測點與衛星距離(m) 無修正轉動
                    Ay_guess_range_list_      : 猜測點與衛星距離(m) 有修正轉動
                    '''
                    Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
                    Ay_guess_range_list_first = np.copy(Ay_beacon_position)
                    for nn in range(len(Ay_guess_range_list_first[0,:])):
                        Ay_guess_range_list_first[:,nn] -= Ay_guess_position[:,0]
                    Ay_guess_range_list = np.sum((Ay_guess_range_list_first)**2,0)**0.5
                    Ay_guess_range_list_ = np.sum((Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_xk*Ay_guess_position[1]-Ay_yk*Ay_guess_position[0])/F_C
        
#                    '''
#                    測試用
#                    '''
#                    Ay_guess_range_list_ = np.sum((Ay_guess_range_list_first)**2,0)**0.5
        
                    '''
                    修正偽距
                    若"不為" 雙頻組合
                    則以TGD修正
                    反之則使用雙頻組合修正
                    
                    注意!!! 每個時間只會修正一次
                    '''
                    if TF_tgd_fix:
                        F_gamma = F_f1_hz**2/F_f2_hz**2
                        if S_ion_model != 'C1P2':
                            Ay_P1_P2 = (1.0-F_gamma)*tgd*F_C
                            Ay_pseudo_range = Ay_pseudo_range - Ay_P1_P2/(1.0-F_gamma)
#                            print(Ay_pseudo_range[-1])
                        else:
                            Ay_pseudo_range = (F_gamma*Ay_pseudo_range - Ay_pseudo_range_P2)/(F_gamma-1)
                        TF_tgd_fix = False
                    
                    '''
                    Ay_pseudo_range_fix            : 修正所有誤差量後所得的偽距 (就是用他來定位啦)
                    Mobj_get_position_fst          : 定位矩陣(
                                                            Ay_pseudo_range_fix       : 修正所有誤差量後所得的偽距
                                                            Ay_guess_range_list       : 猜測點與衛星距離(m) 無修正轉動
                                                            Ay_guess_range_list_      : 猜測點與衛星距離(m) 有修正轉動
                                                            Ay_beacon_position        : 衛星位置
                                                            Ay_guess_position         : 猜測點
                                                            Ay_error_variance_all     : 品質權重
                                                            )
                    '''
#                    print(Ay_resever_time_delay)
                    Ay_pseudo_range_fix = Ay_pseudo_range + F_C*Ay_delta_t_sv - Ay_resever_time_delay - Ay_dtrp -Ay_dion
                    Mobj_get_position_fst = Positioning(Ay_pseudo_range_fix[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                        Ay_guess_range_list[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                        Ay_guess_range_list_[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                        Ay_beacon_position[:,np.where(Ay_elevation > F_elevation_filter/180*np.pi)[0]],
                                                        Ay_guess_position,
                                                        Ay_error_variance_all[np.where(Ay_elevation > F_elevation_filter/180*np.pi)])
                    
                    '''
                    更新下列數值
                    Ay_guess_position
                    Ay_resever_time_delay
                    Ay_enu_resever_sate
                    Ay_elevation
                    Ay_fix_position
                    '''
                    Ay_guess_position = Mobj_get_position_fst.Positioning_results()[0]
                    Ay_resever_time_delay = Mobj_get_position_fst.Positioning_results()[1] + Ay_resever_time_delay
                    Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                    Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
                    Ay_fix_position = Mobj_get_position_fst.Positioning_results()[2]
                    if I_loop_break > 10:
                        print('test_break')
                        break
                    I_loop_break += 1
                    
                    
                Ay_ENU = xyz2enu.xyz2enu(np.array([Ay_guess_position[:,0]]),
                               np.array([Ay_ans_position])
                               ).return_enu()
                test[I_time_chose] = Ay_ENU[0,:]
#                test[I_time_chose] = Ay_guess_position[:,0]
                
                '''
                做 DPGS 前先用SPP對測站定位一次(使用broadcast,saastamoinen)
                '''
                if S_DGPS != 'No':
                    
                    '''
                    I_DGPS_time_chose_before                     : 尋找靠近測站定位時間最近的基站資料的位置 (只往前找)
                    Ay_sate_position_data_DGPS_before            : 基站選取N檔資料
                    Ay_sate_chose_DGPS_before                    : 基站依時間選取的衛星編號
                    F_time_chose_sec_int_DGPS_before             : 基站資料時間整數部分
                    F_time_chose_sec_decimal_DGPS_before         : 基站資料時間小數部分
                    F_time_chose_sec_total_DGPS_before           : 基站資料時間
                    '''
                    I_DGPS_time_chose_before = np.where(Ay_time_data_sec_DGPS <= F_time_chose_sec_total)[0][-1]
                    F_time_chose_sec_int_DGPS_before = int(Ay_time_data_sec_DGPS[I_DGPS_time_chose_before])
                    F_time_chose_sec_decimal_DGPS_before = Ay_time_data_sec_DGPS[I_DGPS_time_chose_before]%1
#                    F_time_chose_sec_total_DGPS_before = F_time_chose_sec_int_DGPS_before + F_time_chose_sec_decimal_DGPS_before
                    Ay_sate_position_data_DGPS_before = Get_n_data_each_time(
                            I_DGPS_time_chose_before,Ay_pr_data_DGPS,Ay_navigation_data,F_time_chose_sec_total
                            )  
                    Ay_sate_chose_DGPS_before = Ay_sate_position_data_DGPS_before[:,0]
                    
                    '''
                    Mobj_sate_cal_DGPS_before                   : 基站衛星計算 Mobj
                    Ay_delta_t_sv_DGPS_before                   : 基站衛星時鐘誤差
                    Ay_pseudo_range_DGPS_berofe                 : 基站選取的偽距
                    Ay_xk_DGPS_before,Ay_yk_DGPS_before,Ay_zk_DGPS_before
                                                                : 基站衛星位置 ECEF
                    '''
                    Ay_pseudo_range_DGPS_berofe = np.zeros(len(np.where(Ay_pr_data_DGPS[I_DGPS_time_chose_before ,:] != 0.)[0]))
                    for i in range( len(np.where(Ay_pr_data_DGPS[I_DGPS_time_chose_before,:] != 0.)[0]) ):
                        Ay_pseudo_range_DGPS_berofe[i] = Ay_pr_data_DGPS[I_DGPS_time_chose_before,int(Ay_sate_position_data_DGPS_before[i,0])-1 ]
                    Mobj_sate_cal_DGPS_before = Satellite_Calculate(Ay_sate_position_data_DGPS_before)
                    Ay_delta_t_sv_DGPS_before = Mobj_sate_cal_DGPS_before.get_sate_clock_error(Ay_pseudo_range_DGPS_berofe,
                                                                                   F_time_chose_sec_int_DGPS_before,
                                                                                   F_time_chose_sec_decimal_DGPS_before,
                                                                                   F_gpsweektime_fst)
#                    sva_DGPS_before = Mobj_sate_cal_DGPS_before.sva
                    tgd_DGPS_before = Mobj_sate_cal_DGPS_before.tgd
                    (Ay_xk_DGPS_before,Ay_yk_DGPS_before,Ay_zk_DGPS_before,Ay_delta_t_sv_DGPS_before) = Mobj_sate_cal_DGPS_before.get_sate_position(
                                                            F_time_chose_sec_int_DGPS_before,F_time_chose_sec_decimal_DGPS_before,
                                                            F_gpsweektime_fst,Ay_delta_t_sv_DGPS_before,Ay_pseudo_range_DGPS_berofe)

                    '''
                    基站 TGD修正
                    '''

                    Ay_P1_P2_DGPS = (1.0-F_gamma)*tgd_DGPS_before*F_C
                    Ay_pseudo_range_DGPS_berofe = Ay_pseudo_range_DGPS_berofe - Ay_P1_P2_DGPS/(1.0-F_gamma)
#  
                    
                    '''
                    ### 基站衛星位置 ###
                    Ay_beacon_position_DGPS_before(x,y,z)    (3,N)
                    '''
                    Ay_beacon_position_DGPS_before = np.array([Ay_xk_DGPS_before,Ay_yk_DGPS_before,Ay_zk_DGPS_before])
                    
                    '''
                    ### 基站真實距離計算 ###
                    Ay_guess_range_list_DGPS_before   基站"不"考慮旋轉後的真實距離
                    Ay_guess_range_list_DGPS_before_  基站考慮旋轉後的真實距離
                    '''
                    Ay_guess_range_list_DGPS_before_first = np.copy(Ay_beacon_position_DGPS_before)
                    for nn in range(len(Ay_guess_range_list_DGPS_before_first[0,:])):
                        Ay_guess_range_list_DGPS_before_first[:,nn] -= Ay_ans_position_DGPS
#                    Ay_guess_range_list_DGPS_before = np.sum((Ay_guess_range_list_DGPS_before_first)**2,0)**0.5
                    Ay_guess_range_list_DGPS_before_ = np.sum((Ay_guess_range_list_DGPS_before_first)**2,0)**0.5 + F_OMGE*(Ay_xk_DGPS_before*Ay_ans_position_DGPS[1]-Ay_yk_DGPS_before*Ay_ans_position_DGPS[0])/F_C
                        
                    '''
                    基站/測站 衛星配對
                    Ay_sate_match_raver                     : 測站衛星位置碼
                    Ay_pseudo_range_DGPS_chose_rover        : 測站偽距選取
                    Ay_sate_match_base                      : 基站衛星位置碼
                    Ay_pseudo_range_DGPS_chose_base         : 基站偽距選取
                    '''
                    Lst_sate_match = list(set(Ay_sate_chose)&set(Ay_sate_chose_DGPS_before))
                    Ay_sate_match_raver = np.zeros(len(Lst_sate_match)).astype('int')
                    Ay_sate_match_base = np.zeros(len(Lst_sate_match)).astype('int')
                    for I_sate_chose in range(len(Lst_sate_match)):
                        Ay_sate_match_raver[I_sate_chose] = int(np.where(Ay_sate_chose == Lst_sate_match[I_sate_chose])[0])
                        Ay_sate_match_base[I_sate_chose] = int(np.where(Ay_sate_chose_DGPS_before == Lst_sate_match[I_sate_chose])[0])
                    Ay_sate_match_base = Ay_sate_match_base[::-1]
                    Ay_sate_match_raver = Ay_sate_match_raver[::-1]
                    Ay_pseudo_range_DGPS_chose_rover = Ay_pseudo_range[Ay_sate_match_raver[:]]
                    Ay_pseudo_range_DGPS_chose_base = Ay_pseudo_range_DGPS_berofe[Ay_sate_match_base[:]]
                    
                    for i in range(3):

                        Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
                        Ay_guess_range_list_first = np.copy(Ay_beacon_position)
                        for nn in range(len(Ay_guess_range_list_first[0,:])):
                            Ay_guess_range_list_first[:,nn] -= Ay_guess_position[:,0]
                        Ay_guess_range_list = np.sum((Ay_guess_range_list_first)**2,0)**0.5
                        Ay_guess_range_list_ = np.sum((Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_xk*Ay_guess_position[1]-Ay_yk*Ay_guess_position[0])/F_C

                        '''
                        Ay_pseudo_range_fix_DGPS             : 測站修過 DGPS 的偽距
                                                               測站偽距 - ( 基站偽距 - 基站真實距離(修過自轉) ) - 測站時鐘誤差
                                                               
                        Mobj_get_position_DGPS         : 定位矩陣(
                                                                Ay_pseudo_range_fix_DGPS       : 測站修過 DGPS 的偽距
                                                                Ay_guess_range_list            : 猜測點與測站衛星距離(m) 無修正轉動
                                                                Ay_guess_range_list_           : 猜測點與測站衛星距離(m) 有修正轉動
                                                                Ay_beacon_position             : 測站衛星位置
                                                                Ay_guess_position              : 猜測點
                                                                Ay_error_variance_all          : 品質權重
                                                                )
                        '''
                        Ay_pseudo_range_fix_DGPS = Ay_pseudo_range_DGPS_chose_rover - (Ay_pseudo_range_DGPS_chose_base - Ay_guess_range_list_DGPS_before_[Ay_sate_match_base[:]]) - Ay_resever_time_delay

                        Mobj_get_position_DGPS = Positioning(Ay_pseudo_range_fix_DGPS[np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)],
                                        Ay_guess_range_list[Ay_sate_match_raver[:]][np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)],
                                        Ay_guess_range_list_[Ay_sate_match_raver[:]][np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)],
                                        Ay_beacon_position[:,Ay_sate_match_raver[:]][:,np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)[0]],
                                        Ay_guess_position,
                                        Ay_error_variance_all[Ay_sate_match_raver[:]][np.where(Ay_elevation[Ay_sate_match_raver[:]] > F_elevation_filter/180*np.pi)])
                        '''
                        更新下列數值
                        Ay_guess_position
                        Ay_resever_time_delay
                        Ay_enu_resever_sate
                        Ay_elevation
                        '''
                        Ay_guess_position = Mobj_get_position_DGPS.Positioning_results()[0]
                        Ay_resever_time_delay = Mobj_get_position_DGPS.Positioning_results()[1] + Ay_resever_time_delay
                        Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_guess_position.T).return_enu()
                        Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
                        Ay_ENU = xyz2enu.xyz2enu(np.array([Ay_guess_position[:,0]]),
                                       np.array([Ay_ans_position])
                                       ).return_enu()
                        test_DGPS[I_time_chose] = Ay_ENU[0,:]
                        Ay_fix_position = Mobj_get_position_DGPS.Positioning_results()[2]
#                        print(Ay_fix_position)
                        #print(Mobj_get_position_DGPS.Positioning_results()[1])

        except:
            test[I_time_chose] = np.nan
            test_DGPS[I_time_chose] = np.nan
            print('ERROR')
    return test,test_DGPS

        
if __name__ == '__main__':
    I_year = 15
    I_doy = 73

    S_station = 'sun1'
#    test,test_DGPS = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen')
    
    
    test,test_DGPS = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='broadcast',S_trp_model='saastamoinen',S_DGPS='fenp')
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\{1}_sin_{0:03d}_broadcast.npy'.format(I_doy,S_station ),test)
#
#    test = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='No')
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\{1}_sin_{0:03d}_noionfree.npy'.format(I_doy,S_station ),test)
#    
#    test = ez2do_every_thing(I_year,I_doy,S_station,S_ion_model='C1P2')
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\{1}_sin_{0:03d}_C1P2.npy'.format(I_doy,S_station ),test)
#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_broadcast.npy'.format(I_day),test_ENU)
#

#    np.save(r'D:\Ddddd\python\2003\Odata\test\2003324data\sun1_sin_{0:03d}_noionfree.npy'.format(I_day),test_ENU) 