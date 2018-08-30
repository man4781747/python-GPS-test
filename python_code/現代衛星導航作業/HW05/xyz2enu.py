# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:00:03 2017

@author: owo
"""

import numpy as np
import xyz2llh

class xyz2enu:
    def __init__(self, P1_array,P2_array): #(目標位置 , 參考位置)    
        tmpxyz = P1_array.T
        tmporg = P2_array.T
        difxyz = tmpxyz - tmporg
        x = xyz2llh.xyz2llh(P2_array[0,0],P2_array[0,1],P2_array[0,2]).xyz()
        orgllh = np.array([[x[0]/180*np.pi],[x[1]/180*np.pi],[x[2]]])
        phi = orgllh[0]
        lam = orgllh[1]
        sinphi = np.sin(phi)[0]
        cosphi = np.cos(phi)[0]
        sinlam = np.sin(lam)[0]
        coslam = np.cos(lam)[0]
        R = np.array([[-sinlam        ,  coslam        , 0.    ],
                      [-sinphi*coslam , -sinphi*sinlam , cosphi],
                      [ cosphi*coslam ,  cosphi*sinlam , sinphi]])

        self.enu = np.dot(R,difxyz)
    def return_enu(self):
        return self.enu.T
        
if __name__ == '__main__':
    import xyz2enu as test
    
    P1_array = np.array([[-2694685.473,-4293642.366,3857878.924]])
    P2_array = np.array([[-2694892.460,-4293083.225,3858353.437]])
    enu = test.xyz2enu(P1_array,P2_array).return_enu()