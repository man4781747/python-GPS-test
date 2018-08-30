# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 16:15:12 2017

@author: Chuanping_LASC_PC
"""

import scipy.io
import numpy as np
import os


year = input("year(str):")
day  = input("day(str):")

os.chdir('./minyangVer/20{0}.{1}'.format(year,day))

if os.path.exists('../../data20{0}{1}/aeosv_data'.format(year,day)) == False:
    os.makedirs('../../data20{0}{1}/aeosv_data'.format(year,day))

data_list = []
for filenames in os.listdir('.'): 
    if os.path.isfile(filenames):
        if filenames[8:11] == "mat":
            data_list.append(filenames)
for data_name in data_list:
    print "start {0}".format(data_name[0:7])
    isfile_test = 0
    if os.path.isfile("a{0}.dat".format(data_name[0:7])):
        isfile_test = 1
    if isfile_test == 0:
        data_a = scipy.io.loadmat(data_name)['a{0}'.format(data_name[0:7])]
        data_o = scipy.io.loadmat(data_name)['o{0}'.format(data_name[0:7])]
        data_v = scipy.io.loadmat(data_name)['v{0}'.format(data_name[0:7])]
        data_e = scipy.io.loadmat(data_name)['e{0}'.format(data_name[0:7])]
        data_s = scipy.io.loadmat(data_name)['s{0}'.format(data_name[0:7])]
        
        data_base_a = np.zeros((2880,32))
        data_base_o = np.zeros((2880,32))
        data_base_v = np.zeros((2880,32))
        data_base_e = np.zeros((2880,32))
        data_base_s = np.zeros((2880,32))
        
        x = 0
        while x < 2880:
            y= 0
            while y < 32:
                data_base_a[x,y] = data_a[x,y]
                data_base_o[x,y] = data_o[x,y]           
                data_base_v[x,y] = data_v[x,y]
                data_base_e[x,y] = data_e[x,y]
                data_base_s[x,y] = data_s[x,y]
                
                y += 1
            x += 1
            
        np.savetxt("../../data20{0}{1}/aeosv_data/a{2}.dat".format(year,day,data_name[0:7]),data_base_a)
        np.savetxt("../../data20{0}{1}/aeosv_data/o{2}.dat".format(year,day,data_name[0:7]),data_base_o)
        np.savetxt("../../data20{0}{1}/aeosv_data/v{2}.dat".format(year,day,data_name[0:7]),data_base_v)
        np.savetxt("../../data20{0}{1}/aeosv_data/e{2}.dat".format(year,day,data_name[0:7]),data_base_e)
        np.savetxt("../../data20{0}{1}/aeosv_data/s{2}.dat".format(year,day,data_name[0:7]),data_base_s)
