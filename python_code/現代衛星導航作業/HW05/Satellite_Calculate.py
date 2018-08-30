# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:27:43 2017

@author: owo
"""
import numpy as np
class Satellite_Calculate:
    def __init__(self):
        self.F_c    = 299792458.0
        self.F_mu   = 3.986005*(10**14)    #μ    (m**3/s**2)
        self.F_omge = 7.2921151467*(10**-5)    # (r/s)
    
    def get_sate_position(self,Ay_M0,Ay_dn,e,Ay_sqrta,Ay_i0,Ay_omg0,w,Ay_odot,Ay_idot,Ay_cuc,Ay_cus,Ay_crc,Ay_crs,Ay_cic,Ay_cis,Ay_toe,recever_time,pseudo_range):
        self.Ay_sqrta = Ay_sqrta
        self.e = e
        a = self.Ay_sqrta**2                    # (m)
        n0 = (self.F_mu/(a**3))**0.5           # (r/s)
        n = n0 + Ay_dn                     # (r/s)
        Ay_tk = recever_time - Ay_toe - pseudo_range/self.F_c       # (s)

        Ay_tk[np.where(Ay_tk > 302400)] -= 604800
        Ay_tk[np.where(Ay_tk <-302400)] += 604800
        
        Ay_mk = Ay_M0 + n*Ay_tk                  # (s)
        
        
        def fun_test(x,sata_num):
            return Ay_mk[sata_num]-(x-self.e[sata_num]*np.sin(x))
        self.Ay_Ek = np.zeros(len(Ay_mk))
        for i in range(len(Ay_mk)):
            test_num = 0
            while abs(fun_test(test_num,i)) > 0.000000000001:
                test_num += fun_test(test_num,i)
            self.Ay_Ek[i] = test_num
            
        Ay_Vk = np.arctan2((((1-self.e**2)**0.5)*np.sin(self.Ay_Ek)/(1-self.e*np.cos(self.Ay_Ek))),((np.cos(self.Ay_Ek)-self.e)/(1-self.e*np.cos(self.Ay_Ek))))
        Ay_PHk = Ay_Vk + w
        Ay_dAy_Uk = Ay_cus*np.sin(2*Ay_PHk)+Ay_cuc*np.cos(2*Ay_PHk)
        Ay_dAy_Rk = Ay_crs*np.sin(2*Ay_PHk)+Ay_crc*np.cos(2*Ay_PHk)
        Ay_dAy_Ik = Ay_cis*np.sin(2*Ay_PHk)+Ay_cic*np.cos(2*Ay_PHk)
        Ay_Uk = Ay_PHk + Ay_dAy_Uk
        
        Ay_Rk = a*(1-self.e*np.cos(self.Ay_Ek))+Ay_dAy_Rk
        Ay_Ik = Ay_i0 + Ay_dAy_Ik + (Ay_idot)*Ay_tk
        
        Ay_xk_ = Ay_Rk*np.cos(Ay_Uk)
        Ay_yk_ = Ay_Rk*np.sin(Ay_Uk)
        
        Ay_omgk = Ay_omg0 + (Ay_odot - self.F_omge)*Ay_tk - self.F_omge*Ay_toe
        
        xk = Ay_xk_*np.cos(Ay_omgk) - Ay_yk_*np.cos(Ay_Ik)*np.sin(Ay_omgk)
        yk = Ay_xk_*np.sin(Ay_omgk) + Ay_yk_*np.cos(Ay_Ik)*np.cos(Ay_omgk)
        zk = Ay_yk_*np.sin(Ay_Ik)

        return (xk,yk,zk)
    def get_sate_clock_error(self,pseudo_range,af0,af1,af2,toc,recever_time):
        F = -4.442807633e-10
        t_sv = recever_time - pseudo_range/self.F_c        
        delta_t_sv = ( af0 + af1*(t_sv-toc) + af2*((t_sv-toc)**2) + F*(self.e**self.Ay_sqrta)*np.sin(self.Ay_Ek) )
        
        return delta_t_sv
    
    def Earth_rotation_error(self,xk,yk,zk,pseudo_range):
        sate_position_before_fix = np.array([xk,yk,zk])
        omega = 7.2921151467e-5
        sate_position_after_fix = np.copy(sate_position_before_fix)
        for i in range(len(sate_position_before_fix[0])):
            deltat = pseudo_range[i]/299792458
            theta = omega*deltat
            rotmat = np.matrix([[ np.cos(theta) , np.sin(theta) ,0],
                                [-np.sin(theta) , np.cos(theta) ,0],
                                [0              , 0             ,1]])
            sate_position_after_fix[:,i] = np.asarray(rotmat*(np.asmatrix(sate_position_before_fix[:,i]).T))[:,0]
        return (sate_position_after_fix[0,:],
                sate_position_after_fix[1,:],
                sate_position_after_fix[2,:])