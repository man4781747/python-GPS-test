# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:27:42 2018

@author: owo
"""
import numpy as np
import math

class Error_module:
    def __init__(self):
        pass
    
    def saastamoinen_model(self,lat,lon,alt,elevation,relative_humidity):
        humi = relative_humidity

        temp0 = 15.

        hgt = np.copy(alt)    
        hgt[np.where(alt < 0.)] = 0.
        pres = 1013.25*(np.power((1.0 - 2.2557e-5*hgt),5.2568))
#        pres = 1013.25*((1.0 - 2.2557e-5*hgt)**5.2568)
        temp = temp0-(6.5e-3)*hgt+273.16
        e = 6.108*humi*np.exp((17.15*temp-4684.0)/(temp-38.45))
        z = math.pi/2.0 - elevation
        trph = 0.0022768*pres/(1.0 - 0.00266*np.cos(2.0*lat*np.pi/180.) - 0.00028*hgt/1000)/np.cos(z)
        trpw = 0.002277*(1255.0/temp + 0.05) * e/np.cos(z)
        return_ans = trph+trpw

        return_ans[np.where((alt < -100.)|(alt > 10000.)|(elevation <= 0.))] = 0.
        return return_ans
    
    def iono_model_broadcast(self,I_year,I_doy,Ay_lat,Ay_lon,Ay_elevation_angle,Ay_enu_resever_sate,F_SPG_time_sec,S_n_data_path):
        '''
        http://www.navipedia.net/index.php/Klobuchar_Ionospheric_Model
        '''
        F_C = 299792458.0
        
        Ay_iono_broadcast = np.load(S_n_data_path)
        Ay_earth_centred_angle = 0.0137/(Ay_elevation_angle/math.pi+0.11)-0.022
        Ay_azimuth = np.arctan2(Ay_enu_resever_sate[:,0], Ay_enu_resever_sate[:,1])
        Ay_azimuth[np.where(Ay_azimuth<0)] += 360.
        Ay_IPP_lat = Ay_lat/math.pi+Ay_earth_centred_angle*np.cos(Ay_azimuth)
        Ay_IPP_lat[np.where(Ay_IPP_lat > 0.416)] = 0.416
        Ay_IPP_lat[np.where(Ay_IPP_lat < -0.416)] = -0.416
        Ay_IPP_lon = Ay_lon/math.pi + Ay_earth_centred_angle*np.sin(Ay_azimuth)/np.cos(Ay_IPP_lat*math.pi)
        Ay_geomagnetic_lat = Ay_IPP_lat + 0.064*np.cos( (Ay_IPP_lon - 1.617)*math.pi)
        Ay_IPP_LT = 43200*Ay_IPP_lon + F_SPG_time_sec
        Ay_IPP_LT[np.where(Ay_IPP_LT >= 86400)] -= 86400
        Ay_IPP_LT[np.where(Ay_IPP_LT < 0)] += 86400
        Ay_amplitude_of_ionospheric_delay = Ay_iono_broadcast[0,0] + Ay_geomagnetic_lat*(Ay_iono_broadcast[0,1]+Ay_geomagnetic_lat*(Ay_iono_broadcast[0,2]+Ay_geomagnetic_lat*Ay_iono_broadcast[0,3]) )
        Ay_amplitude_of_ionospheric_delay[np.where(Ay_amplitude_of_ionospheric_delay < 0)] = 0
        Ay_period_of_ionospheric_delay = Ay_iono_broadcast[1,0] + Ay_geomagnetic_lat*(Ay_iono_broadcast[1,1]+Ay_geomagnetic_lat*(Ay_iono_broadcast[1,2]+Ay_geomagnetic_lat*Ay_iono_broadcast[1,3]) )
        Ay_period_of_ionospheric_delay[np.where(Ay_period_of_ionospheric_delay < 72000)] = 72000
        Ay_x = 2*np.pi*(Ay_IPP_LT-50400.)/Ay_period_of_ionospheric_delay ## Ay_phase_of_ionospheric_delay
        
        Ay_slant_factor = 1+16*(0.53-Ay_elevation_angle/math.pi)**3
        Ay_ionospheric_time_delay = np.zeros((len(Ay_IPP_LT)))
        for i in range(len(Ay_x)):
            if abs(Ay_x[i]) <= 1.57:
                Ay_ionospheric_time_delay[i] = ((5*10**-9)+Ay_amplitude_of_ionospheric_delay[i]*(1+Ay_x[i]*Ay_x[i]*
                                           (-0.5+Ay_x[i]*Ay_x[i]/24.))  )*Ay_slant_factor[i]*F_C
            else:
                Ay_ionospheric_time_delay[i] = (5*10**-9)*Ay_slant_factor[i]*F_C
                
        return Ay_ionospheric_time_delay