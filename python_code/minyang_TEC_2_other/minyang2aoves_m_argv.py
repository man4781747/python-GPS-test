# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 17:50:04 2017

@author: Chuanping_LASC_PC
"""

import scipy.io
import numpy as np
import os
import multiprocessing as mp
import sys

def job(data_num,data_name,year,day,I_data_rate):  
    try:    
        isfile_test = 0
        I_array_long = 2880
        if I_data_rate == 1:
            I_array_long = 2880*30
        if os.path.isfile("a{0}.npy".format(data_name[0:7])):
            isfile_test = 1
        if isfile_test == 0:
            a_data_array = np.zeros((I_array_long,32+26))
            o_data_array = np.zeros((I_array_long,32+26))
            v_data_array = np.zeros((I_array_long,32+26))
            e_data_array = np.zeros((I_array_long,32+26))
            s_data_array = np.zeros((I_array_long,32+26))
            
            data_local_GPS = "./GPS/20{0:02d}.{1:03d}/{3}s/{2}".format(year,day,data_name,I_data_rate)
            if os.path.isfile(data_local_GPS):
                data_a = scipy.io.loadmat(data_local_GPS)['a{0}'.format(data_name[0:7])]
                data_o = scipy.io.loadmat(data_local_GPS)['o{0}'.format(data_name[0:7])]
                data_v = scipy.io.loadmat(data_local_GPS)['v{0}'.format(data_name[0:7])]
                data_e = scipy.io.loadmat(data_local_GPS)['e{0}'.format(data_name[0:7])]
                data_s = scipy.io.loadmat(data_local_GPS)['s{0}'.format(data_name[0:7])]
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
                print('!!! {0} dont have GPS data?'.format(data_name))
                
            data_local_GLONASS = "./GLONASS/20{0:02d}.{1:03d}/{3}s/{2}".format(year,day,data_name,I_data_rate)
            if os.path.isfile(data_local_GLONASS):            
                data_a = scipy.io.loadmat(data_local_GLONASS)['a{0}'.format(data_name[0:7])]
                data_o = scipy.io.loadmat(data_local_GLONASS)['o{0}'.format(data_name[0:7])]
                data_v = scipy.io.loadmat(data_local_GLONASS)['v{0}'.format(data_name[0:7])]
                data_e = scipy.io.loadmat(data_local_GLONASS)['e{0}'.format(data_name[0:7])]
                data_s = scipy.io.loadmat(data_local_GLONASS)['s{0}'.format(data_name[0:7])]
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
                print('!!! {0} dont have GLONASS data?'.format(data_name))
                            
            np.save("../data20{0:02d}{1:03d}/aeosv_data/{3}s/a{2}.npy".format(year,day,data_name[0:7],I_data_rate),a_data_array)
            np.save("../data20{0:02d}{1:03d}/aeosv_data/{3}s/o{2}.npy".format(year,day,data_name[0:7],I_data_rate),o_data_array)
            np.save("../data20{0:02d}{1:03d}/aeosv_data/{3}s/v{2}.npy".format(year,day,data_name[0:7],I_data_rate),v_data_array)
            np.save("../data20{0:02d}{1:03d}/aeosv_data/{3}s/e{2}.npy".format(year,day,data_name[0:7],I_data_rate),e_data_array)
            np.save("../data20{0:02d}{1:03d}/aeosv_data/{3}s/s{2}.npy".format(year,day,data_name[0:7],I_data_rate),s_data_array)
        return None
    except:
        return data_name
#def job_test(data_num,data_name):
#    print "OK"
#    return data_num
def multucore(data_list,year,day,I_data_rate):
#    print 'ml'
    pool = mp.Pool(processes=processes_num)
#    print 'go'
#    multi_res = [pool.apply_async(job,(data_name,)) for data_name in data_list ]
#    print [res.get() for res in multi_res]
    
    res = [pool.apply_async(job, (i,data_list.pop(),year,day,I_data_rate)) for i in range(len(data_list))]
    print([R.get() for R in res])
if __name__ == '__main__':
    import time
    
    t1 = time.time()
    
    year = int(sys.argv[1])
    doy = int(sys.argv[2])
    processes_num = int(sys.argv[3])
    I_data_rate = int(sys.argv[4])

    
    if os.path.exists('./data20{0:02d}{1:03d}/aeosv_data/{2}s'.format(year,doy,I_data_rate)) == False:
        os.makedirs('./data20{0:02d}{1:03d}/aeosv_data/{2}s'.format(year,doy,I_data_rate))    

    os.chdir('./minyangVer/GPS/20{0:02d}.{1:03d}/{2}s'.format(year,doy,I_data_rate))
#    os.chdir('./20{0}.{1}'.format(year,day))
    data_list_GPS = []
    for filenames in os.listdir('.'): 
        if os.path.isfile(filenames):
            if filenames[8:12] == "mat":
                data_list_GPS.append(filenames)
    os.chdir('../../../GLONASS/20{0:02d}.{1:03d}/{2}s'.format(year,doy,I_data_rate))            
    data_list_GLONASS = []
    for filenames in os.listdir('.'): 
        if os.path.isfile(filenames):
            if filenames[8:12] == "mat":
                data_list_GLONASS.append(filenames)   
    os.chdir('../../..')     
    
    data_list = set(data_list_GPS)|set(data_list_GLONASS)
   
    print(len(data_list))
 
    multucore(data_list,year,doy,I_data_rate)
    
    t2 = time.time()
    print(t2-t1)
