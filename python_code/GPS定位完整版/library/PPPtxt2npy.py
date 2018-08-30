# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:13:49 2018

@author: owo
"""
from CustomValue import *
import numpy as np
import os 

def PPPtxt2npy(I_Year, I_Doy, S_StationName):
    with open(S_RTKPPath.format(I_Year, I_Doy) + '{0}{1:02d}{2:03d}_PPP.txt'.format(S_StationName, I_Year, I_Doy)) as f:
        Lst_DataLines = f.readlines()
        line_num = 0
        title = '%  GPST'
        while True:
            if Lst_DataLines[line_num].find(title) != -1:
                line_num += 1
                break
            line_num += 1
        output_array = np.zeros((2880,3))
        while line_num < len(Lst_DataLines):
            time_chose = int(int(Lst_DataLines[line_num][11:13])*60*2+int(Lst_DataLines[line_num][14:16])*2+int(Lst_DataLines[line_num][17:19])/30)
            lat_chose = float(Lst_DataLines[line_num][24:39])
            lon_chose = float(Lst_DataLines[line_num][39:53])
            height_chose = float(Lst_DataLines[line_num][53:64])
            output_array[time_chose,0] = lat_chose
            output_array[time_chose,1] = lon_chose
            output_array[time_chose,2] = height_chose
            line_num += 1
        save_name = S_RTKPPath.format(I_Year, I_Doy) + '{0}{1:02d}{2:03d}_PPP.npy'.format(S_StationName, I_Year, I_Doy)
        np.save(save_name,output_array)









if __name__ == '__main__':
    try:
        I_Year = int(sys.argv[1])
        I_Doy = int(sys.argv[2])
        S_StationName = sys.argv[3]
    except:
        I_Year = int(input("I_Year:"))
        I_Doy = int(input("I_Doy:"))
        S_StationName = input("I_StationName:")
    PPPtxt2npy(I_Year, I_Doy, S_StationName)