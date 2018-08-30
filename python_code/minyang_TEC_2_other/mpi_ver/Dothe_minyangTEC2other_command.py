# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 21:03:38 2018

@author: owo

啟動方法:  mpirun -np 36 -f host_test python3.5 Dothe_minyangTEC2other_command.py
"""



import os
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
I_comm_rank = comm.Get_rank()
I_comm_size = comm.Get_size()
print("Now is Rnak No:{0} . Work on {1}".format(I_comm_rank,os.popen('uname -a').read()[6:12]))

try:
    Ay_command = np.load('minyangTEC2other_command.npy')
except:
    print("dont have minyangTEC2other_command.npy ??")
    exit()

if I_comm_rank != I_comm_size-1:
#        print(I_comm_rank,Lst_data_name[(int(len(Lst_data_name)/I_comm_size)+1)*I_comm_rank:(int(len(Lst_data_name)/I_comm_size)+1)*(I_comm_rank+1)])
    
    Ay_command_chose = Ay_command[(int(len(Ay_command)/I_comm_size)+1)*I_comm_rank:(int(len(Ay_command)/I_comm_size)+1)*(I_comm_rank+1)]
    for i in range(len(Ay_command_chose)):
        os.system(Ay_command_chose[i])
else:    
#        print(I_comm_rank,Lst_data_name)
    Ay_command_chose = Ay_command[(int(len(Ay_command)/I_comm_size)+1)*I_comm_rank:]
#    os.chdir('/nishome/m
    for i in range(len(Ay_command_chose)):
        os.system(Ay_command_chose[i])
