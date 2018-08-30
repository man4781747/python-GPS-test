# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 16:15:12 2017

@author: Chuanping_LASC_PC
"""

import scipy.io
import numpy as np
import os


year = input("year(str):")
data_list = []
for filenames in os.listdir('.'): 
    if os.path.isfile(filenames):
        if filenames[8:11] == "mat":
            data_list.append(filenames)
for data_name in data_list:
    data_silp = scipy.io.loadmat(data_name)['phase_silp_base']

    
    data_base_silp = np.zeros((2880,32))

    
    x = 0
    while x < 2880:
        y= 0
        while y < 32:
            data_base_silp[x,y] = data_silp[x,y]

            
            y += 1
        x += 1
        
    np.savetxt("{0}{1}{2}slip.dat".format(data_name[0:4],year,data_name[4:7]),data_base_silp)

    print "finish {0}".format(data_name[0:7])