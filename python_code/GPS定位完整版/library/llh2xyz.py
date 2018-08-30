# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:13:42 2017

@author: owo
"""
import numpy as np

class llh2xyz:
    def __init__(self,llh_array):
        phi = llh_array[0,0]/180.*np.pi
        lambda_ = llh_array[0,1]/180.*np.pi
        h = llh_array[0,2]
    
        a = 6378137.0000
        b = 6356752.3142
        e = (1-(b/a)**2)**0.5
        
        sinphi = np.sin(phi)
        cosphi = np.cos(phi)
        coslam = np.cos(lambda_)
        sinlam = np.sin(lambda_)
        tan2phi = (np.tan(phi))**2
        tmp = 1 - e*e
        tmpden = ( 1 + tmp*tan2phi )**0.5
        
        x = (a*coslam)/tmpden + h*coslam*cosphi
        
        y = (a*sinlam)/tmpden + h*sinlam*cosphi
        
        tmp2 = (1 - e*e*sinphi*sinphi)**0.2
        z = (a*tmp*sinphi)/tmp2 + h*sinphi
        xyz = np.array([[x,y,z]])
        self.xyz = xyz
      
    def return_xyz(self):
        return self.xyz

if __name__ == '__main__':
    import xyz2llh as test
    import llh2xyz as test_2

    x = -2694685.473
    y = -4293642.366
    z = 3857878.924

    llh = test.xyz2llh(x,y,z).xyz()
    
    llh_array = np.array([[llh[0],llh[1],llh[2]]])
    xyz = test_2.llh2xyz(llh_array).return_xyz()

#    all_array_llh2xyz = [test_2.llh2xyz(np.array([[lon,lat,0]])).return_xyz() for lat in np.arange(-90,90,1) for lon in np.arange(-180,180,1)]
#    
#    all_array_xyz2llh = [test.xyz2llh( all_array_llh2xyz[i][0,0],all_array_llh2xyz[i][0,1],all_array_llh2xyz[i][0,2] ).xyz() for i in range(len(all_array_llh2xyz))]