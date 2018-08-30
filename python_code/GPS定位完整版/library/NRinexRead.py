# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:19:11 2017

@author: owo
"""

import numpy as np
from CustomValue import *
import os

def NRinexRead(I_Year, I_Doy):
    if os.path.isdir(S_NDataPath) != True:
        os.makedirs(S_NDataPath)
    
    if os.path.isfile(S_NDataPath+'NRowData/brdc{1:03d}0.{0:02d}n'.format(I_Year, I_Doy)) != True:
        print("Can't find brdc{1:03d}0.{0:02d}n, Try Download".format(I_Year, I_Doy))
        import NDataDownload
        NDataDownload.n_data_dam(I_Year,I_Doy)
    
    with open(S_NDataPath+'NRowData/brdc{1:03d}0.{0:02d}n'.format(I_Year, I_Doy)) as f :
        data_read_lines = f.readlines()
        
    Ay_IonBroadcast = np.zeros((2, 4))
    line_chose = 0
    while data_read_lines[line_chose].find('END OF HEADER') == -1:
        if data_read_lines[line_chose].find('ION ALPHA') != -1:
            for ION_ALPHA in range(4):
                Ay_IonBroadcast[0,ION_ALPHA] = float(data_read_lines[line_chose][3+12*ION_ALPHA:14+12*ION_ALPHA].replace('D','e'))
                print(data_read_lines[line_chose][3+12*ION_ALPHA:14+12*ION_ALPHA])
        if data_read_lines[line_chose].find('ION BETA') != -1:
            for ION_BETA in range(4):
                Ay_IonBroadcast[1,ION_BETA] = float(data_read_lines[line_chose][3+12*ION_BETA:14+12*ION_BETA].replace('D','e'))
        
        line_chose += 1
    line_chose += 1
    
    data_end = np.zeros((0,38))
    for test in range(int((len(data_read_lines)-line_chose)/8)):
        array_box = np.zeros((1,38))
        array_box[0,0] = int(data_read_lines[line_chose][0:2])     # PRN
        array_box[0,1] = int(data_read_lines[line_chose][2:5])     # Year
        array_box[0,2] = int(data_read_lines[line_chose][5:8])     # Month
        array_box[0,3] = int(data_read_lines[line_chose][8:11])    # Day
        array_box[0,4] = int(data_read_lines[line_chose][11:14])   # Hr
        array_box[0,5] = int(data_read_lines[line_chose][14:17])   # Min
        array_box[0,6] = float(data_read_lines[line_chose][17:22]) # Sec
        array_box[0,7] = float(data_read_lines[line_chose][22:41].replace('D','e')) # af0
        array_box[0,8] = float(data_read_lines[line_chose][41:60].replace('D','e')) # af1
        array_box[0,9] = float(data_read_lines[line_chose][60:79].replace('D','e')) # af2
        replace_num = 10
        for line_inside in range(7):
            for i in range(4):
                array_box[0,replace_num] = float(data_read_lines[line_chose+line_inside+1][3+19*i:22+19*i].replace('D','e'))
                replace_num += 1
        data_end = np.concatenate((data_end,array_box))
        line_chose += 8
    np.save(S_NDataPath+'NData{0:02d}{1:03d}.npy'.format(I_Year, I_Doy),data_end)
    np.save(S_NDataPath+'NData{0:02d}{1:03d}_ION.npy'.format(I_Year, I_Doy),Ay_IonBroadcast)
    
if __name__ == '__main__':
    import NRinexRead
    try:
        I_year = [int(sys.argv[1])]
        I_doy = [int(sys.argv[2])]
    except:
        I_year = int(input("I_year:"))
        I_doy = int(input("I_doy:"))
    NRinexRead.NRinexRead(I_year,I_doy)