# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:44:42 2017

@author: Chuanping_LASC_PC
"""

import numpy as np
import os 
import multiprocessing as mp
import sys

def data_trans(dataname):
    with open(dataname) as f :
        data_line = f.readlines()
        line_num = 0
        title = '%  GPST'
        while True:
            if data_line[line_num].find(title) != -1:
                line_num += 1
                break
            line_num += 1
        output_array = np.zeros((2880,3))
        while line_num < len(data_line):
            time_chose = int(int(data_line[line_num][11:13])*60*2+int(data_line[line_num][14:16])*2+int(data_line[line_num][17:19])/30)
            lat_chose = float(data_line[line_num][24:39])
            lon_chose = float(data_line[line_num][39:53])
            height_chose = float(data_line[line_num][53:64])
            output_array[time_chose,0] = lat_chose
            output_array[time_chose,1] = lon_chose
            output_array[time_chose,2] = height_chose
            line_num += 1
        save_name = dataname[:14]+'.npy'
        print(dataname)
        np.save(save_name,output_array)


def multucore(name_list,processes_num):
    pool = mp.Pool(processes=processes_num)
    res = [pool.apply_async(data_trans,(name_list[i],)) for i in range(len(name_list))]
    print([R.get() for R in res])



if __name__ == '__main__':
#    year_list = [int(x) for x in input('yy,yy(int): ').split()]    
#    doy_list = [int(x) for x in input('ddd,ddd(int): ').split()]    
#    processes_num = int(input("processes_num(int):"))
    
    year_list = [int(sys.argv[1])]
    doy_list = [int(sys.argv[2])]
    processes_num = int(sys.argv[3])

    for year in year_list:
        for doy in doy_list:
            os.chdir('./data20{0:02d}{1:03d}/rtkp_data'.format(year,doy))
            
            data_list = []
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[4:] == '{0:02d}{1:03d}0_single.txt'.format(year,doy):            
                        data_list.append(filenames)
            for filenames in os.listdir('.'): 
                if os.path.isfile(filenames):
                    if filenames[4:] == '{0:02d}{1:03d}0_PPP.txt'.format(year,doy):            
                        data_list.append(filenames)
    
            multucore(data_list,processes_num)
        
        
        