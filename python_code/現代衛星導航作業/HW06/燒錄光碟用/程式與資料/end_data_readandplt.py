# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:53:33 2018

@author: owo

做完 HW05_allforone.py
"""

import numpy as np
import matplotlib.pyplot as plt 

S_event = './{0}_data/{0}'.format('New_GPS_day2_out')

Ay_atmo_llh = np.load('{0}_atmsfree_llh_all.npy'.format(S_event))
Ay_atmo_xyz = np.load('{0}_atmsfree_xyz_all.npy'.format(S_event))
Ay_atmo_enu = np.load('{0}_atmsfree_enu_all.npy'.format(S_event))
Ay_atmo_sate_num = np.load('{0}_atmsfree_sate_num.npy'.format(S_event))
Ay_atmo_time = np.load('{0}_atmsfree_time.npy'.format(S_event))
Ay_atmo_DOP = np.load('{0}_atmsfree_DOP.npy'.format(S_event))

plt.plot(Ay_atmo_time+24,Ay_atmo_sate_num)
plt.xlabel('LT')
plt.ylabel('num')
plt.title('num of satelite')
plt.savefig('{0}_notatmsfree_satenum.png'.format(S_event))
plt.clf()

atmo_DOP = plt.plot(Ay_atmo_time,Ay_atmo_DOP[0,:],label='PDOP')
atmo_DOP = plt.plot(Ay_atmo_time,Ay_atmo_DOP[1,:],label='TDOP')
atmo_DOP = plt.plot(Ay_atmo_time,Ay_atmo_DOP[2,:],label='GDOP')
plt.legend()
plt.xlabel('LT')
plt.ylabel('m')
plt.title('atms-free_DOP')

plt.savefig('{0}_DOP.png'.format(S_event))
plt.clf()

with open('{0}_atmofree_llh_googleearth.txt'.format(S_event),'w') as f:
    for i in range(len(Ay_atmo_llh)):
        f.write("{0},{1},{2}\n".format(Ay_atmo_llh[i,1],Ay_atmo_llh[i,0],Ay_atmo_llh[i,2]))