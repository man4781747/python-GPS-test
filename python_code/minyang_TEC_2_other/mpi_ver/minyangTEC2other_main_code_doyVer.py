# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 21:26:06 2017

@author: owo
"""

import scipy.io
import numpy as np
import os
import time
import sys
import minyangTEC2other_main_code_stationVer as miny2other
import multiprocessing as mp

global S_yankai_data_path
S_yankai_data_path = "/pub3/man4781747/GPS_data/"

global S_minyang_data_path
S_minyang_data_path = "/nishome/man4781747/GPSTEC_minyan/gnsstec_v7.2/"


def job(S_data_name,I_year,I_doy,I_rate):
    miny2other_main = miny2other.minyangTEC2other(S_data_name,I_year,I_doy,I_rate)
#    Lst_2phase_ans.append(miny2other_main.minyang2phase())
#    Lst_2aeosv_ans.append(miny2other_main.minyang2aeosv())
    return (miny2other_main.minyang2phase(),miny2other_main.minyang2aeosv())
    
class multucore:
    def __init__(self,Lst_data_name,I_year,I_doy,I_rate,I_processes_num):
        pool = mp.Pool(processes=I_processes_num)
#        print(Lst_data_name)
        res = [pool.apply_async(job, (Lst_data_name[i],I_year,I_doy,I_rate)) for i in range(len(Lst_data_name))]
        print([R.get() for R in res])


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
            
    
            data_local_GPS = S_minyang_data_path+"OBS/gps/20{0:02d}.{1:03d}/{3}s/{2}".format(self.I_year,self.I_doy,self.S_data_name,self.I_rate)
            if os.path.isfile(data_local_GPS):
                data_L1 = scipy.io.loadmat(data_local_GPS)['L1']
                data_L2 = scipy.io.loadmat(data_local_GPS)['L2']
                data_P2 = scipy.io.loadmat(data_local_GPS)['P2']
                data_C1 = scipy.io.loadmat(data_local_GPS)['C1']
                data_hr = scipy.io.loadmat(data_local_GPS)['hour']
                data_minute = scipy.io.loadmat(data_local_GPS)['minute']
                data_sec = scipy.io.loadmat(data_local_GPS)['second']
                x = 0
                while x < len(data_hr):
                    data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/(self.I_rate/60.))
                    data_base_L1[data_local:data_local+1,0:32] = np.matrix(data_L1[x].toarray())
                    data_base_L2[data_local:data_local+1,0:32] = np.matrix(data_L2[x].toarray())
                    data_base_P2[data_local:data_local+1,0:32] = np.matrix(data_P2[x].toarray())
                    data_base_C1[data_local:data_local+1,0:32] = np.matrix(data_C1[x].toarray())
                    x += 1 
                    
            data_local_GLONASS = S_minyang_data_path+"OBS/glonass/20{0:02d}.{1:03d}/{3}s/{2}".format(self.I_year,self.I_doy,self.S_data_name,self.I_rate)
            if os.path.isfile(data_local_GLONASS):            
                data_L1 = scipy.io.loadmat(data_local_GLONASS)['L1']
                data_L2 = scipy.io.loadmat(data_local_GLONASS)['L2']
                data_P2 = scipy.io.loadmat(data_local_GLONASS)['P2']
                data_C1 = scipy.io.loadmat(data_local_GLONASS)['C1']
                data_hr = scipy.io.loadmat(data_local_GLONASS)['hour']
                data_minute = scipy.io.loadmat(data_local_GLONASS)['minute']
                data_sec = scipy.io.loadmat(data_local_GLONASS)['second']
                x = 0
                while x < len(data_hr):
                    data_local = int((data_hr[x]*60.+data_minute[x]+data_sec[x]/60.)/(self.I_rate/60.))
                    data_base_L1[data_local:data_local+1,32:32+26] = np.matrix(data_L1[x].toarray())
                    data_base_L2[data_local:data_local+1,32:32+26] = np.matrix(data_L2[x].toarray())
                    data_base_P2[data_local:data_local+1,32:32+26] = np.matrix(data_P2[x].toarray())
                    data_base_C1[data_local:data_local+1,32:32+26] = np.matrix(data_C1[x].toarray())
                    x += 1 
            
            save_dir = S_yankai_data_path+'data20{0:02d}{1:03d}/phase_data/{2}s/'.format(self.I_year,self.I_doy,self.I_rate)
  
            np.save("{0}{1}{2}{3}phaseL1.npy".format(save_dir,self.S_data_name[0:4],self.I_year,self.S_data_name[4:7]),data_base_L1)
            np.save("{0}{1}{2}{3}phaseL2.npy".format(save_dir,self.S_data_name[0:4],self.I_year,self.S_data_name[4:7]),data_base_L2)
            np.save("{0}{1}{2}{3}phaseP2.npy".format(save_dir,self.S_data_name[0:4],self.I_year,self.S_data_name[4:7]),data_base_P2)
            np.save("{0}{1}{2}{3}phaseC1.npy".format(save_dir,self.S_data_name[0:4],self.I_year,self.S_data_name[4:7]),data_base_C1)  
#            print('phase test')
            return None
        except:
            print("{0}{1}{2}phase.npy error!!".format(self.S_data_name[0:4],self.I_year,self.S_data_name[4:7]))
            return "{0}{1}{2}phase.npy error!!".format(self.S_data_name[0:4],self.I_year,self.S_data_name[4:7])

    def minyang2aeosv(self):
        if os.path.exists(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data'.format(self.I_year,self.I_doy)) == False:
            os.makedirs(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data'.format(self.I_year,self.I_doy))   
        if os.path.exists(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data/{2}s'.format(self.I_year,self.I_doy,self.I_rate)) == False:
            os.makedirs(S_yankai_data_path+'data20{0:02d}{1:03d}/aeosv_data/{2}s'.format(self.I_year,self.I_doy,self.I_rate))    
        try:    
            isfile_test = 0
            I_array_long = 2880
            if self.I_rate == 1:
                I_array_long = 2880*30
            if os.path.isfile("a{0}.npy".format(self.S_data_name[0:7])):
                isfile_test = 1
                print("a{0}.npy existed!!".format(self.S_data_name[0:7]))
                return "a{0}.npy existed!!".format(self.S_data_name[0:7])
            if isfile_test == 0:
                a_data_array = np.zeros((I_array_long,32+26))
                o_data_array = np.zeros((I_array_long,32+26))
                v_data_array = np.zeros((I_array_long,32+26))
                e_data_array = np.zeros((I_array_long,32+26))
                s_data_array = np.zeros((I_array_long,32+26))
                
                data_local_GPS = S_yankai_data_path+"minyangVer/GPS/20{0:02d}.{1:03d}/{3}s/{2}".format(self.I_year,self.I_doy,self.S_data_name[:7]+'.mat',self.I_rate)
                if os.path.isfile(data_local_GPS):
                    data_a = scipy.io.loadmat(data_local_GPS)['a{0}'.format(self.S_data_name[0:7])]
                    data_o = scipy.io.loadmat(data_local_GPS)['o{0}'.format(self.S_data_name[0:7])]
                    data_v = scipy.io.loadmat(data_local_GPS)['v{0}'.format(self.S_data_name[0:7])]
                    data_e = scipy.io.loadmat(data_local_GPS)['e{0}'.format(self.S_data_name[0:7])]
                    data_s = scipy.io.loadmat(data_local_GPS)['s{0}'.format(self.S_data_name[0:7])]
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
                    
                data_local_GLONASS = S_yankai_data_path+"minyangVer/GLONASS/20{0:02d}.{1:03d}/{3}s/{2}".format(self.I_year,self.I_doy,self.S_data_name[:7]+'.mat',self.I_rate)
                if os.path.isfile(data_local_GLONASS):            
                    data_a = scipy.io.loadmat(data_local_GLONASS)['a{0}'.format(self.S_data_name[0:7])]
                    data_o = scipy.io.loadmat(data_local_GLONASS)['o{0}'.format(self.S_data_name[0:7])]
                    data_v = scipy.io.loadmat(data_local_GLONASS)['v{0}'.format(self.S_data_name[0:7])]
                    data_e = scipy.io.loadmat(data_local_GLONASS)['e{0}'.format(self.S_data_name[0:7])]
                    data_s = scipy.io.loadmat(data_local_GLONASS)['s{0}'.format(self.S_data_name[0:7])]
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
                                
                np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/a{2}.npy".format(self.I_year,self.I_doy,self.S_data_name[0:7],self.I_rate),a_data_array)
                np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/o{2}.npy".format(self.I_year,self.I_doy,self.S_data_name[0:7],self.I_rate),o_data_array)
                np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/v{2}.npy".format(self.I_year,self.I_doy,self.S_data_name[0:7],self.I_rate),v_data_array)
                np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/e{2}.npy".format(self.I_year,self.I_doy,self.S_data_name[0:7],self.I_rate),e_data_array)
                np.save(S_yankai_data_path+"data20{0:02d}{1:03d}/aeosv_data/{3}s/s{2}.npy".format(self.I_year,self.I_doy,self.S_data_name[0:7],self.I_rate),s_data_array)
#                print('aeosv test')
                return None
        except:
            print("a{0}.npy error!!".format(self.S_data_name[0:7]))
            return "a{0}.npy error!!".format(self.S_data_name[0:7])

if __name__ == '__main__':    
    '''
    EX: 
      mpirun -np 9 -f host_test python3.5 minyangTEC2other_main_code_stationVer.py 15 60 80 30 4
    '''
    
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    I_comm_rank = comm.Get_rank()
    I_comm_size = comm.Get_size()
    print("Now is Rnak No:{0} . Work on {1}".format(I_comm_rank,os.popen('uname -a').read()[6:12]))
#    print('MPI test_0')
    t1 = time.time()
    I_year = int(sys.argv[1])
    I_doy_start = int(sys.argv[2])
    I_doy_end = int(sys.argv[3])
    I_rate = int(sys.argv[4])
    I_processes_num = int(sys.argv[5])
    
    for I_doy in np.arange(I_doy_start,I_doy_end,1):
        try:
            Lst_data_name = np.load(S_yankai_data_path+"data20{0:02d}{1:03d}/Ar_minyangdata_{2:02d}.npy".format(I_year,I_doy,I_rate))
        except:
            print("dont have Ar_minyangdata_{1:02d}.npy ??".format(I_rate))
            exit()
        
        if I_comm_rank != I_comm_size-1:
    #        print(I_comm_rank,Lst_data_name[(int(len(Lst_data_name)/I_comm_size)+1)*I_comm_rank:(int(len(Lst_data_name)/I_comm_size)+1)*(I_comm_rank+1)])
            miny2other.multucore(Lst_data_name[(int(len(Lst_data_name)/I_comm_size)+1)*I_comm_rank:(int(len(Lst_data_name)/I_comm_size)+1)*(I_comm_rank+1)],
                                               I_year,I_doy,I_rate,I_processes_num)
        else:    
    #        print(I_comm_rank,Lst_data_name)
            miny2other.multucore(Lst_data_name[(int(len(Lst_data_name)/I_comm_size)+1)*I_comm_rank:],I_year,I_doy,I_rate,I_processes_num)
#    os.chdir('/nishome/man4781747/GPSTEC_minyan/gnsstec_v7.2/OBS/gps/20{0:02d}.{1:03d}/{2}s'.format(I_year,I_doy,I_rate))
#    
#    Lst_data_GPS = []
#    for filenames in os.listdir('.'): 
#        if os.path.isfile(filenames):
#            if filenames[9:13] == "mat":
#                Lst_data_GPS.append(filenames)
#                
#    os.chdir('/nishome/man4781747/GPSTEC_minyan/gnsstec_v7.2/OBS/glonass/20{0:02d}.{1:03d}/{2}s'.format(I_year,I_doy,I_rate))
#    Lst_data_glonass = []
#    for filenames in os.listdir('.'): 
#        if os.path.isfile(filenames):
#            if filenames[9:13] == "mat":
#                Lst_data_glonass.append(filenames)
#    
#    Lst_all_data = list(set(Lst_data_GPS)|set(Lst_data_glonass))
#    Lst_2phase_ans = []
#    Lst_2aeosv_ans = []
#    for S_data_name in Lst_all_data:
#        miny2other_main = miny2other.minyangTEC2other(S_data_name,I_year,I_doy,I_rate,If_MPI)
#        Lst_2phase_ans.append(miny2other_main.minyang2phase())
#        Lst_2aeosv_ans.append(miny2other_main.minyang2aeosv())

    print(time.time()-t1)

    