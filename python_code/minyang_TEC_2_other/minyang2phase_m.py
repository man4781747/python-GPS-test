# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 16:15:12 2017

@author: Chuanping_LASC_PC
"""

import scipy.io
import numpy as np
import os

import multiprocessing as mp

def job(data_num,data_name,year,day):      
#    for data_name in data_list:
#    print '{0}'.format(data_name)
#    try:
        data_base_L1 = np.zeros((2880,32+26))
        data_base_L2 = np.zeros((2880,32+26))
#        data_base_P1 = np.zeros((2880,32+26))
        data_base_P2 = np.zeros((2880,32+26))
        data_base_C1 = np.zeros((2880,32+26))        
        

        data_local_GPS = "./gps/20{0}.{1}/{2}".format(year,day,data_name)
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
                data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/0.5)
                data_base_L1[0:32,data_local:data_local+1] = np.matrix(data_L1[x].toarray()).T
                data_base_L2[0:32,data_local:data_local+1] = np.matrix(data_L2[x].toarray()).T
#                data_base_P1[0:32,data_local] = np.matrix(data_P1[x].toarray())
                data_base_P2[0:32,data_local:data_local+1] = np.matrix(data_P2[x].toarray()).T
                data_base_C1[0:32,data_local:data_local+1] = np.matrix(data_C1[x].toarray()).T
                x += 1 
                
        data_local_GLONASS = "./glonass/20{0}.{1}/{2}".format(year,day,data_name)
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
                data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/0.5)
                data_base_L1[32:32+26,data_local:data_local+1] = np.matrix(data_L1[x].toarray()).T
                data_base_L2[32:32+26,data_local:data_local+1] = np.matrix(data_L2[x].toarray()).T
#                data_base_P1[0:32,data_local] = np.matrix(data_P1[x].toarray())
                data_base_P2[32:32+26,data_local:data_local+1] = np.matrix(data_P2[x].toarray()).T
                data_base_C1[32:32+26,data_local:data_local+1] = np.matrix(data_C1[x].toarray()).T
                x += 1 
        
        save_dir = '../../../python/Odata/data20{0}{1}/phase_data/'.format(year,day)
    #    print 'save'
    #    save_dir = '../phase_data/'.format(year,day)        
        np.save("{0}{1}{2}{3}phaseL1.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_L1)
        np.save("{0}{1}{2}{3}phaseL2.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_L2)
#        np.save("{0}{1}{2}{3}phaseP1.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_P1)
        np.save("{0}{1}{2}{3}phaseP2.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_P2)
        np.save("{0}{1}{2}{3}phaseC1.npy".format(save_dir,data_name[0:4],year,data_name[4:7]),data_base_C1)      
#    except:
#        print data_name
        return data_name

def job_test(data_num,data_name):
    print "OK"
    return data_num
def multucore(data_list,year,day):
#    print 'ml'
    pool = mp.Pool(processes=processes_num)
#    print 'go'
#    multi_res = [pool.apply_async(job,(data_name,)) for data_name in data_list ]
#    print [res.get() for res in multi_res]
    
    res = [pool.apply_async(job, (i,data_list.pop(),year,day)) for i in range(len(data_list))]
    print [R.get() for R in res]
if __name__ == '__main__':
    import time
    
    t1 = time.time()
    year = input("year(str):")
    day  = input("day(str):")
    
    processes_num = int(input("processes_num(str):"))
    
if os.path.exists('./data20{0}{1}/phase_data'.format(year,day)) == False:
    os.makedirs('./data20{0}{1}/phase_data'.format(year,day))    

#    year = '03'
#    day  = '302'
    
#    processes_num = int('4')
os.chdir('../../GPSTEC_minyan/gnsstec_v7.2/OBS/gps/20{0}.{1}'.format(year,day))

data_list_GPS = []
for filenames in os.listdir('.'): 
    if os.path.isfile(filenames):
        if filenames[9:13] == "mat":
            data_list_GPS.append(filenames)
            
os.chdir('../../glonass/20{0}.{1}'.format(year,day))
data_list_glonass = []
for filenames in os.listdir('.'): 
    if os.path.isfile(filenames):
        if filenames[9:13] == "mat":
            data_list_glonass.append(filenames)

os.chdir('../..')

data_list = set(data_list_GPS)|set(data_list_glonass)
print len(data_list)

multucore(data_list,year,day)

t2 = time.time()
print t2-t1