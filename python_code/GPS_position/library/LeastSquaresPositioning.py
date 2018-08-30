# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:24:28 2018

@author: owo
"""
import numpy as np

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
                self.H[m,:] = np.matrix([[(self.guess_position[0,0]-beacon_location[0,m])/self.guess_range_list[m],
                                     (self.guess_position[1,0]-beacon_location[1,m])/self.guess_range_list[m],
                                     (self.guess_position[2,0]-beacon_location[2,m])/self.guess_range_list[m],1.]]/(Ay_error_variance_all[m])**0.5 )

            fix_position = np.array(np.linalg.inv(self.H.T*self.H)*self.H.T*  (np.matrix([((self.pseudo_range- self.guess_range_list_fix_rot)/(Ay_error_variance_all)**0.5 ).T]).T) )
            self.guess_position[0:3,0] = self.guess_position[0:3,0] + fix_position[0:3,0]
            self.pseudo_range -= fix_position[3,0]

            self.List_clock_fix.append(fix_position[3,0])

        M_HH = np.linalg.inv(self.H.T*self.H)
        self.F_PDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2])**0.5
        self.F_TDOP = (M_HH[3,3])**0.5
        self.F_GDOP = (M_HH[0,0]+M_HH[1,1]+M_HH[2,2]+M_HH[3,3])**0.5
        self.Ay_fix_position = fix_position[0:3,0]
        
    def Positioning_results(self):
        return (self.guess_position,sum(self.List_clock_fix),self.Ay_fix_position,self.F_PDOP,self.F_TDOP,self.F_GDOP)
    