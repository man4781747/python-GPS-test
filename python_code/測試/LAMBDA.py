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
    
    
    
def search(Ay_a_,I_x,Mt_D,Mt_L):
    '''
    Ay_a_ : 經由KALMAN所求出的 ambiguity 值 (初始估計值)
    I_x   : LAMBDA 判斷範圍數值(自訂?)
    Mt_D  : KALMAN所求出的 ambiguity 的 P矩陣經由 LDL_decomposition 後的 D 矩陣
            表示 新的 ambiguity 值 'Ay_a_new' 中的各值的 variance
    Mt_L  : KALMAN所求出的 ambiguity 的 P矩陣經由 LDL_decomposition 後的 L 矩陣
            要由此 L 矩陣來求出新的 ambiguity 值 'Ay_a_new' , Ay_a_new中的新的 ambiguity 值
            其互相間相關度低
    '''
    
    
    '''
    Ay_sig_xx : D矩陣數值 ( a_(i|I,i|I) 的 sigma值 )
    '''
    I_search_range = 3
    Ay_sig_xx = np.zeros((1,len(Mt_D)))
    for I_sig_xx in range(len(Mt_D)):
        Ay_sig_xx[0,I_sig_xx] = Mt_D[I_sig_xx,I_sig_xx]
        
        
    for I_i in range(len(Ay_a_[0])):   
        '''
        求出 新的 ambiguity 值 
        a_1 = a_1
        a_2|1 = a_2 - sig()*(a_1 - a1) ...
        
        表除了第一項新 ambiguity 值之外 第 i 項新 a 值皆與前 i-1 項新 a 值有關
        a_i|I = a_i - Mt_L[i,:]*(a_j|J - aj)  
        aj 為 前時刻訂出來的估計值
        '''
        if I_i == 0:
            '''
            a_1 = a_1
            
            Ay_a_guass : 以 a_1 來設出猜測的 a1 值 (目前為 a_1 值前後各4位整數位)
                         [ 9 X 1 ]
            
            Ay_a__minus_a : ( a_1 - a1 ) 值 ,表新 a 值與猜測 a_ 的差距 
                            [ 9 X 1 ]
            '''
            Ay_a_new = np.copy(Ay_a_[0:1,0:1])
            Ay_a_guass = np.array([np.arange(int(Ay_a_[0:1,0:1])-I_search_range,int(Ay_a_[0:1,0:1])+I_search_range+1,1)]).T
            Ay_a__minus_a = Ay_a_new - Ay_a_guass
        elif I_i > 0:
            '''
            a_2|1 開始
            Ay_a_new_ : 以已知的 a_j|J 值求得新的 a_i|I 值 ,並預留猜測值 ai 空間
            '''
            Ay_a_new_ = np.zeros((len(Ay_a_new[:,0])*(2*I_search_range+1),I_i+1))
            for I_Ay_a_new__num in range(len(Ay_a_new[:,0])):
                Ay_a_new_[I_Ay_a_new__num*(2*I_search_range+1):(I_Ay_a_new__num+1)*(2*I_search_range+1),:len(Ay_a_new_[0,:])-1] = Ay_a_new[I_Ay_a_new__num,:]
            Ay_a_new_[:,len(Ay_a_new_[0,:])-1] = Ay_a_[0,I_i] - (Mt_L[I_i,:I_i]*np.matrix(Ay_a__minus_a.T))
            Ay_a_new = Ay_a_new_
            
            Ay_a_guass_ = np.zeros((len(Ay_a_guass[:,0])*(2*I_search_range+1),I_i+1))
            for I_Ay_a_guass_num in range(len(Ay_a_guass[:,0])):
                Ay_a_guass_[I_Ay_a_guass_num*(2*I_search_range+1):(I_Ay_a_guass_num+1)*(2*I_search_range+1),:len(Ay_a_new[0,:])-1] = Ay_a_guass[I_Ay_a_guass_num,:len(Ay_a_guass[0,:])]
                Ay_a_guass_[I_Ay_a_guass_num*(2*I_search_range+1):(I_Ay_a_guass_num+1)*(2*I_search_range+1),len(Ay_a_new[0,:])-1] = np.arange(int(Ay_a_new[I_Ay_a_guass_num,-1])-I_search_range,int(Ay_a_new[I_Ay_a_guass_num,-1])+I_search_range+1,1)
            Ay_a_guass = Ay_a_guass_
            
            Ay_a__minus_a = np.zeros_like(Ay_a_guass)
            for I_Ay_a__minus_a_num in range(len(Ay_a_new[:,0])):
                Ay_a__minus_a[I_Ay_a__minus_a_num*(2*I_search_range+1):(I_Ay_a__minus_a_num+1)*(2*I_search_range+1)] = Ay_a_new[I_Ay_a__minus_a_num,:]
            Ay_a__minus_a -= Ay_a_guass
            
            
    '''
    lambda(ai) 值
    '''
    Ay_lambda = np.zeros_like(Ay_a__minus_a)
    for I_Ay_lambda in range(len(Ay_lambda[0])):
        if I_Ay_lambda == 0:
            Ay_lambda[:,0] = 1 
        elif I_Ay_lambda > 0:
            Ay_lambda[:,I_Ay_lambda] = 1 - (Ay_a__minus_a[:,I_Ay_lambda-1]**2)/((I_x**2)*Ay_sig_xx[0,I_Ay_lambda-1])        


    I_x = 50
    tt = (Ay_a__minus_a**2) - (Ay_sig_xx*Ay_lambda*I_x**2)
    ttt = np.sum((Ay_a__minus_a**2)/Ay_sig_xx,1)-I_x**2
    Ay_check_array = np.zeros_like(tt)
    Ay_check_array[np.where(tt>0)]=1 
    Ay_check_array = np.sum(Ay_check_array,1)
    Ay_pass = np.where((Ay_check_array == 0)&(ttt<=0))[0]
    while len(Ay_pass) > 3:
#        print(I_x)
        I_x *= 0.9
        tt = (Ay_a__minus_a**2) - (Ay_sig_xx*Ay_lambda*I_x**2)
        ttt = np.sum((Ay_a__minus_a**2)/Ay_sig_xx,1)-I_x**2
        Ay_check_array = np.zeros_like(tt)
        Ay_check_array[np.where(tt>0)]=1 
        Ay_check_array = np.sum(Ay_check_array,1)
        Ay_pass = np.where((Ay_check_array == 0)&(ttt<=0))[0]
    
    Ay_a_guass_chose = Ay_a_guass[Ay_pass]
    
    return(Ay_a_guass_chose)
    