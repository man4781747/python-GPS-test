# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:37:46 2017

@author: owo

pseudo_range     : (N,) array
guess_range_list : (N,) array
beacon_position  : (3,N) array
guess_position_input : (3,1) array

運算定位過程
"""
import numpy as np

def get_position(pseudo_range,guess_range_list,beacon_position,guess_position_input):
    guess_position = np.copy(guess_position_input)
    i = 0
    List_clock_fix = []
    while np.sum((pseudo_range-guess_range_list)**2)**0.5 > 5. and i < 20:
    #for i in range(100):
    #        print(i)
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
        List_clock_fix.append(fix_position[3,0])
    #            guess_position[3,0] = guess_position[3,0] + fix_position[3,0]
        i += 1
    M_HH = np.linalg.inv(H.T*H)
    F_PDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2])**0.5
    F_TDOP = (M_HH[3,3])**0.5
    F_GDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2]+M_HH[3,3])**0.5
    return (guess_position,sum(List_clock_fix),F_PDOP,F_TDOP,F_GDOP)

def get_position_ENU(pseudo_range,guess_range_list,beacon_position,guess_position_input):
    import xyz2enu
    guess_position = np.copy(guess_position_input)
    i = 0
    List_clock_fix = []
    while np.sum((pseudo_range-guess_range_list)**2)**0.5 > 5. and i < 20:
    #for i in range(100):
    #        print(i)
#        beacon_location = np.copy(beacon_position,guess_position_input)
        guess_range_list_first = np.copy(beacon_position)
        for nn in range(len(guess_range_list_first[0,:])):
            guess_range_list_first[:,nn] -= guess_position[:,0]
        guess_range_list = np.sum((guess_range_list_first)**2,0)**0.5
        
        
        H = np.asmatrix(np.zeros((len(guess_range_list),4)))
        for m in range(len(guess_range_list)):
            print(np.array([beacon_position[:,m]]),guess_position.T)
            Ay_enu = xyz2enu.xyz2enu(np.array([beacon_position[:,m]]),guess_position)
            F_range = np.sum(Ay_enu**2)**0.5
            M_e = [((np.sum(Ay_enu[0,0:2]**2)**0.5)/F_range)*(Ay_enu[0,0]/F_range),
                   ((np.sum(Ay_enu[0,0:2]**2)**0.5)/F_range)*(Ay_enu[0,1]/F_range),
                   -(Ay_enu[0,2]/F_range)]
            H[m,:] = np.matrix([[-M_e.T,1.]])
    
        
        fix_position = np.array(np.linalg.inv(H.T*H)*H.T*  (np.matrix([(pseudo_range- guess_range_list).T]).T) )
        
        guess_position[0:3,0] = guess_position[0:3,0] + fix_position[0:3,0]
        
        pseudo_range -= fix_position[3,0]
        List_clock_fix.append(fix_position[3,0])
    #            guess_position[3,0] = guess_position[3,0] + fix_position[3,0]
        i += 1
    M_HH = np.linalg.inv(H.T*H)
    F_PDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2])**0.5
    F_TDOP = (M_HH[3,3])**0.5
    F_GDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2]+M_HH[3,3])**0.5
    return (guess_position,sum(List_clock_fix),F_PDOP,F_TDOP,F_GDOP)