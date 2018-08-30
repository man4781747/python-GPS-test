# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 11:40:25 2017

@author: owo

大氣誤差model
"""

def init(lat,lon,alt,elevation,relative_humidity): #(rad,rad,m,rad,%)   
    import math 
    import numpy as np
    
    humi = relative_humidity
#    azimuth = 0.

    temp0 = 15.
#    if alt < -100. or alt > 1000. or elevation <= 0.:
#        print('NO')
    
    hgt = np.copy(alt)    
    hgt[np.where(alt < 0.)] = 0.
#    if alt < 0.:
#        hgt = 0.
    
    pres = 1013.25*(1.0-(2.2557e-5*hgt)**5.2568)
    temp = temp0-(6.5e-3)*hgt+273.16
    e = 6.108*humi*np.exp((17.15*temp-4684.0)/(temp-38.45))
    z = math.pi/2.0 - elevation
    trph = 0.0022768*pres/(1.0 - 0.00266*np.cos(2.0*lat) - 0.00028*hgt/1000)/np.cos(z)
    trpw = 0.0022768*(1255.0/temp + 0.05) * e/np.cos(z)
    return_ans = trph+trpw
    return_ans[np.where((alt < -100.)|(alt > 10000.)|(elevation <= 0.))] = 0.
    
    return return_ans
if __name__ == '__main__':
    import saastamoinen_model as saamd
    import numpy as np
#    enutropospheric_delay = saamd.init(0.6538,-2.1313,-31.4557,50.,50.)
    lat = np.array([ 0.41026888,  0.41026888,  0.41026888,  0.41026888,  0.41026888,0.41026888,  0.41026888,  0.41026888])
    lon = np.array([ 2.1086224,  2.1086224,  2.1086224,  2.1086224,  2.1086224,2.1086224,  2.1086224,  2.1086224])
    alt = np.array([ 1390.17883613,  1390.17883613,  1390.17883613,  1390.17883613, 1390.17883613,  1390.17883613,  1390.17883613,  1390.17883613])
    elevation = np.array([ 0.41417493,  0.85426229,  0.64230729,  0.26299678,  1.0773899 ,
        0.62940248,  0.58234196,  0.26525226])
    enutropospheric_delay = saamd.init(lat,lon,alt,elevation,50.)