# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 16:15:12 2017

@author: Chuanping_LASC_PC
"""

import scipy.io
import numpy as np
import os
import sys
import multiprocessing as mp

def job(data_num,data_name,year,day,I_data_rate):      
#    for data_name in data_list:
#    print '{0}'.format(data_name)
    try:
#        print(data_name)
#        print(data_num)
#        print(os.getcwd())
        I_array_long = 2880
        if I_data_rate == 1:
            I_array_long = 2880*30
        
        data_base_L1 = np.zeros((I_array_long,32+26))
        data_base_L2 = np.zeros((I_array_long,32+26))
#        data_base_P1 = np.zeros((2880,32+26))
        data_base_P2 = np.zeros((I_array_long,32+26))
        data_base_C1 = np.zeros((I_array_long,32+26))        
        

        data_local_GPS = "./gps/20{0:02d}.{1:03d}/{3}s/{2}".format(year,day,data_name,I_data_rate)
#        print(data_local_GPS)
        if os.path.isfile(data_local_GPS):
            data_L1 = scipy.io.loadmat(data_local_GPS)['L1']
            data_L2 = scipy.io.loadmat(data_local_GPS)['L2']
#            data_P1 = scipy.io.loadmat(data_local_GPS)['P1']
            data_P2 = scipy.io.loadmat(data_local_GPS)['P2']
            data_C1 = scipy.io.loadmat(data_local_GPS)['C1']
            data_hr = scipy.io.loadmat(data_local_GPS)['hour']
            data_minute = scipy.io.loadmat(data_local_GPS)['minute']
            data_sec = scipy.io.loadmat(data_local_GPS)['second']
            x = 0
            while x < len(data_hr):
#                print(x)
                data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/(I_data_rate/60.))
                data_base_L1[data_local:data_local+1,0:32] = np.matrix(data_L1[x].toarray())
                data_base_L2[data_local:data_local+1,0:32] = np.matrix(data_L2[x].toarray())
#                data_base_P1[0:32,data_local] = np.matrix(data_P1[x].toarray())
                data_base_P2[data_local:data_local+1,0:32] = np.matrix(data_P2[x].toarray())
                data_base_C1[data_local:data_local+1,0:32] = np.matrix(data_C1[x].toarray())
                x += 1 
                
        data_local_GLONASS = "./glonass/20{0:02d}.{1:03d}/{3}s/{2}".format(year,day,data_name,I_data_rate)
        if os.path.isfile(data_local_GLONASS):            
            data_L1 = scipy.io.loadmat(data_local_GLONASS)['L1']
            data_L2 = scipy.io.loadmat(data_local_GLONASS)['L2']
#            data_P1 = scipy.io.loadmat(data_local_GLONASS)['P1']
            data_P2 = scipy.io.loadmat(data_local_GLONASS)['P2']
            data_C1 = scipy.io.loadmat(data_local_GLONASS)['C1']
            data_hr = scipy.io.loadmat(data_local_GLONASS)['hour']
            data_minute = scipy.io.loadmat(data_local_GLONASS)['minute']
            data_sec = scipy.io.loadmat(data_local_GLONASS)['second']
            x = 0
            while x < len(data_hr):
                data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/(I_data_rate/60.))
                data_base_L1[data_local:data_local+1,32:32+26] = np.matrix(data_L1[x].toarray())
                data_base_L2[data_local:data_local+1,32:32+26] = np.matrix(data_L2[x].toarray())
#                data_base_P1[0:32,data_local] = np.matrix(data_P1[x].toarray())
                data_base_P2[data_local:data_local+1,32:32+26] = np.matrix(data_P2[x].toarray())
                data_base_C1[data_local:data_local+1,32:32+26] = np.matrix(data_C1[x].toarray())
                x += 1 
        
        save_dir = '../../../python/Odata/data20{0:02d}{1:03d}/phase_data/{2}s/'.format(year,day,I_data_rate)
#        print('save')
    #    save_dir = '../phase_data/'.format(year,day)    
#        print(save_dir)    
        np.save("{0}{1}{2}{3}phaseL1.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_L1)
        np.save("{0}{1}{2}{3}phaseL2.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_L2)
#        np.save("{0}{1}{2}{3}phaseP1.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_P1)
        np.save("{0}{1}{2}{3}phaseP2.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_P2)
        np.save("{0}{1}{2}{3}phaseC1.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_C1)      
#    except:
#        print data_name
        return None
    except:
        data_name


def multucore(data_list,year,day,I_data_rate):
#    print 'ml'
    pool = mp.Pool(processes=processes_num)
#    print 'go'
#    multi_res = [pool.apply_async(job,(data_name,)) for data_name in data_list ]
#    print [res.get() for res in multi_res]
#    print('taaaaaaaaaa {0}'.format(len(data_list)))
    res = [pool.apply_async(job, (i,data_list.pop(),year,day,I_data_rate)) for i in range(len(data_list))]
#    print(len(res))
    print([R.get() for R in res])
if __name__ == '__main__':
    import time
    
    t1 = time.time()
    
    year = int(sys.argv[1])
    doy = int(sys.argv[2])
    processes_num = int(sys.argv[3])
    I_data_rate = int(sys.argv[4])

    
    if os.path.exists('./data20{0:02d}{1:03d}/phase_data/{2}s'.format(year,doy,I_data_rate)) == False:
        os.makedirs('./data20{0:02d}{1:03d}/phase_data/{2}s'.format(year,doy,I_data_rate))    
    
    os.chdir('../../GPSTEC_minyan/gnsstec_v7.2/OBS/gps/20{0:02d}.{1:03d}/{2}s'.format(year,doy,I_data_rate))
    
    data_list_GPS = []
    for filenames in os.listdir('.'): 
        if os.path.isfile(filenames):
            if filenames[9:13] == "mat":
                data_list_GPS.append(filenames)
                
    os.chdir('../../../glonass/20{0:02d}.{1:03d}/{2}s'.format(year,doy,I_data_rate))
    data_list_glonass = []
    for filenames in os.listdir('.'): 
        if os.path.isfile(filenames):
            if filenames[9:13] == "mat":
                data_list_glonass.append(filenames)
    
    os.chdir('../../..')
    
    data_list = set(data_list_GPS)|set(data_list_glonass)
    
    multucore(data_list,year,doy,I_data_rate)
    
    t2 = time.time()
    print (t2-t1)