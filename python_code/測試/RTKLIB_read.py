# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 16:37:52 2018

@author: owo
"""
import numpy as np
import xyz2enu
import matplotlib.pyplot as plt

I_doy = 76
I_year = 15
S_ans_position_path = 'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/position_data/'

Ay_ans_position = np.load(S_ans_position_path.format(I_year,I_doy)+'{2}{0:02d}{1:03d}_position.npy'.format(I_year,I_doy,'sun1'))[0:1,:]

#Ay_ans_position = np.array([[ -2997876.4145,5007428.4953,2566681.003    ]])

with open(r'C:\Users\owo\Desktop\我der碩士論文\電將砲\sun1{0:03d}0.pos'.format(I_doy)) as f:
    test = f.readlines()[23:]
    
Ay_time = np.zeros((len(test),3))
Ay_xyz = np.zeros((len(test),3))


for i in range(len(test)):
    Ay_time[i,0] = int(test[i][11:13])
    Ay_time[i,1] = int(test[i][14:16])
    Ay_time[i,2] = float(test[i][17:23])
    Ay_xyz[i,0] = float(test[i][23:38])
    Ay_xyz[i,1] = float(test[i][38:53])
    Ay_xyz[i,2] = float(test[i][53:68])
    Ay_xyz[i:i+1,:] = xyz2enu.xyz2enu(Ay_xyz[i:i+1,:],Ay_ans_position).return_enu()


np.save('sun1_{0:02d}{1:03d}_RTK_ENU.npy'.format(I_year,I_doy),Ay_xyz)
np.save('sun1_{0:02d}{1:03d}_RTK_time.npy'.format(I_year,I_doy),Ay_time)
