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

os.chdir('../../GPSTEC_minyan/gnsstec_v7.2/OBS/gps/20{0}.{1}'.format(year,day))

data_list = []
for filenames in os.listdir('.'): 
    if os.path.isfile(filenames):
        if filenames[9:13] == "mat":
            data_list.append(filenames)
for data_name in data_list:
#    print "start {0}".format(data_name[0:7])
    data_L1 = scipy.io.loadmat(data_name)['L1']
#    print "L1 load OK!!"
    data_L2 = scipy.io.loadmat(data_name)['L2']
#    print "L2 load OK!!"
    data_P1 = scipy.io.loadmat(data_name)['P1']
#    print "P1 load OK!!"
    data_P2 = scipy.io.loadmat(data_name)['P2']
#    print "P2 load OK!!"
    data_C1 = scipy.io.loadmat(data_name)['C1']
#    print "C1 load OK!!"
    data_hr = scipy.io.loadmat(data_name)['hour']
    data_minute = scipy.io.loadmat(data_name)['minute']
    data_sec = scipy.io.loadmat(data_name)['second']
    
    data_base_L1 = np.zeros((2880,32))
    data_base_L2 = np.zeros((2880,32))
    data_base_P1 = np.zeros((2880,32))
    data_base_P2 = np.zeros((2880,32))
    data_base_C1 = np.zeros((2880,32))
    print "change start!!"
    x = 0
    while x < len(data_hr):
        data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/0.5)
        data_base_L1[data_local] = np.matrix(data_L1[x].toarray())
        data_base_L2[data_local] = np.matrix(data_L2[x].toarray())
        data_base_P1[data_local] = np.matrix(data_P1[x].toarray())
        data_base_P2[data_local] = np.matrix(data_P2[x].toarray())
        data_base_C1[data_local] = np.matrix(data_C1[x].toarray())
        
        x += 1
    print "start to save"    
    save_dir = '../../../../../python/Odata/data20{0}{1}/phase_data/'.format(year,day)
    np.savetxt("{0}{1}{2}{3}phaseL1.dat".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_L1)
    np.savetxt("{0}{1}{2}{3}phaseL2.dat".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_L2)
    np.savetxt("{0}{1}{2}{3}phaseP1.dat".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_P1)
    np.savetxt("{0}{1}{2}{3}phaseP2.dat".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_P2)
    np.savetxt("{0}{1}{2}{3}phaseC1.dat".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_C1)
    print "finish {0}".format(data_name[0:7])