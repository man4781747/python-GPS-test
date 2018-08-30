# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:27:29 2018

@author: owo
"""

from CustomValue import *
import numpy as np
import llh2xyz
import sys

def PPPnpy2Position(I_Year, I_Doy, S_StationName):
    S_PPPnpyDataPath = S_RTKPPath.format(I_Year, I_Doy) + '{0}{1:02d}{2:03d}_PPP.npy'.format(S_StationName, I_Year, I_Doy)
    PPP_load = np.load(S_PPPnpyDataPath)
    PPP_load_check_sum = np.sum(PPP_load,axis=1)
    PPP_array = np.delete(PPP_load,np.where(PPP_load_check_sum==0.),0)
    PPP_location = np.array([np.mean(PPP_array,axis = 0)])
    print(PPP_location)
#    PPP_location_xyz = llh2xyz.llh2xyz(np.array([PPP_location])).return_xyz()
#    print(PPP_location_xyz)
    
    np.save(S_TruePositionDataPath.format(I_Year, I_Doy) + 
            '{0}{1:02d}{2:03d}_position.npy'.format(S_StationName, I_Year, I_Doy),PPP_location)
    
    
if __name__ == '__main__':
    try:
        I_Year = int(sys.argv[1])
        I_Doy = int(sys.argv[2])
        S_StationName = sys.argv[3]
    except:
        I_Year = int(input("I_Year:"))
        I_Doy = int(input("I_Doy:"))
        S_StationName = input("I_StationName:")
    PPPnpy2Position(I_Year, I_Doy, S_StationName)