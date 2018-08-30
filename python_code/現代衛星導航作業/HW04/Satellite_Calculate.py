# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:27:43 2017

@author: owo
"""
import numpy as np
class Satellite_Calculate:
    def __init__(self):
        self.c    = 299792458.0
        self.mu   = 3.986005*(10**14)    #μ    (m**3/s**2)
        self.omge = 7.2921151467*(10**-5)    # (r/s)
    
    def get_sate_position(self,M0,dn,e,sqrta,i0,omg0,w,odot,idot,cuc,cus,crc,crs,cic,cis,toe,recever_time,pseudo_range):
        self.sqrta = sqrta
        self.e = e
        a = self.sqrta**2                    # (m)
        n0 = (self.mu/(a**3))**0.5           # (r/s)
        n = n0 + dn                     # (r/s)
        tk = recever_time - toe - pseudo_range/self.c       # (s)

        tk[np.where(tk > 302400)] -= 604800
        tk[np.where(tk <-302400)] += 604800
        
        mk = M0 + n*tk                  # (s)
        
        
        def fun_test(x,sata_num):
            return mk[sata_num]-(x-self.e[sata_num]*np.sin(x))
        self.Ek = np.zeros(len(mk))
        for i in range(len(mk)):
            test_num = 0
            while abs(fun_test(test_num,i)) > 0.000000000001:
                test_num += fun_test(test_num,i)
            self.Ek[i] = test_num
            
        Vk = np.arctan2((((1-self.e**2)**0.5)*np.sin(self.Ek)/(1-self.e*np.cos(self.Ek))),((np.cos(self.Ek)-self.e)/(1-self.e*np.cos(self.Ek))))
        PHk = Vk + w
        dUk = cus*np.sin(2*PHk)+cuc*np.cos(2*PHk)
        dRk = crs*np.sin(2*PHk)+crc*np.cos(2*PHk)
        dIk = cis*np.sin(2*PHk)+cic*np.cos(2*PHk)
        Uk = PHk + dUk
        
        Rk = a*(1-self.e*np.cos(self.Ek))+dRk
        Ik = i0 + dIk + (idot)*tk
        
        xk_ = Rk*np.cos(Uk)
        yk_ = Rk*np.sin(Uk)
        
        omgk = omg0 + (odot - self.omge)*tk - self.omge*toe
        
        xk = xk_*np.cos(omgk) - yk_*np.cos(Ik)*np.sin(omgk)
        yk = xk_*np.sin(omgk) + yk_*np.cos(Ik)*np.cos(omgk)
        zk = yk_*np.sin(Ik)

        return (xk,yk,zk)
    def get_sate_clock_error(self,pseudo_range,af0,af1,af2,toc,recever_time):
        F = -4.442807633e-10
        t_sv = recever_time - pseudo_range/self.c        
        delta_t_sv = ( af0 + af1*(t_sv-toc) + af2*((t_sv-toc)**2) + F*(self.e**self.sqrta)*np.sin(self.Ek) )
        
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