# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:07:35 2017

@author: Chuanping_LASC_PC
"""

import os
#import subprocess
import ftplib
#import numpy as np
import multiprocessing as mp
import datetime
import sys
from n_data_download_make import n_data_dam

def do_rnx2rtkp(data_name,test,gps_weektatal,I_data_rate):
    print(test)
    rnx2rtkp_path = '/nishome/man4781747/rnx2rtkp/rnx2rtkp '
    single_conf = '-k /nishome/man4781747/rnx2rtkp/single.conf '
    save_txt_path = '-o ./rtkp_data/{0}{1}{2}0_single.txt '
    o_data_path = './odata/{3}s/{0}{2}0.{1}o '
    brdc_path = '../n_data/n_row_data/brdc{2}0.{1}n'
    PPP_conf = '-k /nishome/man4781747/rnx2rtkp/PPP.conf '
    sp3_path = 'igs{0}.sp3 '.format(gps_weektatal)
    save_txt_path_PPP = '-o ./rtkp_data/{0}{1}{2}0_PPP.txt '
    
    
#    print((rnx2rtkp_path+PPP_conf+save_txt_path_PPP+o_data_path+sp3_path+brdc_path).format(data_name[0:4],data_name[9:11],data_name[4:7],I_data_rate))
    print((rnx2rtkp_path+single_conf+save_txt_path+o_data_path+brdc_path).format(data_name[0:4],data_name[9:11],data_name[4:7],I_data_rate))
    os.system((rnx2rtkp_path+single_conf+save_txt_path+o_data_path+brdc_path).format(data_name[0:4],data_name[9:11],data_name[4:7],I_data_rate))
    
    os.system((rnx2rtkp_path+PPP_conf+save_txt_path_PPP+o_data_path+sp3_path+brdc_path).format(data_name[0:4],data_name[9:11],data_name[4:7],I_data_rate))
#   
def multucore(name_list,processes_num,gps_weektatal,I_data_rate):
    pool = mp.Pool(processes=processes_num)
#    print(name_list[0])
    res = [pool.apply_async(do_rnx2rtkp,(name_list[i],i,gps_weektatal,I_data_rate)) for i in range(len(name_list))]
    print([R.get() for R in res])


if __name__ == '__main__':
#    year_list = [int(x) for x in input('yy,yy(int): ').split()]    
#    doy_list = [int(x) for x in input('ddd,ddd(int): ').split()]        
#    processes_num = int(input("processes_num(int):"))

    year_list = [int(sys.argv[1])]
    doy_list = [int(sys.argv[2])]
    processes_num = int(sys.argv[3])
    I_data_rate = int(sys.argv[4])

#    print(year_list)
#    print(doy_list)
#    print(processes_num)
    
    save_path = r'./data20{0:02d}{1:03d}/'
    
    brdc_url_path = r'gnss/data/daily/20{0:02d}/brdc/'
    brdc_dataname = r'brdc{1:03d}0.{0:02d}n'
    
    sp3_url_path = r'pub/product/{0:04d}/'
    sp3_dataname = r'igs{2}.sp3'
    
    for year in year_list:
        for doy in doy_list:
            path = (save_path+brdc_dataname).format(year,doy)
#            brdc_chcek_num = 0
#            while not os.path.isfile(path):
#                if brdc_chcek_num > 10:
#                    print('!!!!!!!!!! {0:02d}/{1:03d} cont find brdc data'.format(year,doy))
#                    os._exit()
#                print('download brdc data')
#                data_url_path = brdc_url_path.format(year)
#                data_url_name = brdc_dataname.format(year,doy)+'.Z'
#                login_rul = ftplib.FTP(r'cddis.gsfc.nasa.gov')
#                login_rul.login()
#                login_rul.cwd(data_url_path)
#                login_rul.retrbinary("RETR " + data_url_name ,open(path+'.Z', 'wb').write)
#                login_rul.quit()
#                os.system('uncompress {0}'.format(path+'.Z'))
#                brdc_chcek_num += 1
            n_data_dam(year,doy)

            doy2day = datetime.date(year+2000,1,1)+datetime.timedelta(doy-1)
            gps_day = int(round(((doy2day-datetime.date(1980, 1, 6)).days/7.-int((doy2day-datetime.date(1980, 1, 6)).days/7))*7))
            gps_week = int((doy2day-datetime.date(1980, 1, 6)).days/7)
#            print(gps_week)
            #print(gps_day)
            gps_weektatal = '{0:04d}{1:01d}'.format(gps_week,gps_day)
            path_local_sp3 = (save_path+sp3_dataname).format(year,doy,gps_weektatal)
            
            sp3_chcek_num = 0
            while not os.path.isfile(path_local_sp3):
                if sp3_chcek_num > 10:
                    print('!!!!!!!!!! {0:02d}/{1:03d} cont find sp3 data'.format(year,doy))
                    os._exit()
                print('download sp3 data')
                sp3_dataname_chose = sp3_dataname.format(0,0,gps_weektatal)+'.Z'
                sp3_dataname_chose_path = sp3_url_path.format(gps_week)
                login_rul = ftplib.FTP(r'ftp.igs.org')
                login_rul.login()
                login_rul.cwd(sp3_dataname_chose_path)
                login_rul.retrbinary("RETR " + sp3_dataname_chose ,open(path_local_sp3+'.Z', 'wb').write)
                login_rul.quit()
                os.system('uncompress {0}'.format(path_local_sp3+'.Z'))
                sp3_chcek_num += 1

            os.chdir('./data20{0:02d}{1:03d}/odata/{2}s'.format(year,doy,I_data_rate))
            
            odata_list = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[4:] == '{1:03d}0.{0:02d}o'.format(year,doy):            
                        odata_list.append(filenames)
            
            os.chdir('../..')
            if os.path.exists('./rtkp_data') == False:
                os.makedirs('./rtkp_data')
            
            multucore(odata_list,processes_num,gps_weektatal,I_data_rate)
        
        