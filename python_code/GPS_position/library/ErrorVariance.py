# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:11:35 2018

@author: owo
"""
import numpy as np


class Error_variance:
    def __init__(self):
        self.F_CCPER = 100.  # code/carrier‐phase error ratio
        self.F_a = 0.003 # carrier‐phase error factor a (m)
        self.F_b = 0.003 # carrier‐phase error factor b (m)
        self.F_EFACT_GPS = 1.0
        self.F_ERR_BRDCI = 0.5
        self.F_ERR_SAAS = 0.3   # /* saastamoinen model error std (m) */
        
        
    def varerr(self,Ay_elevation,S_ionofree_model_type):
        Ay_varr = self.F_EFACT_GPS*self.F_CCPER**2*( self.F_a**2 + (self.F_b**2)/np.sin(Ay_elevation))
        if S_ionofree_model_type == 'C1P2':
            Ay_varr *= 3.0**2
        
        return Ay_varr*self.F_EFACT_GPS
    
    def vare(self,Ay_sva):
        '''
        測試用記得砍
        以下
        '''
#        Ay_sva = np.zeros_like(Ay_sva)  ##### 測試用記得砍  
        '''
        以上
        測試用記得砍
        '''
        Lst_ura_value = [2.4,3.4,4.85,6.85,9.65,13.65,24.0,48.0,96.0,192.0,384.0,768.0,1536.0,3072.0,6144.0]
        Ay_ura = np.zeros_like(Ay_sva)
        for i in range(len(Ay_ura)):
            if Ay_sva[i] < 0 or Ay_sva[i] > 15:
                Ay_ura[i] = 6144.0**2
            else:
                Ay_ura[i] = Lst_ura_value[int(Ay_sva[i])]**2
        return(Ay_ura)
    
    def vmeas(self):
        return 0.3**2  # code bias error std (m)
    
    def vion(self,I_i,S_ionofree_model_type,Ay_ion,S_DGPS):
        if I_i == 0 or S_DGPS != 'No':
            S_ionofree_model_type = 'broadcast'
        if S_ionofree_model_type == 'broadcast':
            Ay_vion = (Ay_ion * self.F_ERR_BRDCI)**2
            
        elif S_ionofree_model_type == 'C1P2':
            Ay_vion = 0
        
        elif S_ionofree_model_type == 'No':
            Ay_vion = (5.0)**2   ## ERR_ION     5.0         /* ionospheric delay std (m) */
        
        
        return Ay_vion
    
    def vtrp(self,I_i,S_tropospherefree_model_type,Ay_elevation):
        if I_i == 0:
            S_tropospherefree_model_type = 'saastamoinen'
            
        if S_tropospherefree_model_type == 'saastamoinen':
            Ay_vtrp = (self.F_ERR_SAAS/(np.sin(Ay_elevation)+0.1) )**2
        
        elif S_tropospherefree_model_type == 'No':
            Ay_vtrp = 3.0**2
            
        return Ay_vtrp