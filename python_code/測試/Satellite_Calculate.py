# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:33:26 2018

@author: owo
"""
import numpy as np

class Satellite_Calculate:
    def __init__(self,Ay_sate_n_data):
        self.F_c    = 299792458.0
        self.F_mu   = 3.986005*(10**14)    #μ    (m**3/s**2)
        self.F_omge = 7.2921151467*(10**-5)    # (r/s)
        self.crs  = Ay_sate_n_data[:,11]                # (m)
        self.dn   = Ay_sate_n_data[:,12]                # (r/s)
        self.M0   = Ay_sate_n_data[:,13]                # (s)
        self.cuc  = Ay_sate_n_data[:,14]                # (r)
        self.e    = Ay_sate_n_data[:,15]                # (-)
        self.cus  = Ay_sate_n_data[:,16]                # (r)
        self.sqrta = Ay_sate_n_data[:,17]                # (m**0.5)
        self.toe  = Ay_sate_n_data[:,18]                # (s)
        self.cic  = Ay_sate_n_data[:,19]                # (r)
        self.omg0 = Ay_sate_n_data[:,20]                # (r)
        self.cis  = Ay_sate_n_data[:,21]                # (r)
        self.i0   = Ay_sate_n_data[:,22]                # (r)
        self.crc  = Ay_sate_n_data[:,23]                # (m)
        self.w    = Ay_sate_n_data[:,24]                # (r)
        self.odot = Ay_sate_n_data[:,25]                # (r/s)
        self.idot = Ay_sate_n_data[:,26]                # (r/s)
        self.af0  = Ay_sate_n_data[:,7]
        self.af1  = Ay_sate_n_data[:,8]
        self.af2  = Ay_sate_n_data[:,9]
        self.tgd  = Ay_sate_n_data[:,32]
        self.sva  = Ay_sate_n_data[:,30]
        self.toc  = self.toe 
        
    def get_sate_position(self,F_time_chose_sec_int,F_time_chose_sec_decimal,F_gpsweektime_fst,Ay_delta_t_sv,Ay_pseudo_range):


        self.sqrta = self.sqrta
        a = self.sqrta**2                    # (m)
        n0 = (self.F_mu/(a**3))**0.5           # (r/s)
        n = n0 + self.dn                     # (r/s)
        Ay_time_int = F_time_chose_sec_int + F_gpsweektime_fst - (Ay_pseudo_range/self.F_c).astype('int') - Ay_delta_t_sv.astype('int')
        Ay_time_decimal = F_time_chose_sec_decimal + F_gpsweektime_fst%1 - \
                        (Ay_pseudo_range/self.F_c-(Ay_pseudo_range/self.F_c).astype('int')) - \
                        (Ay_delta_t_sv-Ay_delta_t_sv.astype('int'))
                        
#        print(Ay_time_int)
#        print(self.toe.astype('int'))
        Ay_tk_int = Ay_time_int - self.toe.astype('int')
        Ay_tk_decimal = Ay_time_decimal - (self.toe-self.toe.astype('int'))
        Ay_tk = Ay_tk_int +  Ay_tk_decimal      # (s)
        Ay_tk[np.where(Ay_tk > 302400)] -= 604800
        Ay_tk[np.where(Ay_tk <-302400)] += 604800
        
        
        Ay_mk = self.M0 + n*Ay_tk                  # (s)
        def fun_test(x,sata_num):
            return Ay_mk[sata_num]-(x-self.e[sata_num]*np.sin(x))
        self.Ay_Ek = np.zeros(len(Ay_mk))
        for i in range(len(Ay_mk)):
            test_num = 0
            while abs(fun_test(test_num,i)) > 0.000000000001:
                test_num += fun_test(test_num,i)
            self.Ay_Ek[i] = test_num
            
        Ay_Vk = np.arctan2((((1-self.e**2)**0.5)*np.sin(self.Ay_Ek)/(1-self.e*np.cos(self.Ay_Ek))),((np.cos(self.Ay_Ek)-self.e)/(1-self.e*np.cos(self.Ay_Ek))))
        Ay_PHk = Ay_Vk + self.w
        Ay_dAy_Uk = self.cus*np.sin(2*Ay_PHk)+self.cuc*np.cos(2*Ay_PHk)
        Ay_dAy_Rk = self.crs*np.sin(2*Ay_PHk)+self.crc*np.cos(2*Ay_PHk)
        Ay_dAy_Ik = self.cis*np.sin(2*Ay_PHk)+self.cic*np.cos(2*Ay_PHk)
        Ay_Uk = Ay_PHk + Ay_dAy_Uk
        
        Ay_Rk = a*(1-self.e*np.cos(self.Ay_Ek))+Ay_dAy_Rk
        Ay_Ik = self.i0 + Ay_dAy_Ik + (self.idot)*Ay_tk
        
        Ay_xk_ = Ay_Rk*np.cos(Ay_Uk)
        Ay_yk_ = Ay_Rk*np.sin(Ay_Uk)
        
        Ay_omgk = self.omg0 + (self.odot - self.F_omge)*Ay_tk - self.F_omge*self.toe
        
        xk = Ay_xk_*np.cos(Ay_omgk) - Ay_yk_*np.cos(Ay_Ik)*np.sin(Ay_omgk)
        yk = Ay_xk_*np.sin(Ay_omgk) + Ay_yk_*np.cos(Ay_Ik)*np.cos(Ay_omgk)
        zk = Ay_yk_*np.sin(Ay_Ik)


        Ay_time_int = F_time_chose_sec_int + F_gpsweektime_fst - (Ay_pseudo_range/self.F_c).astype('int') - Ay_delta_t_sv.astype('int')
        Ay_time_decimal = F_time_chose_sec_decimal + F_gpsweektime_fst%1 - \
                        (Ay_pseudo_range/self.F_c-(Ay_pseudo_range/self.F_c).astype('int')) - \
                        (Ay_delta_t_sv-Ay_delta_t_sv.astype('int'))
        
        Ay_tk_fix_time_int = Ay_time_int - self.toe.astype('int')
        Ay_tk_fix_time_decimal = Ay_time_decimal - (self.toe-self.toe.astype('int'))
        
        Ay_tk_fix_time = Ay_tk_fix_time_int +  Ay_tk_fix_time_decimal  
        get_sate_clock_error_fix = self.af0+self.af1*Ay_tk_fix_time+self.af2*Ay_tk_fix_time**2-2*(self.F_mu**0.5)/(self.F_c**2)*self.e*self.sqrta*np.sin(self.Ay_Ek)
#        print(get_sate_clock_error_fix[6])
        return (xk,yk,zk,get_sate_clock_error_fix)

    
    def get_sate_clock_error(self,Ay_pseudo_range,F_time_chose_sec_int,F_time_chose_sec_decimal,F_gpsweektime_fst):
        Ay_recever_time_int = F_time_chose_sec_int + int(F_gpsweektime_fst)
        Ay_recever_time_decimal = F_time_chose_sec_decimal + F_gpsweektime_fst%1
        
        Ay_signal_transmission_time_int = Ay_recever_time_int - (Ay_pseudo_range/self.F_c).astype('int')
        Ay_signal_transmission_time_decimal = Ay_recever_time_decimal - Ay_pseudo_range/self.F_c + (Ay_pseudo_range/self.F_c).astype('int')
        Ay_signal_transmission_time_total = Ay_signal_transmission_time_int + Ay_signal_transmission_time_decimal 

        Ay_t = Ay_signal_transmission_time_total - self.toc 
       
        for i in range(2):
            Ay_t -= self.af0 + self.af1*Ay_t+self.af2*(Ay_t**2)
        return (self.af0 + self.af1*Ay_t+self.af2*(Ay_t**2))
    
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