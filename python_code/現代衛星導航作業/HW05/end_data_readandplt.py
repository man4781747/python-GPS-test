# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 22:53:33 2018

@author: owo
"""

import numpy as np
import matplotlib.pyplot as plt 

S_event = 'Stationary_all'
#S_event = 'move_5'
#S_event_2 = 'move_6'

Ay_notatmo_llh = np.load('{0}_notatmsfree_llh_all.npy'.format(S_event))
Ay_notatmo_xyz = np.load('{0}_notatmsfree_xyz_all.npy'.format(S_event))
Ay_notatmo_enu = np.load('{0}_notatmsfree_enu_all.npy'.format(S_event))
Ay_notatmo_sate_num = np.load('{0}_notatmsfree_sate_num.npy'.format(S_event))
Ay_notatmo_time = np.load('{0}_notatmsfree_time.npy'.format(S_event))
Ay_notatmo_DOP = np.load('{0}_notatmsfree_DOP.npy'.format(S_event))

Ay_atmo_llh = np.load('{0}_atmsfree_llh_all.npy'.format(S_event))
Ay_atmo_xyz = np.load('{0}_atmsfree_xyz_all.npy'.format(S_event))
Ay_atmo_enu = np.load('{0}_atmsfree_enu_all.npy'.format(S_event))
Ay_atmo_sate_num = np.load('{0}_atmsfree_sate_num.npy'.format(S_event))
Ay_atmo_time = np.load('{0}_atmsfree_time.npy'.format(S_event))
Ay_atmo_DOP = np.load('{0}_atmsfree_DOP.npy'.format(S_event))

Ay_DGPS_llh = np.load('{0}_stableatmsfree_llh_all.npy'.format(S_event))
Ay_DGPS_xyz = np.load('{0}_stableatmsfree_xyz_all.npy'.format(S_event))
Ay_DGPS_enu = np.load('{0}_stableatmsfree_enu_all.npy'.format(S_event))
Ay_DGPS_sate_num = np.load('{0}_stableatmsfree_sate_num.npy'.format(S_event))
Ay_DGPS_time = np.load('{0}_stableatmsfree_time.npy'.format(S_event))
Ay_DGPS_DOP = np.load('{0}_stableatmsfree_DOP.npy'.format(S_event))
#
#Ay_notatmo_llh = np.concatenate((np.load('{0}_notatmsfree_llh_all.npy'.format(S_event)),np.load('{0}_notatmsfree_llh_all.npy'.format(S_event_2)) ))
#Ay_notatmo_xyz = np.concatenate((np.load('{0}_notatmsfree_xyz_all.npy'.format(S_event)),np.load('{0}_notatmsfree_xyz_all.npy'.format(S_event_2)) ))
#Ay_notatmo_enu = np.concatenate((np.load('{0}_notatmsfree_enu_all.npy'.format(S_event)),np.load('{0}_notatmsfree_enu_all.npy'.format(S_event_2)) ))
#Ay_notatmo_sate_num = np.concatenate((np.load('{0}_notatmsfree_sate_num.npy'.format(S_event)),np.load('{0}_notatmsfree_sate_num.npy'.format(S_event_2)) ))
#Ay_notatmo_time = np.concatenate((np.load('{0}_notatmsfree_time.npy'.format(S_event)),np.load('{0}_notatmsfree_time.npy'.format(S_event_2)) ))
#Ay_notatmo_DOP = np.concatenate((np.load('{0}_notatmsfree_DOP.npy'.format(S_event)),np.load('{0}_notatmsfree_DOP.npy'.format(S_event_2)) ),1)
#
#Ay_atmo_llh = np.concatenate((np.load('{0}_atmsfree_llh_all.npy'.format(S_event)),np.load('{0}_atmsfree_llh_all.npy'.format(S_event_2)) ))
#Ay_atmo_xyz = np.concatenate((np.load('{0}_atmsfree_xyz_all.npy'.format(S_event)),np.load('{0}_atmsfree_xyz_all.npy'.format(S_event_2)) ))
#Ay_atmo_enu = np.concatenate((np.load('{0}_atmsfree_enu_all.npy'.format(S_event)),np.load('{0}_atmsfree_enu_all.npy'.format(S_event_2)) ))
#Ay_atmo_sate_num = np.concatenate((np.load('{0}_atmsfree_sate_num.npy'.format(S_event)),np.load('{0}_atmsfree_sate_num.npy'.format(S_event_2)) ))
#Ay_atmo_time = np.concatenate((np.load('{0}_atmsfree_time.npy'.format(S_event)),np.load('{0}_atmsfree_time.npy'.format(S_event_2)) ))
#Ay_atmo_DOP = np.concatenate((np.load('{0}_atmsfree_DOP.npy'.format(S_event)),np.load('{0}_atmsfree_DOP.npy'.format(S_event_2)) ),1)
#
#Ay_DGPS_llh = np.concatenate((np.load('{0}_stableatmsfree_llh_all.npy'.format(S_event)),np.load('{0}_stableatmsfree_llh_all.npy'.format(S_event_2)) ))
#Ay_DGPS_xyz = np.concatenate((np.load('{0}_stableatmsfree_xyz_all.npy'.format(S_event)),np.load('{0}_stableatmsfree_xyz_all.npy'.format(S_event_2)) ))
#Ay_DGPS_enu = np.concatenate((np.load('{0}_stableatmsfree_enu_all.npy'.format(S_event)),np.load('{0}_stableatmsfree_enu_all.npy'.format(S_event_2)) ))
#Ay_DGPS_sate_num = np.concatenate((np.load('{0}_stableatmsfree_sate_num.npy'.format(S_event)),np.load('{0}_stableatmsfree_sate_num.npy'.format(S_event_2)) ))
#Ay_DGPS_time = np.concatenate((np.load('{0}_stableatmsfree_time.npy'.format(S_event)),np.load('{0}_stableatmsfree_time.npy'.format(S_event_2)) ))
#Ay_DGPS_DOP = np.concatenate((np.load('{0}_stableatmsfree_DOP.npy'.format(S_event)),np.load('{0}_stableatmsfree_DOP.npy'.format(S_event_2)) ),1)
##

plt.plot(Ay_notatmo_time,Ay_notatmo_sate_num)
plt.xlabel('LT')
plt.ylabel('num')
plt.title('num of satelite')
plt.savefig('{0}_notatmsfree_satenum.png'.format(S_event))
plt.clf()

        
#notatmo_ENU_std = np.std(Ay_notatmo_enu[np.where(Ay_notatmo_time>=10)[0],:],0)
#notatmo_ENU_mean = np.mean(Ay_notatmo_llh[np.where(Ay_notatmo_time>=10)[0],:],0)
#atmo_ENU_std = np.std(Ay_atmo_enu[np.where(Ay_notatmo_time>=10)[0],:],0)
#atmo_ENU_mean = np.mean(Ay_atmo_llh[np.where(Ay_notatmo_time>=10)[0],:],0)
#DGPSatmo_ENU_std = np.std(Ay_DGPS_enu[np.where(Ay_notatmo_time>=10)[0],:],0)
#DGPSatmo_ENU_mean = np.mean(Ay_DGPS_llh[np.where(Ay_notatmo_time>=10)[0],:],0)
#notatmo_ENU_std = np.std(Ay_notatmo_enu,0)
#notatmo_ENU_mean = np.mean(Ay_notatmo_llh,0)
#atmo_ENU_std = np.std(Ay_atmo_enu,0)
#atmo_ENU_mean = np.mean(Ay_atmo_llh,0)
#DGPSatmo_ENU_std = np.std(Ay_DGPS_enu,0)
#DGPSatmo_ENU_mean = np.mean(Ay_DGPS_llh,0)
notatmo_ENU_std = np.std(Ay_notatmo_enu,0)
notatmo_ENU_mean = np.mean(Ay_notatmo_llh,0)
atmo_ENU_std = np.std(Ay_atmo_enu,0)
atmo_ENU_mean = np.mean(Ay_atmo_llh,0)
DGPSatmo_ENU_std = np.std(Ay_DGPS_enu[np.where(Ay_DGPS_enu[:,0]>-999999999999999999)[0],:],0)
DGPSatmo_ENU_mean = np.mean(Ay_DGPS_llh[np.where(Ay_DGPS_llh[:,0]>-999999999999999999)[0],:],0)

plt.figure(2,figsize=(10,20))
plt.subplot(3,1,1)
notatmo_DOP = plt.plot(Ay_notatmo_time,Ay_notatmo_DOP[0,:],label='PDOP')
notatmo_DOP = plt.plot(Ay_notatmo_time,Ay_notatmo_DOP[1,:],label='TDOP')
notatmo_DOP = plt.plot(Ay_notatmo_time,Ay_notatmo_DOP[2,:],label='GDOP')
plt.legend()
plt.xlabel('LT')
plt.ylabel('m')
plt.title('not_atms-free_DOP')

plt.subplot(3,1,2)
atmo_DOP = plt.plot(Ay_atmo_time,Ay_atmo_DOP[0,:],label='PDOP')
atmo_DOP = plt.plot(Ay_atmo_time,Ay_atmo_DOP[1,:],label='TDOP')
atmo_DOP = plt.plot(Ay_atmo_time,Ay_atmo_DOP[2,:],label='GDOP')
plt.legend()
plt.xlabel('LT')
plt.ylabel('m')
plt.title('atms-free_DOP')

plt.subplot(3,1,3)
DGPS_DOP = plt.plot(Ay_notatmo_time,Ay_DGPS_DOP[0,:],label='PDOP')
DGPS_DOP = plt.plot(Ay_notatmo_time,Ay_DGPS_DOP[1,:],label='TDOP')
DGPS_DOP = plt.plot(Ay_notatmo_time,Ay_DGPS_DOP[2,:],label='GDOP')
plt.legend()
plt.xlabel('LT')
plt.ylabel('m')
plt.title('DGPS_DOP')
plt.savefig('{0}_DOP.png'.format(S_event))
plt.clf()

with open('{0}_atmofree_llh_googleearth.txt'.format(S_event),'w') as f:
    for i in range(len(Ay_atmo_llh)):
        f.write("{0},{1},{2}\n".format(Ay_atmo_llh[i,1],Ay_atmo_llh[i,0],Ay_atmo_llh[i,2]))
        
with open('{0}_notatmofree_llh_googleearth.txt'.format(S_event),'w') as f:
    for i in range(len(Ay_notatmo_llh)):
        f.write("{0},{1},{2}\n".format(Ay_notatmo_llh[i,1],Ay_notatmo_llh[i,0],Ay_notatmo_llh[i,2]))

with open('{0}_DGPS_llh_googleearth.txt'.format(S_event),'w') as f:
    for i in range(len(Ay_DGPS_llh)):
        f.write("{0},{1},{2}\n".format(Ay_DGPS_llh[i,1],Ay_DGPS_llh[i,0],Ay_DGPS_llh[i,2]))


#with open('{0}_atmofree_llh_googleearth.txt'.format(S_event),'w') as f:
#    for i in range(1415):
#        f.write("{0},{1},{2}\n".format(Ay_atmo_llh[i,1],Ay_atmo_llh[i,0],Ay_atmo_llh[i,2]))
#        
#with open('{0}_notatmofree_llh_googleearth.txt'.format(S_event),'w') as f:
#    for i in range(1415):
#        f.write("{0},{1},{2}\n".format(Ay_notatmo_llh[i,1],Ay_notatmo_llh[i,0],Ay_notatmo_llh[i,2]))
#
#with open('{0}_DGPS_llh_googleearth.txt'.format(S_event),'w') as f:
#    for i in range(1415):
#        f.write("{0},{1},{2}\n".format(Ay_DGPS_llh[i,1],Ay_DGPS_llh[i,0],Ay_DGPS_llh[i,2]))