# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 15:38:54 2018

@author: owo
"""

import sys
sys.path.append(r'./library')

import numpy as np
from ErrorVariance import Error_variance
from DOY2GPSweek import DOY2GPSweek
from Satellite_Calculate import Satellite_Calculate
from LeastSquaresPositioning import Positioning
from ErrorModule import Error_module
from TimeBreakDown import TimeBreakDown
from NDataRead import NDataRead
import xyz2llh
import xyz2enu
from CustomValue import *
class SPPClass:
    def __init__(self):
        pass
    def SPP(self, I_Year, I_Doy, Ay_GuessPosition, F_GPSWeek_Sec, C_Time, Ay_PrC1P2Chose, C_NData, 
        S_ion_model='broadcast', S_trp_model='saastamoinen', F_elevation_filter = 15.):

        '''
        SPP定位
        Input: 
            1. Ay_GuessPosition: 猜測定位點               np.array 3X1
            2. C_Time:           資料當前的時間            TimeBreakDown的物件 Class
    ####        3. Ay_AnsPosition:   測站正確位置              np.array 1X3
            4. Ay_PrC1P2Chose:     資料當前所有GPS衛星的C1與P2數值 np.array 2X32
                Ay_PrC1P2Chose[0]: C1
                Ay_PrC1P2Chose[1]: P2
            5. C_NData:          資料當天的NData           NDataRead物件  Class
            6. S_ion_model:      欲使用的電離層模組(預設broadcast)   String
            7. S_trp_model:      欲使用的大氣模組(預設saastamoinen)  String
            8. F_elevation_filter: 衛星最低仰角限制(預設15度)        Float 
        
        Output:
            1. SPP計算後位置(xyz)   np.array 3X1
        '''
        S_DGPS = 'No'
        if S_ion_model=='IONFREE':
            Ay_PrC1P2Chose[0][np.where(Ay_PrC1P2Chose[1] == 0)] = 0
            Ay_PrC1P2Chose[1][np.where(Ay_PrC1P2Chose[0] == 0)] = 0
            
        
        Ay_NDataChose, Ay_SateChoseNum = C_NData.GetData(Ay_PrC1P2Chose[0], C_Time.F_TimeTotal)
        Ay_PrC1SateChose = Ay_PrC1P2Chose[0, Ay_SateChoseNum]
        
        Mobj_sate_cal = Satellite_Calculate(Ay_NDataChose)
        (Ay_xk,Ay_yk,Ay_zk,Ay_SateTimeDelay) = Mobj_sate_cal.GetSatePositionAndClockDelay(
                                                     Ay_PrC1SateChose,C_Time,F_GPSWeek_Sec)
        
        self.SatePosition = (Ay_xk,Ay_yk,Ay_zk)
        self.SateTimeDelay = Ay_SateTimeDelay
        self.SateChoseNum = Ay_SateChoseNum
        
        sva = Mobj_sate_cal.sva
        tgd = Mobj_sate_cal.tgd
        
        Mobj_error_variance = Error_variance()
        Ay_vare = Mobj_error_variance.vare(sva)
        Ay_vmeas = Mobj_error_variance.vmeas()
        
        Ay_elevation = np.zeros(len(Ay_xk)) + np.pi/2
        Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_GuessPosition.T).return_enu()
        Ay_fix_position = np.array([100,100,100])
        TF_tgd_fix = True
        
        I_loop_break = 0
        Ay_ReceiverDelay = 0
        while abs(Ay_fix_position[0]) > 1e-4 or abs(Ay_fix_position[1]) > 1e-4 or abs(Ay_fix_position[2]) > 1e-4:
            Ay_GuessPosition_llh = np.zeros((3,len(Ay_PrC1SateChose)))
            for j in range(len(Ay_PrC1SateChose)):
                Ay_GuessPosition_llh[:,j] = np.array([xyz2llh.xyz2llh(Ay_GuessPosition[0],Ay_GuessPosition[1],Ay_GuessPosition[2]).xyz()])
            
            Ay_varerr = Mobj_error_variance.varerr(Ay_elevation,S_ion_model)
            
            Mobj_delay = Error_module()
            if S_ion_model == 'broadcast':
                S_n_data_path_ = S_NDataPath + 'NData{0:02d}{1:03d}_ION.npy'.format(I_Year,I_Doy)
                Ay_dion = Mobj_delay.iono_model_broadcast(I_Year,I_Doy,
                                                          Ay_GuessPosition_llh[0,:]*np.pi/180.,
                                                          Ay_GuessPosition_llh[1,:]*np.pi/180.,
                                                          Ay_elevation,
                                                          Ay_enu_resever_sate,
                                                          C_Time.F_TimeTotal,
                                                          S_n_data_path_
                                                          )
            else:
                Ay_dion = 0
            Ay_vion = Mobj_error_variance.vion(I_loop_break,S_ion_model,Ay_dion,S_DGPS)
            if S_trp_model == 'saastamoinen':
                Ay_dtrp = Mobj_delay.saastamoinen_model(Ay_GuessPosition_llh[0,:]*np.pi/180.,
                                                        Ay_GuessPosition_llh[1,:]*np.pi/180.,
                                                        Ay_GuessPosition_llh[2,:],
                                                        Ay_elevation,
                                                        0.6)
            else:  
                Ay_dtrp = 0
            Ay_vtrp = Mobj_error_variance.vtrp(I_loop_break,S_trp_model,Ay_elevation)
            self.Ay_error_variance_all = Ay_varerr + Ay_vmeas + Ay_vare + Ay_vion + Ay_vtrp 
            self.Ay_error_variance_all = np.zeros_like(self.Ay_error_variance_all)+1
            Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
            self.Ay_guess_range_list_first = np.copy(Ay_beacon_position)
            for nn in range(len(self.Ay_guess_range_list_first[0,:])):
                self.Ay_guess_range_list_first[:,nn] -= Ay_GuessPosition[:,0]
            self.Ay_guess_range_list = np.sum((self.Ay_guess_range_list_first)**2,0)**0.5
            self.Ay_guess_range_list_ = np.sum((self.Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_xk*Ay_GuessPosition[1]-Ay_yk*Ay_GuessPosition[0])/F_C
            if TF_tgd_fix:
                F_gamma = F_f1_hz**2/F_f2_hz**2
                if S_ion_model != 'IONFREE':
                    Ay_P1_P2 = (1.0-F_gamma)*tgd*F_C
                    Ay_PrC1SateChose = Ay_PrC1SateChose - Ay_P1_P2/(1.0-F_gamma)
            #                            print(Ay_pseudo_range[-1])
                else:
                    Ay_PrC1SateChose = (F_gamma*Ay_PrC1SateChose - Ay_PrC1P2Chose[1,Ay_SateChoseNum])/(F_gamma-1)
                TF_tgd_fix = False
    #        print(Ay_dion)
    
            self.PrC1SateChose = Ay_PrC1SateChose
    
            Ay_pseudo_range_fix = Ay_PrC1SateChose + F_C*Ay_SateTimeDelay - Ay_ReceiverDelay - Ay_dtrp -Ay_dion
    #        print(Ay_PrC1SateChose)
            #                    print(Ay_beacon_position)
            Mobj_get_position_fst = Positioning(Ay_pseudo_range_fix[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                self.Ay_guess_range_list[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                self.Ay_guess_range_list_[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
                                                Ay_beacon_position[:,np.where(Ay_elevation > F_elevation_filter/180*np.pi)[0]],
                                                Ay_GuessPosition,
                                                self.Ay_error_variance_all[np.where(Ay_elevation > F_elevation_filter/180*np.pi)])
            
            '''
            更新下列數值
            Ay_GuessPosition
            Ay_resever_time_delay
            Ay_enu_resever_sate
            Ay_elevation
            Ay_fix_position
            '''
            Ay_GuessPosition = Mobj_get_position_fst.Positioning_results()[0]
            Ay_ReceiverDelay = Mobj_get_position_fst.Positioning_results()[1] + Ay_ReceiverDelay
            Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_GuessPosition.T).return_enu()
            Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
            Ay_fix_position = Mobj_get_position_fst.Positioning_results()[2]
            
        #    print(Ay_ReceiverDelay)
        #    print(Ay_enu_resever_sate)
        #    print(Ay_elevation)
            
            if I_loop_break > 10:
                print('test_break')
                break
            I_loop_break += 1
        
        self.Elevation = Ay_elevation
        self.Ay_ReceiverDelay = Ay_ReceiverDelay
        return (Ay_GuessPosition.T)
    def ReturnDGPSInfo(self):
        return (self.SatePosition,
                self.SateTimeDelay,
                self.PrC1SateChose,
                self.SateChoseNum,
                self.Ay_error_variance_all,
                self.Elevation,
                self.Ay_ReceiverDelay
                )

#def SPP(I_Year, I_Doy, Ay_GuessPosition, F_GPSWeek_Sec, C_Time, Ay_PrC1P2Chose, C_NData, 
#        S_ion_model='broadcast', S_trp_model='saastamoinen', F_elevation_filter = 15.):
#    '''
#    SPP定位
#    Input: 
#        1. Ay_GuessPosition: 猜測定位點               np.array 3X1
#        2. C_Time:           資料當前的時間            TimeBreakDown的物件 Class
#####        3. Ay_AnsPosition:   測站正確位置              np.array 1X3
#        4. Ay_PrC1P2Chose:     資料當前所有GPS衛星的C1與P2數值 np.array 2X32
#            Ay_PrC1P2Chose[0]: C1
#            Ay_PrC1P2Chose[1]: P2
#        5. C_NData:          資料當天的NData           NDataRead物件  Class
#        6. S_ion_model:      欲使用的電離層模組(預設broadcast)   String
#        7. S_trp_model:      欲使用的大氣模組(預設saastamoinen)  String
#        8. F_elevation_filter: 衛星最低仰角限制(預設15度)        Float 
#    
#    Output:
#        1. SPP計算後位置(xyz)   np.array 3X1
#    '''
#    S_DGPS = 'No'
#    if S_ion_model=='IONFREE':
#        Ay_PrC1P2Chose[0][np.where(Ay_PrC1P2Chose[1] == 0)] = 0
#        Ay_PrC1P2Chose[1][np.where(Ay_PrC1P2Chose[0] == 0)] = 0
#        
#    
#    Ay_NDataChose, Ay_SateChoseNum = C_NData.GetData(Ay_PrC1P2Chose[0], C_Time.F_TimeTotal)
#    Ay_PrC1SateChose = Ay_PrC1P2Chose[0, Ay_SateChoseNum]
#    
#    Mobj_sate_cal = Satellite_Calculate(Ay_NDataChose)
#    (Ay_xk,Ay_yk,Ay_zk,Ay_SateTimeDelay) = Mobj_sate_cal.GetSatePositionAndClockDelay(
#                                                 Ay_PrC1SateChose,C_Time,F_GPSWeek_Sec)
#    sva = Mobj_sate_cal.sva
#    tgd = Mobj_sate_cal.tgd
#    
#    Mobj_error_variance = Error_variance()
#    Ay_vare = Mobj_error_variance.vare(sva)
#    Ay_vmeas = Mobj_error_variance.vmeas()
#    
#    Ay_elevation = np.zeros(len(Ay_xk)) + np.pi/2
#    Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_GuessPosition.T).return_enu()
#    Ay_fix_position = np.array([100,100,100])
#    TF_tgd_fix = True
#    
#    I_loop_break = 0
#    Ay_ReceiverDelay = 0
#    while abs(Ay_fix_position[0]) > 1e-4 or abs(Ay_fix_position[1]) > 1e-4 or abs(Ay_fix_position[2]) > 1e-4:
#        Ay_GuessPosition_llh = np.zeros((3,len(Ay_PrC1SateChose)))
#        for j in range(len(Ay_PrC1SateChose)):
#            Ay_GuessPosition_llh[:,j] = np.array([xyz2llh.xyz2llh(Ay_GuessPosition[0],Ay_GuessPosition[1],Ay_GuessPosition[2]).xyz()])
#        
#        Ay_varerr = Mobj_error_variance.varerr(Ay_elevation,S_ion_model)
#        
#        Mobj_delay = Error_module()
#        if S_ion_model == 'broadcast':
#            S_n_data_path_ = S_NDataPath + 'NData{0:02d}{1:03d}_ION.npy'.format(I_Year,I_Doy)
#            Ay_dion = Mobj_delay.iono_model_broadcast(I_Year,I_Doy,
#                                                      Ay_GuessPosition_llh[0,:]*np.pi/180.,
#                                                      Ay_GuessPosition_llh[1,:]*np.pi/180.,
#                                                      Ay_elevation,
#                                                      Ay_enu_resever_sate,
#                                                      C_Time.F_TimeTotal,
#                                                      S_n_data_path_
#                                                      )
#        else:
#            Ay_dion = 0
#        Ay_vion = Mobj_error_variance.vion(I_loop_break,S_ion_model,Ay_dion,S_DGPS)
#        if S_trp_model == 'saastamoinen':
#            Ay_dtrp = Mobj_delay.saastamoinen_model(Ay_GuessPosition_llh[0,:]*np.pi/180.,
#                                                    Ay_GuessPosition_llh[1,:]*np.pi/180.,
#                                                    Ay_GuessPosition_llh[2,:],
#                                                    Ay_elevation,
#                                                    0.6)
#        else:  
#            Ay_dtrp = 0
#        Ay_vtrp = Mobj_error_variance.vtrp(I_loop_break,S_trp_model,Ay_elevation)
#        self.Ay_error_variance_all = Ay_varerr + Ay_vmeas + Ay_vare + Ay_vion + Ay_vtrp 
#        self.Ay_error_variance_all = np.zeros_like(self.Ay_error_variance_all)+1
#        Ay_beacon_position = np.array([Ay_xk,Ay_yk,Ay_zk])
#        self.Ay_guess_range_list_first = np.copy(Ay_beacon_position)
#        for nn in range(len(self.Ay_guess_range_list_first[0,:])):
#            self.Ay_guess_range_list_first[:,nn] -= Ay_GuessPosition[:,0]
#        self.Ay_guess_range_list = np.sum((self.Ay_guess_range_list_first)**2,0)**0.5
#        self.Ay_guess_range_list_ = np.sum((self.Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_xk*Ay_GuessPosition[1]-Ay_yk*Ay_GuessPosition[0])/F_C
#        if TF_tgd_fix:
#            F_gamma = F_f1_hz**2/F_f2_hz**2
#            if S_ion_model != 'IONFREE':
#                Ay_P1_P2 = (1.0-F_gamma)*tgd*F_C
#                Ay_PrC1SateChose = Ay_PrC1SateChose - Ay_P1_P2/(1.0-F_gamma)
#        #                            print(Ay_pseudo_range[-1])
#            else:
#                Ay_PrC1SateChose = (F_gamma*Ay_PrC1SateChose - Ay_PrC1P2Chose[1,Ay_SateChoseNum])/(F_gamma-1)
#            TF_tgd_fix = False
##        print(Ay_dion)
#        Ay_pseudo_range_fix = Ay_PrC1SateChose + F_C*Ay_SateTimeDelay - Ay_ReceiverDelay - Ay_dtrp -Ay_dion
##        print(Ay_PrC1SateChose)
#        #                    print(Ay_beacon_position)
#        Mobj_get_position_fst = Positioning(Ay_pseudo_range_fix[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
#                                            self.Ay_guess_range_list[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
#                                            self.Ay_guess_range_list_[np.where(Ay_elevation > F_elevation_filter/180*np.pi)],
#                                            Ay_beacon_position[:,np.where(Ay_elevation > F_elevation_filter/180*np.pi)[0]],
#                                            Ay_GuessPosition,
#                                            self.Ay_error_variance_all[np.where(Ay_elevation > F_elevation_filter/180*np.pi)])
#        
#        '''
#        更新下列數值
#        Ay_GuessPosition
#        Ay_resever_time_delay
#        Ay_enu_resever_sate
#        Ay_elevation
#        Ay_fix_position
#        '''
#        Ay_GuessPosition = Mobj_get_position_fst.Positioning_results()[0]
#        Ay_ReceiverDelay = Mobj_get_position_fst.Positioning_results()[1] + Ay_ReceiverDelay
#        Ay_enu_resever_sate = xyz2enu.xyz2enu(np.array([Ay_xk,Ay_yk,Ay_zk]).T,Ay_GuessPosition.T).return_enu()
#        Ay_elevation = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )
#        Ay_fix_position = Mobj_get_position_fst.Positioning_results()[2]
#        
#    #    print(Ay_ReceiverDelay)
#    #    print(Ay_enu_resever_sate)
#    #    print(Ay_elevation)
#        
#        if I_loop_break > 10:
#            print('test_break')
#            break
#        I_loop_break += 1
#        
#    return (Ay_GuessPosition.T)


if __name__ == '__main__':
    try:
        I_Year = int(sys.argv[1])
        I_Doy = int(sys.argv[2])
        S_StationName = sys.argv[3]
    except:
        I_Year = int(input("I_Year:"))
        I_Doy = int(input("I_Doy:"))
        S_StationName = input("I_StationName:")


    C_NData = NDataRead(S_NDataPath + 'NData{0:02d}{1:03d}.npy'.format(I_Year,I_Doy)) 
    Ay_Pr_C1_Rover = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}C1.npy'.format(I_Year,I_Doy,S_StationName))[:,:32]
    Ay_Pr_P2_Rover = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}P2.npy'.format(I_Year,I_Doy,S_StationName))[:,:32]
    Ay_AnsPosition_Rover = np.load(S_TruePositionDataPath.format(I_Year,I_Doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_Year,I_Doy,S_StationName))[0,:]
    Ay_TimeRaw_Rover = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}Time.npy'.format(I_Year,I_Doy,S_StationName))[:,0:6]
    Ay_Time_Rover = Ay_TimeRaw_Rover[:,3]*3600.+Ay_TimeRaw_Rover[:,4]*60.+Ay_TimeRaw_Rover[:,5]
    
    
    F_test_point_x = 0.000000001
    F_test_point_y = 0.
    F_test_point_z = 0.
    Ay_guess_position = np.array([[F_test_point_x],[F_test_point_y],[F_test_point_z]])
    
    F_GPSWeek_Sec= (float(DOY2GPSweek(I_Year,I_Doy))%10)*24*60*60  
    
    Ay_test = np.zeros((2880,3))
    for te in range(2880):
        S_info = "\rSPP  r{0} ,Y:{1:02d} ,D:{2:03d},now in {3:2.2f}%\r".format(S_StationName,
                    I_Year,
                    I_Doy,
                    (te/float(len(Ay_Pr_C1_Rover[:,0])))*100)
        print(S_info,end='')
    #for te in range(1):
    #    print(te)
        I_time_chose = te
        C_TimeRover = TimeBreakDown(Ay_Time_Rover[I_time_chose])
        Ay_PrC1Chose = Ay_Pr_C1_Rover[I_time_chose]
        Ay_PrP2Chose = Ay_Pr_P2_Rover[I_time_chose]
        Ay_PrC1P2Chose = np.array([Ay_PrC1Chose, Ay_PrP2Chose])
    #    Ay_PrC1P2Chose = np.zeros((2,len(Ay_PrC1Chose)))
        
        test = SPPClass()
        Ay_test[te:te+1] = test.SPP(I_Year, I_Doy, Ay_guess_position, F_GPSWeek_Sec, C_TimeRover, Ay_PrC1P2Chose, C_NData, 
                S_ion_model='IONFREE')
#    #    Ay_test[te:te+1] = SPP(Ay_guess_position, C_TimeRover, Ay_AnsPosition_Rover, Ay_PrC1P2Chose, C_NData)
#        Ay_test[te:te+1] = SPP(I_Year, I_Doy, Ay_guess_position, F_GPSWeek_Sec, C_TimeRover, Ay_PrC1P2Chose, C_NData, 
#                S_ion_model='IONFREE')

        