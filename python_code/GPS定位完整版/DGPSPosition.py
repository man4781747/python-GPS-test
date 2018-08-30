# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 15:42:47 2018

@author: owo
"""

import sys
sys.path.append(r'./library')

from SPPPosition import SPPClass
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

def DGPS(I_Year, I_Doy, Ay_GuessPosition, F_GPSWeek_Sec, C_Time_Rover, Ay_PrC1P2Chose_Rover,
         C_Time_Base, Ay_PrC1P2Chose_Base, Ay_BasePosition, F_elevation_filter = 15.):

    '''
    SPP 定位
    '''
    
    C_RoverSPPPosition = SPPClass()
    Ay_GuessPosition = C_RoverSPPPosition.SPP(I_Year, I_Doy, Ay_GuessPosition, F_GPSWeek_Sec, C_Time_Rover, Ay_PrC1P2Chose_Rover, C_NData)
    
    (Ay_SatePosition_Rover,
     Ay_SateTimeDelay_Rover,
     Ay_PrC1SateChose_Rover,
     Ay_SateChoseNum_Rover,
     Ay_error_variance_all_Rover,   
     Ay_Elevation_Rover,
     Ay_ReceiverDelay_Rover) = C_RoverSPPPosition.ReturnDGPSInfo()
    '''
    計算Base站所得真實距離
    '''
    Ay_NDataChose_Base, Ay_SateChoseNum_Base = C_NData.GetData(Ay_PrC1P2Chose_Base[0], C_Time_Base.F_TimeTotal)
    Ay_PrC1SateChose_Base = Ay_PrC1P2Chose_Base[0, Ay_SateChoseNum_Base]
    Mobj_SateCal_Base = Satellite_Calculate(Ay_NDataChose_Base)
    (Ay_xk_Base,
     Ay_yk_Base,
     Ay_zk_Base,
     Ay_SateTimeDelay_Base) = Mobj_SateCal_Base.GetSatePositionAndClockDelay(
                                                 Ay_PrC1SateChose_Base,C_Time_Base,F_GPSWeek_Sec)
    tgd_Base = Mobj_SateCal_Base.tgd
    
    '''
    Base TDG FIX
    '''
    Ay_P1_P2_Base = (1.0-(F_f1_hz**2/F_f2_hz**2))*tgd_Base*F_C
    Ay_PrC1SateChose_Base = Ay_PrC1SateChose_Base - Ay_P1_P2_Base/(1.0-(F_f1_hz**2/F_f2_hz**2))
    
    Ay_SatePosition_Base = np.array([Ay_xk_Base,Ay_yk_Base,Ay_zk_Base])
    
    Ay_guess_range_list_DGPS_before_first = np.copy(Ay_SatePosition_Base)
    for nn in range(len(Ay_guess_range_list_DGPS_before_first[0,:])):
        Ay_guess_range_list_DGPS_before_first[:,nn] -= Ay_BasePosition
    Ay_guess_range_list_DGPS_before_ = np.sum((Ay_guess_range_list_DGPS_before_first)**2,0)**0.5 + F_OMGE*(Ay_xk_Base*Ay_AnsPosition_Base[1]-Ay_yk_Base*Ay_AnsPosition_Base[0])/F_C
    
    '''
    比較 Rover 與 Base 兩站所擁有的衛星 並選取兩站接共同慵有的衛星
    '''
    Lst_sate_match = list(set(Ay_SateChoseNum_Rover)&
                          set(Ay_SateChoseNum_Base))    
    Ay_SateMatch_Rover = np.zeros(len(Lst_sate_match)).astype('int')
    Ay_SateMatch_Base = np.zeros(len(Lst_sate_match)).astype('int')
    for I_sate_chose in range(len(Lst_sate_match)):
        Ay_SateMatch_Rover[I_sate_chose] = int(np.where(Ay_SateChoseNum_Rover == Lst_sate_match[I_sate_chose])[0])
        Ay_SateMatch_Base[I_sate_chose]  = int(np.where(Ay_SateChoseNum_Base  == Lst_sate_match[I_sate_chose])[0])
    Ay_pseudo_range_DGPS_chose_rover = Ay_PrC1SateChose_Rover[Ay_SateMatch_Rover[:]]
    Ay_pseudo_range_DGPS_chose_base  = Ay_PrC1SateChose_Base[Ay_SateMatch_Base[:]]
    
#    print(Ay_pseudo_range_DGPS_chose_rover[:])
    Ay_Elevation_Rover_Chose = Ay_Elevation_Rover[Ay_SateMatch_Rover[:]]
    
    
    Ay_SatePosition = np.array([Ay_SatePosition_Rover[0],
                                Ay_SatePosition_Rover[1],
                                Ay_SatePosition_Rover[2]])
    
    
    Ay_GuessPosition = Ay_GuessPosition.T
    
    for i in range(3):
        Ay_guess_range_list_first = np.copy(Ay_SatePosition)
        for nn in range(len(Ay_guess_range_list_first[0,:])):
            Ay_guess_range_list_first[:,nn] -= Ay_GuessPosition[:,0]
        Ay_guess_range_list = np.sum((Ay_guess_range_list_first)**2,0)**0.5
        Ay_guess_range_list_ = np.sum((Ay_guess_range_list_first)**2,0)**0.5 + F_OMGE*(Ay_SatePosition_Rover[0]*Ay_guess_position[1]-Ay_SatePosition_Rover[1]*Ay_guess_position[0])/F_C

        Ay_PrFixDGPS = (Ay_pseudo_range_DGPS_chose_rover) - ((Ay_pseudo_range_DGPS_chose_base) - Ay_guess_range_list_DGPS_before_[Ay_SateMatch_Base[:]]) - Ay_ReceiverDelay_Rover
        print(Ay_GuessPosition)

        Mobj_get_position_fst = Positioning(Ay_PrFixDGPS[np.where(Ay_Elevation_Rover_Chose > F_elevation_filter/180*np.pi)],
                                            Ay_guess_range_list[np.where(Ay_Elevation_Rover_Chose > F_elevation_filter/180*np.pi)],
                                            Ay_guess_range_list_[np.where(Ay_Elevation_Rover_Chose > F_elevation_filter/180*np.pi)],
                                            Ay_SatePosition[:,np.where(Ay_Elevation_Rover_Chose > F_elevation_filter/180*np.pi)[0]],
                                            Ay_GuessPosition,
                                            Ay_error_variance_all_Rover[np.where(Ay_Elevation_Rover_Chose > F_elevation_filter/180*np.pi)])
        
        Ay_GuessPosition = Mobj_get_position_fst.Positioning_results()[0]
        Ay_ReceiverDelay_Rover = Mobj_get_position_fst.Positioning_results()[1] + Ay_ReceiverDelay_Rover
        Ay_enu_resever_sate = xyz2enu.xyz2enu(Ay_SatePosition.T,Ay_GuessPosition.T).return_enu()
        Ay_Elevation_Rover_Chose = np.arctan2( (Ay_enu_resever_sate[:,2]),np.sum(Ay_enu_resever_sate[:,0:2]**2,1)**0.5 )

    return Ay_GuessPosition.T



if __name__ == '__main__':
    try:
        I_Year = int(sys.argv[1])
        I_Doy = int(sys.argv[2])
        S_StationName = sys.argv[3]
    except:
        I_Year = int(input("I_Year:"))
        I_Doy = int(input("I_Doy:"))
        S_StationName_Rover = input("S_StationName_Rover: ")
        S_StationName_Base = input("S_StationName_Base: ")


    C_NData = NDataRead(S_NDataPath + 'NData{0:02d}{1:03d}.npy'.format(I_Year,I_Doy)) 
    Ay_Pr_C1_Rover = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}C1.npy'.format(I_Year,I_Doy,S_StationName_Rover))[:,:32]
    Ay_Pr_P2_Rover = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}P2.npy'.format(I_Year,I_Doy,S_StationName_Rover))[:,:32]
    Ay_AnsPosition_Rover = np.load(S_TruePositionDataPath.format(I_Year,I_Doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_Year,I_Doy,S_StationName_Rover))[0,:]
    Ay_TimeRaw_Rover = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}Time.npy'.format(I_Year,I_Doy,S_StationName_Rover))[:,0:6]
    Ay_Time_Rover = Ay_TimeRaw_Rover[:,3]*3600.+Ay_TimeRaw_Rover[:,4]*60.+Ay_TimeRaw_Rover[:,5]
    
    Ay_Pr_C1_Base = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}C1.npy'.format(I_Year,I_Doy,S_StationName_Base))[:,:32]
    Ay_Pr_P2_Base = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}P2.npy'.format(I_Year,I_Doy,S_StationName_Base))[:,:32]
    Ay_AnsPosition_Base = np.load(S_TruePositionDataPath.format(I_Year,I_Doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_Year,I_Doy,S_StationName_Base))[0,:]
    Ay_TimeRaw_Base = np.load(S_PhaseAndCodeDataPath.format(I_Year,I_Doy)+'30s/{2}{0:02d}{1:03d}Time.npy'.format(I_Year,I_Doy,S_StationName_Base))[:,0:6]
    Ay_Time_Base = Ay_TimeRaw_Base[:,3]*3600.+Ay_TimeRaw_Base[:,4]*60.+Ay_TimeRaw_Base[:,5]

    F_test_point_x = 0.000000001
    F_test_point_y = 0.
    F_test_point_z = 0.
    Ay_guess_position = np.array([[F_test_point_x],[F_test_point_y],[F_test_point_z]])
    
    F_GPSWeek_Sec= (float(DOY2GPSweek(I_Year,I_Doy))%10)*24*60*60  
    
    Ay_test = np.zeros((2880,3))
#    for te in range(2880):
#        S_info = "\rSPP  r{0} ,Y:{1:02d} ,D:{2:03d},now in {3:2.2f}%\r".format(S_StationName,
#                    I_Year,
#                    I_Doy,
#                    (te/float(len(Ay_Pr_C1_Rover[:,0])))*100)
#        print(S_info,end='')
    for te in range(1):
    #    print(te)
        I_time_chose = te
        C_TimeRover = TimeBreakDown(Ay_Time_Rover[I_time_chose])
        Ay_PrC1Chose_Rover = Ay_Pr_C1_Rover[I_time_chose]
        Ay_PrP2Chose_Rover = Ay_Pr_P2_Rover[I_time_chose]
        Ay_PrC1P2Chose_Rover = np.array([Ay_PrC1Chose_Rover, Ay_PrP2Chose_Rover])
        

        C_TimeBase = TimeBreakDown(Ay_Time_Base[I_time_chose])
        Ay_PrC1Chose_Base = Ay_Pr_C1_Base[I_time_chose]
        Ay_PrP2Chose_Base = Ay_Pr_P2_Base[I_time_chose]
        Ay_PrC1P2Chose_Base = np.array([Ay_PrC1Chose_Base, Ay_PrP2Chose_Base])
        
        Ay_test[te:te+1] = DGPS(I_Year, I_Doy, Ay_guess_position, F_GPSWeek_Sec, C_TimeRover, 
               Ay_PrC1P2Chose_Rover,C_TimeBase, Ay_PrC1P2Chose_Base, Ay_AnsPosition_Base)