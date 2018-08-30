# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 20:56:46 2018

@author: owo


"""

import numpy as np

def a_transform(Ay_a_guass_,Ay_a_sig,Ay_a_,Ay_D,Ay_L):
    Ay_a_sig_ = np.zeros((len(Ay_a_sig[:]),len(Ay_a_sig[0])+1))
    Ay_a_sig_[:,:len(Ay_a_sig[0])] = Ay_a_sig
    if len(Ay_a_sig_[0,:]) == 1:
        Ay_a_sig_[:] = Ay_a_[0]-Ay_a_guass_[:,0:1]
    
    else:
        Ay_a_sig_[:,len(Ay_a_sig_[0,:])-1] = 1
        
    return Ay_a_guass_,Ay_a_sig_
    
    
    
def search(Ay_a_,I_x,Ay_D,Ay_L):

#    for I_i in range(len(Ay_a_[0,:])):
    Ay_a_ = np.array([[1,2,3]])
    Ay_a_ = np.array([[8,10,33]])
    
    test_get = np.zeros((20,20))
    I_x = 1
    while len(test_get[:,0]) >= 2:
        for I_i in range(3):    
            print(I_i)
            if I_i == 0:
                Ay_a_new = np.copy(Ay_a_[0:1,0:1])
    #            Ay_a_new = np.zeros((9,1))+np.copy(Ay_a_[0:1,0:1])
                Ay_a_guass = np.array([np.arange(int(Ay_a_[0:1,0:1])-4,int(Ay_a_[0:1,0:1])+5,1)]).T
                Ay_a__minus_a = Ay_a_new - Ay_a_guass
            elif I_i > 0:
                Ay_a_new_ = np.zeros((len(Ay_a_new[:,0])*9,I_i+1))
    #            Ay_a_new_ = np.zeros((len(Ay_a__minus_a[:,0])*11,I_i+1))
                for I_Ay_a_new__num in range(len(Ay_a_new[:,0])):
                    Ay_a_new_[I_Ay_a_new__num*9:(I_Ay_a_new__num+1)*9,:len(Ay_a_new_[0,:])-1] = Ay_a_new[I_Ay_a_new__num,:]
                Ay_a_new_[:,len(Ay_a_new_[0,:])-1] = Ay_a_[0,I_i] - (Ay_L[I_i,:I_i]*np.matrix(Ay_a__minus_a.T))
                Ay_a_new = Ay_a_new_
                
                Ay_a_guass_ = np.zeros((len(Ay_a_guass[:,0])*9,I_i+1))
                for I_Ay_a_guass_num in range(len(Ay_a_guass[:,0])):
                    Ay_a_guass_[I_Ay_a_guass_num*9:(I_Ay_a_guass_num+1)*9,:len(Ay_a_new[0,:])-1] = Ay_a_guass[I_Ay_a_guass_num,:len(Ay_a_guass[0,:])]
                    Ay_a_guass_[I_Ay_a_guass_num*9:(I_Ay_a_guass_num+1)*9,len(Ay_a_new[0,:])-1] = np.arange(int(Ay_a_new[I_Ay_a_guass_num,-1])-4,int(Ay_a_new[I_Ay_a_guass_num,-1])+5,1)
                Ay_a_guass = Ay_a_guass_
                
                Ay_a__minus_a = np.zeros_like(Ay_a_guass)
                for I_Ay_a__minus_a_num in range(len(Ay_a_new[:,0])):
                    Ay_a__minus_a[I_Ay_a__minus_a_num*9:(I_Ay_a__minus_a_num+1)*9] = Ay_a_new[I_Ay_a__minus_a_num,:]
                Ay_a__minus_a -= Ay_a_guass
    #            Ay_a__minus_a_ = 
            print('test')
            Ay_sig_xx = np.zeros((1,I_i+1))
            for I_sig_xx in range(I_i+1):
                Ay_sig_xx[0,I_sig_xx] = Ay_D[I_sig_xx,I_sig_xx]
                
            Ay_lambda = np.zeros_like(Ay_a__minus_a)
            for I_Ay_lambda in range(I_i+1):
                if I_Ay_lambda == 0:
                    Ay_lambda[:,0] = 1
                elif I_Ay_lambda > 0:
                    Ay_lambda[:,I_Ay_lambda] = 1 - (Ay_a__minus_a[:,I_Ay_lambda-1]**2)/((I_x**2)*Ay_sig_xx[0,I_Ay_lambda-1])
            
            test = Ay_a__minus_a**2 - Ay_sig_xx*I_x*Ay_lambda
            test_sum = np.sum(test,1)
            test_zeros = np.zeros_like(test)
            test_zeros[np.where(test > 0)] = 1
            test_get = test[np.where((np.sum(test_zeros,1) <= 0)&(test_sum <= 0))[0],:]
            Ay_ans = Ay_a_guass[np.where((np.sum(test_zeros,1) <= 0)&(test_sum <= 0))[0],:]
        I_x *= 0.9
    print(I_x/0.9)
    
# I_x =0.0984770902183612
#        Ay_a_guass = Ay_a_guass[np.where((np.sum(test_zeros,1) <= 0)&(test_sum <= 0))[0],:]
#        Ay_a__minus_a = Ay_a__minus_a[np.where((np.sum(test_zeros,1) <= 0)&(test_sum <= 0))[0],:]
#        test = Ay_a__minus_a**2 - 

