# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 15:27:18 2018

@author: owo
"""

import ORinexDoRNX2RTKP
import PPPtxt2npy
import PPPnpy2Position
import sys

def GetPPPPositionNPYData(I_Year, I_Doy, S_StationName):
    ORinexDoRNX2RTKP.GetPPPPosition(I_Year, I_Doy, S_StationName)
    PPPtxt2npy.PPPtxt2npy(I_Year, I_Doy, S_StationName)
    PPPnpy2Position.PPPnpy2Position(I_Year, I_Doy, S_StationName)
    
if __name__ == '__main__':
    try:
        I_Year = int(sys.argv[1])
        I_Doy = int(sys.argv[2])
        S_StationName = sys.argv[3]
    except:
        I_Year = int(input("I_Year:"))
        I_Doy = int(input("I_Doy:"))
        S_StationName = input("S_StationName:")
        
    GetPPPPositionNPYData(I_Year, I_Doy, S_StationName)