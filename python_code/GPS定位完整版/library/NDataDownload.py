# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 15:21:51 2018

@author: owo
"""

import ftplib
import os
import platform
import sys
from CustomValue import *


def n_data_dam(I_year,I_doy):
    S_ndata_save_path = S_NDataPath
    S_rawdata_save_path = S_NDataPath+'NRowData/'
    
    S_brdc_url_path = r'gnss/data/daily/20{0:02d}/brdc/'
    S_brdc_dataname = r'brdc{1:03d}0.{0:02d}n'
    
    if os.path.exists(S_rawdata_save_path) == False:
        os.makedirs(S_rawdata_save_path)
    
    S_download_path = (S_rawdata_save_path+S_brdc_dataname+'.Z').format(I_year,I_doy)
    
    S_brdc_chcek_num = 0
    while not os.path.isfile(S_download_path) and not os.path.isfile((S_rawdata_save_path+S_brdc_dataname).format(I_year,I_doy)):
        if S_brdc_chcek_num > 10:
            print('!!!!!!!!!! {0:02d}/{1:03d} cont find brdc data'.format(I_year,I_doy))
            os._exit()
        print('download brdc data')
        data_url_path = S_brdc_url_path.format(I_year)
        data_url_name = S_brdc_dataname.format(I_year,I_doy)+'.Z'
        login_rul = ftplib.FTP(r'cddis.gsfc.nasa.gov')
        login_rul.login()
        login_rul.cwd(data_url_path)
        login_rul.retrbinary("RETR " + data_url_name ,open(S_download_path, 'wb').write)
        login_rul.quit()
        if platform.system() == 'Linux':
            os.system('uncompress {0}'.format(S_download_path))
        elif platform.system() == 'Windows':
            os.system('{0} x {1} {2} -y'.format(WinRARPath, S_download_path, S_rawdata_save_path))
        S_brdc_chcek_num += 1
    

if __name__ == '__main__':
    try:
        I_year = [int(sys.argv[1])]
        I_doy = [int(sys.argv[2])]
    except:
        I_year = int(input("I_year:"))
        I_doy = int(input("I_doy:"))
    n_data_dam(I_year,I_doy )