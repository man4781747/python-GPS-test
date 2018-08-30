# -*- coding: utf-8 -*-
"""
Created on Fri May 11 13:48:46 2018

@author: owo

nmf

仿照 RTKLIB 中 rtkcmn.c 中的 nmf

"""

import numpy as np

def interpc(Ay_coef_chose,F_lat):
    I_i = int(F_lat/15.0)
    if I_i < 1:
        return Ay_coef_chose[0]
    elif I_i > 4:
        return Ay_coef_chose[4]
#    print(I_i)
#    print(Ay_coef_chose[I_i-1],Ay_coef_chose[I_i])
    return Ay_coef_chose[I_i-1] * (1.0 - F_lat/15.0 + I_i) + Ay_coef_chose[I_i] * (F_lat/15.0 - I_i)

def mapf(Ay_el ,a ,b ,c):
    Ay_sinel = np.sin(Ay_el)
    return (1.0+a/(1.0+b/(1.0+c)))/(Ay_sinel+(a/(Ay_sinel+b/(Ay_sinel+c))))

Ay_coef = np.array([[1.2769934E-3, 1.2683230E-3, 1.2465397E-3, 1.2196049E-3, 1.2045996E-3],
                    [2.9153695E-3, 2.9152299E-3, 2.9288445E-3, 2.9022565E-3, 2.9024912E-3],
                    [62.610505E-3, 62.837393E-3, 63.721774E-3, 63.824265E-3, 64.258455E-3],
                    [0.0000000E-0, 1.2709626E-5, 2.6523662E-5, 3.4000452E-5, 4.1202191E-5],
                    [0.0000000E-0, 2.1414979E-5, 3.0160779E-5, 7.2562722E-5, 11.723375E-5],
                    [0.0000000E-0, 9.0128400E-5, 4.3497037E-5, 84.795348E-5, 170.37206E-5],
                    [5.8021897E-4, 5.6794847E-4, 5.8118019E-4, 5.9727542E-4, 6.1641693E-4],
                    [1.4275268E-3, 1.5138625E-3, 1.4572752E-3, 1.5007428E-3, 1.7599082E-3],
                    [4.3472961E-2, 4.6729510E-2, 4.3908931E-2, 4.4626982E-2, 5.4736038E-2]])

def nmf(I_doy,F_lat,F_lon,F_hgt,Ay_el):
    Ay_aht = np.array([2.53E-5, 5.49E-3, 1.14E-3])
    Ay_ah = np.zeros(3)
    Ay_aw = np.zeros(3)
#Ay_el = np.array([0.557,0.711,0.928,1.166,0.523,0.581])
#I_doy = 76
#F_lat = 24.017879
#F_lon = 121.610348
#F_hgt = 36.4
    F_y = (I_doy - 28.0)/365.25 + (0.5 if F_lat<0.0 else 0.0)
    F_cosy = np.cos(2*np.pi*F_y)
#    print(F_y,F_hgt)
#    print(F_cosy)
    F_lat = abs(F_lat)
    
    for i in range(3):
       Ay_ah[i] = interpc(Ay_coef[i],F_lat) - interpc(Ay_coef[i+3],F_lat)*F_cosy
       Ay_aw[i] = interpc(Ay_coef[i+6],F_lat)
#    print(Ay_ah)
#    print(Ay_aw)
#    print(mapf(Ay_el ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2]))
#    print(np.sin(Ay_el) ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2])
#    print(mapf(Ay_el ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2])[0])
#    print(1.0/np.sin(Ay_el[0]))
#    print(F_hgt)
    Ay_dm = (1.0/np.sin(Ay_el) - mapf(Ay_el ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2]))*F_hgt/1E3
#    print(Ay_dm[0])
#    print(mapf(Ay_el ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2]) + Ay_dm)
    return mapf(Ay_el ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2]) + Ay_dm


#test = mapf(Ay_el ,Ay_aht[0] ,Ay_aht[1] ,Ay_aht[2]) + Ay_dm