# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:19:11 2017

@author: owo
"""

import numpy as np
import ftplib
#from DOY2GPSweek import DOY2GPSweek
import os
import platform
import sys

def n_data_dam(I_year,I_doy):
    S_ndata_save_path = './n_data'
    S_rawdata_save_path = S_ndata_save_path+'/n_row_data/'
    
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
            os.system('Winrar x {0}'.format(S_download_path))
        S_brdc_chcek_num += 1
    
#    S_GPSweek = DOY2GPSweek(I_year,I_doy)
    
    with open(S_rawdata_save_path+S_brdc_dataname.format(I_year,I_doy)) as f :
        data_read_lines = f.readlines()
        
    line_chose = 0
    
    Ay_ion_broadcast = np.zeros((2,4))
    while data_read_lines[line_chose].find('ION ALPHA') == -1:
        line_chose += 1
    for i in range(4):
        Ay_ion_broadcast[0,i] = float(data_read_lines[line_chose][2+(i*12):2+((i+1)*12)].replace('D','e'))
    while data_read_lines[line_chose].find('ION BETA') == -1:
        line_chose += 1
    for i in range(4):
        Ay_ion_broadcast[1,i] = float(data_read_lines[line_chose][2+(i*12):2+((i+1)*12)].replace('D','e'))
    
    
    while data_read_lines[line_chose].find('END OF HEADER') == -1:
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
    np.save(S_ndata_save_path+'/n_data_{0:02d}{1:03d}.npy'.format(I_year,I_doy),data_end)
    np.save(S_ndata_save_path+'/n_data_{0:02d}{1:03d}_ion.npy'.format(I_year,I_doy),Ay_ion_broadcast)

if __name__ == '__main__':
    try:
        I_year = [int(sys.argv[1])]
        I_doy = [int(sys.argv[2])]
    except:
        I_year = int(input("I_year:"))
        I_doy = int(input("I_doy:"))
    n_data_dam(I_year,I_doy )