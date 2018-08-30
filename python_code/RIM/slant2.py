# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:50:53 2018

@author: owo

R = 6371 km
H = 電離殼層高度(km)
z = 仰角(度)


"""

import numpy as np

def slant2(z,H,r=6371):
    zp = np.arcsin(r/(r+H)*np.sin(0.9782*(z/180.*np.pi)))
    s = np.cos(zp)
    
    return(s,zp)


if __name__ == '__main__':
    test_sTEC = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\saknd073.npy')
    test_vTEC = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\vaknd073.npy')
    test_elv = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\eaknd073.npy')
    
    test_elv[np.where(test_elv==0)]=np.nan
    
    test = slant2(-test_elv+90,325)[0]
    
    test_2 = test_vTEC/test