# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 17:01:10 2018

@author: owo
"""

from CustomValue import *
import os
import sys
import DOY2GPSweek

def GetPPPPosition(I_Year, I_Doy, S_StationName):
    if os.path.exists(S_RTKPPath.format(I_Year, I_Doy)) == False:
        os.makedirs(S_RTKPPath.format(I_Year, I_Doy))
    
    rnx2rtkp_path = S_rnx2rtkpPath
    o_data_path = S_ORinexDataPath.format(I_Year, I_Doy) + '{0}{2:03d}0.{1:02d}o '.format(S_StationName, I_Year, I_Doy)
    brdc_path = S_NDataPath + 'NRowData/brdc{2:03d}0.{1:02d}n '
    PPP_conf = S_PPPconfPath
    sp3_path = S_SP3DataPath + 'igs{0}.sp3 '.format(DOY2GPSweek.DOY2GPSweek(I_Year, I_Doy))
    save_txt_path_PPP = '-o '+S_RTKPPath.format(I_Year, I_Doy)+'{0}{1:02d}{2:03d}_PPP.txt '
    os.system(
            ((S_rnx2rtkpPath+'-k '+PPP_conf+save_txt_path_PPP+o_data_path+brdc_path+sp3_path).format(S_StationName, I_Year, I_Doy)).replace('/','\\')
            )
    
    
    
if __name__ == '__main__':
    try:
        I_year = int(sys.argv[1])
        I_doy = int(sys.argv[2])
        S_StationName = sys.argv[3]
    except:
        I_year = int(input("I_year:"))
        I_doy = int(input("I_doy:"))
        S_StationName = input("S_StationName:")
    
    GetPPPPosition(I_year, I_doy, S_StationName)