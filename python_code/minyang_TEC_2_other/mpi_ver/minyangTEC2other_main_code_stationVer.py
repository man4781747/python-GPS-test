# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 21:26:06 2017

@author: owo
"""

import scipy.io
import numpy as np
import os
import sys
import minyangTEC2other_main_code_stationVer as miny2other
#import multiprocessing as mp

global S_yankai_data_path
S_yankai_data_path = "/pub3/man4781747/GPS_data/"

global S_minyang_data_path
S_minyang_data_path = "/nishome/man4781747/GPSTEC_minyan/gnsstec_v7.2/"

class minyangTEC2other:
    def __init__(self,S_data_name,I_year,I_doy,I_rate):
        self.S_data_name = S_data_name
        self.I_year = I_year
        self.I_doy = I_doy
        self.I_rate = I_rate
        self.S_nowinwhichSer = ''
        
    
    def minyang2phase(self):
        if os.path.exists(S_yankai_data_path+'data20{0:02d}{1:03d}/phase_data'.format(self.I_year,self.I_doy)) == False:
            os.makedirs(S_yankai_data_path+'data20{0:02d}{1:03d}/phase_data'.format(self.I_year,self.I_doy))   
        if os.path.exists(S_yankai_data_path+'data20{0:02d}{1:03d}/phase_data/{2}s'.format(self.I_year,self.I_doy,self.I_rate)) == False:
            os.makedirs(S_yankai_data_path+'data20{0:02d}{1:03d}/phase_data/{2}s'.format(self.I_year,self.I_doy,self.I_rate))    
        try:
            I_array_long = 2880
            if self.I_rate == 1:
                I_array_long = 2880*30
            
            data_base_L1 = np.zeros((I_array_long,32+26))
            data_base_L2 = np.zeros((I_array_long,32+26))
            data_base_P2 = np.zeros((I_array_long,32+26))
            data_base_C1 = np.zeros((I_array_long,32+26))       
            data_base_time = np.zeros((I_array_long,12))
    
            data_local_GPS = S_minyang_data_path+"OBS/gps/20{0:02d}.{1:03d}/{3}s/{2}{1:03d}0.mat".format(self.I_year,self.I_doy,self.S_data_name,self.I_rate)
            if os.path.isfile(data_local_GPS):
#                print('test_1')
                data_L1 = scipy.io.loadmat(data_local_GPS)['L1']
                data_L2 = scipy.io.loadmat(data_local_GPS)['L2']
                data_P2 = scipy.io.loadmat(data_local_GPS)['P2']
                data_C1 = scipy.io.loadmat(data_local_GPS)['C1']
                data_hr = scipy.io.loadmat(data_local_GPS)['hour']
                data_minute = scipy.io.loadmat(data_local_GPS)['minute']
                data_sec = scipy.io.loadmat(data_local_GPS)['second']
                data_yr = scipy.io.loadmat(data_local_GPS)['year']
                data_day = scipy.io.loadmat(data_local_GPS)['day']
                data_month = scipy.io.loadmat(data_local_GPS)['month']
                ###                
                data_base_L1[:len(np.matrix(data_L1.toarray())[:,0]),:32] = np.matrix(data_L1.toarray())
                data_base_L2[:len(np.matrix(data_L1.toarray())[:,0]),:32] = np.matrix(data_L2.toarray())
                data_base_P2[:len(np.matrix(data_L1.toarray())[:,0]),:32] = np.matrix(data_P2.toarray())
                data_base_C1[:len(np.matrix(data_L1.toarray())[:,0]),:32] = np.matrix(data_C1.toarray())  

#                print(np.shape(data_minute[:,0]))
#                print(np.shape(data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),0]))
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),0] = data_yr[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),1] = data_month[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),2] = data_day[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),3] = data_hr[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),4] = data_minute[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),5] = data_sec[:,0]

#                x = 0
#                while x < len(data_hr):
#                    data_local = int(round(((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/(self.I_rate/60.))[0]))
#                    data_base_L1[data_local:data_local+1,0:32] = np.matrix(data_L1[x].toarray())
#                    data_base_L2[data_local:data_local+1,0:32] = np.matrix(data_L2[x].toarray())
#                    data_base_P2[data_local:data_local+1,0:32] = np.matrix(data_P2[x].toarray())
#                    data_base_C1[data_local:data_local+1,0:32] = np.matrix(data_C1[x].toarray())
#                    x += 1 
            data_local_GLONASS = S_minyang_data_path+"OBS/glonass/20{0:02d}.{1:03d}/{3}s/{2}{1:03d}0.mat".format(self.I_year,self.I_doy,self.S_data_name,self.I_rate)
            if os.path.isfile(data_local_GLONASS):            
                data_L1 = scipy.io.loadmat(data_local_GLONASS)['L1']
                data_L2 = scipy.io.loadmat(data_local_GLONASS)['L2']
                data_P2 = scipy.io.loadmat(data_local_GLONASS)['P2']
                data_C1 = scipy.io.loadmat(data_local_GLONASS)['C1']
                data_hr = scipy.io.loadmat(data_local_GLONASS)['hour']
                data_minute = scipy.io.loadmat(data_local_GLONASS)['minute']
                data_sec = scipy.io.loadmat(data_local_GLONASS)['second']
                data_yr = scipy.io.loadmat(data_local_GLONASS)['year']
                data_day = scipy.io.loadmat(data_local_GLONASS)['day']
                data_month = scipy.io.loadmat(data_local_GLONASS)['month']
#                print('test4')
#                print(np.shape(np.matrix(data_L1.toarray())))
#                print(np.shape(data_base_L1[:len(np.matrix(data_L1.toarray())[:,0]),32:]))
                ###                
                data_base_L1[:len(np.matrix(data_L1.toarray())[:,0]),32:] = np.matrix(data_L1.toarray())
                data_base_L2[:len(np.matrix(data_L1.toarray())[:,0]),32:] = np.matrix(data_L2.toarray())
                data_base_P2[:len(np.matrix(data_L1.toarray())[:,0]),32:] = np.matrix(data_P2.toarray())
                data_base_C1[:len(np.matrix(data_L1.toarray())[:,0]),32:] = np.matrix(data_C1.toarray())  
#                print('test2')
##                print(data_minute[:])
##                print(np.shape(data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),0]))
#                
#                print(np.shape(data_yr[:,0]))
#                print(np.shape(data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),6]))
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),6] = data_yr[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),7] = data_month[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),8] = data_day[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),9] = data_hr[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),10] = data_minute[:,0]
                data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),11] = data_sec[:,0]
                
                
#                x = 0
#                while x < len(data_hr):
#                    data_local = int(round(((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/(self.I_rate/60.))[0]))
#                    data_base_L1[data_local:data_local+1,32:32+26] = np.matrix(data_L1[x].toarray())
#                    data_base_L2[data_local:data_local+1,32:32+26] = np.matrix(data_L2[x].toarray())
#                    data_base_P2[data_local:data_local+1,32:32+26] = np.matrix(data_P2[x].toarray())
#                    data_base_C1[data_local:data_local+1,32:32+26] = np.matrix(data_C1[x].toarray())
#                    x += 1 
            save_dir = S_yankai_data_path+'data20{0:02d}{1:03d}/phase_data/{2}s/'.format(self.I_year,self.I_doy,self.I_rate)
            S_save_name_base = "{0}{1:02d}{2:03d}".format(self.S_data_name,self.I_year,self.I_doy)
#            print(len(np.matrix(data_L1.toarray())[:,0]))
            np.save("{0}{1}phaseL1.npy".format(save_dir,S_save_name_base),data_base_L1[:len(np.matrix(data_L1.toarray())[:,0]),:])
            np.save("{0}{1}phaseL2.npy".format(save_dir,S_save_name_base),data_base_L2[:len(np.matrix(data_L1.toarray())[:,0]),:])
            np.save("{0}{1}phaseP2.npy".format(save_dir,S_save_name_base),data_base_P2[:len(np.matrix(data_L1.toarray())[:,0]),:])
            np.save("{0}{1}phaseC1.npy".format(save_dir,S_save_name_base),data_base_C1[:len(np.matrix(data_L1.toarray())[:,0]),:])  
            np.save("{0}{1}phasetime.npy".format(save_dir,S_save_name_base),data_base_time[:len(np.matrix(data_L1.toarray())[:,0]),:])  
#            print('phase test')
            return None
        except:
            print("{0}{1:02d}{2:03d}phase.npy error!!".format(self.S_data_name,self.I_year,self.I_doy))
            return "{0}{1:02d}{2:03d}phase.npy error!!".format(self.S_data_name,self.I_year,self.I_doy)

    def minyang2aeosv(self):
        if os.path.exists(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data'.format(self.I_year,self.I_doy)) == False:
            os.makedirs(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data'.format(self.I_year,self.I_doy))   
        if os.path.exists(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data/{2}s'.format(self.I_year,self.I_doy,self.I_rate)) == False:
            os.makedirs(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data/{2}s'.format(self.I_year,self.I_doy,self.I_rate))    
        try:    
            I_array_long = 2880
            if self.I_rate == 1:
                I_array_long = 2880*30

            a_data_array = np.zeros((I_array_long,32+26))
            o_data_array = np.zeros((I_array_long,32+26))
            v_data_array = np.zeros((I_array_long,32+26))
            e_data_array = np.zeros((I_array_long,32+26))
            s_data_array = np.zeros((I_array_long,32+26))
            
            data_local_GPS = S_yankai_data_path+"minyangVer/GPS/20{0:02d}.{1:03d}/{3}s/{2}{1:03d}.mat".format(self.I_year,self.I_doy,self.S_data_name,self.I_rate)
            if os.path.isfile(data_local_GPS):
                data_a = scipy.io.loadmat(data_local_GPS)['a{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_o = scipy.io.loadmat(data_local_GPS)['o{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_v = scipy.io.loadmat(data_local_GPS)['v{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_e = scipy.io.loadmat(data_local_GPS)['e{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_s = scipy.io.loadmat(data_local_GPS)['s{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_base_a = np.matrix(data_a.toarray())
                data_base_o = np.matrix(data_o.toarray())
                data_base_v = np.matrix(data_v.toarray())
                data_base_e = np.matrix(data_e.toarray())
                data_base_s = np.matrix(data_s.toarray())
                a_data_array[:,0:32] = data_base_a
                o_data_array[:,0:32] = data_base_o
                v_data_array[:,0:32] = data_base_v
                e_data_array[:,0:32] = data_base_e
                s_data_array[:,0:32] = data_base_s
            else:
#                    print('!!! {0} dont have GPS data?'.format(self.S_data_name))
                pass
#                    print(data_local_GPS)
            data_local_GLONASS = S_yankai_data_path+"minyangVer/GLONASS/20{0:02d}.{1:03d}/{3}s/{2}{1:03d}.mat".format(self.I_year,self.I_doy,self.S_data_name,self.I_rate)
            if os.path.isfile(data_local_GLONASS):            
                data_a = scipy.io.loadmat(data_local_GLONASS)['a{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_o = scipy.io.loadmat(data_local_GLONASS)['o{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_v = scipy.io.loadmat(data_local_GLONASS)['v{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_e = scipy.io.loadmat(data_local_GLONASS)['e{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_s = scipy.io.loadmat(data_local_GLONASS)['s{0}{1:03d}'.format(self.S_data_name,self.I_doy)]
                data_base_a = np.matrix(data_a.toarray())
                data_base_o = np.matrix(data_o.toarray())
                data_base_v = np.matrix(data_v.toarray())
                data_base_e = np.matrix(data_e.toarray())
                data_base_s = np.matrix(data_s.toarray())
                a_data_array[:,32:58] = data_base_a
                o_data_array[:,32:58] = data_base_o
                v_data_array[:,32:58] = data_base_v
                e_data_array[:,32:58] = data_base_e
                s_data_array[:,32:58] = data_base_s
            else:
#                    print('!!! {0} dont have GLONASS data?'.format(self.S_data_name))
#                    print(data_local_GLONASS)
                pass
            
            S_save_data_name_base = "{0}{1:03d}".format(self.S_data_name,self.I_doy)
            np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/a{2}.npy".format(self.I_year,self.I_doy,S_save_data_name_base,self.I_rate),a_data_array)
            np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/o{2}.npy".format(self.I_year,self.I_doy,S_save_data_name_base,self.I_rate),o_data_array)
            np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/v{2}.npy".format(self.I_year,self.I_doy,S_save_data_name_base,self.I_rate),v_data_array)
            np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/e{2}.npy".format(self.I_year,self.I_doy,S_save_data_name_base,self.I_rate),e_data_array)
            np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/s{2}.npy".format(self.I_year,self.I_doy,S_save_data_name_base,self.I_rate),s_data_array)
#                print('aeosv test')
            return None
        except:
            print("a{0}{1:03d}.npy error!!".format(self.S_data_name,self.I_doy))
            return "a{0}{1:03d}.npy error!!".format(self.S_data_name,self.I_doy)

if __name__ == '__main__':    
    '''
    EX: 
      python3.5 minyangTEC2other_main_code_stationVer.py 15 73 aknd 30
    '''


    I_year = int(sys.argv[1])
    I_doy = int(sys.argv[2])
    S_stataion_chose = str(sys.argv[3])
    I_rate = int(sys.argv[4])

    Mobj_miny2other = miny2other.minyangTEC2other(S_stataion_chose,I_year,I_doy,I_rate)
    Mobj_miny2other.minyang2aeosv()
    Mobj_miny2other.minyang2phase()


    