# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 19:42:13 2016

@author: Chuanping_LASC_PC
"""

class xyz2llh:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def xyz(self):
#        import numpy as np
        import math
        (x2,y2,z2) = (self.x**2.,self.y**2.,self.z**2.)
        a = 6378137.0000	# earth radius in meters
        b = 6356752.3142	# earth semiminor in meters	
        e = ( 1. - (b/a)**2. )**0.5
        b2 = b**2.
        e2 = e**2.
        ep = e*(a/b)
        r = (x2+y2)**0.5
        r2 = r**2.
        E2 = a**2. - b**2.
        F = 54*b2*z2
        G = r2 + (1.-e2)*z2 - e2*E2
        c = (e2*e2*F*r2)/(G*G*G)
        c = float(c)
#        print(c)
        s = ( 1. + c + (c*c + 2.*c)**0.5 )**(1./3.)
        P = F / (3. * ((s+1./s+1.)**2.)*G*G)
        Q = (1.+2.*e2*e2*P)**0.5
        ro = -(P*e2*r)/(1.+Q) + ((a*a/2.)*(1.+1./Q)
                - (P*(1.-e2)*z2)/(Q*(1+Q)) - P*r2/2.)**0.5
        tmp = (r - e2*ro)**2.
        U = ( tmp + z2 )**0.5
        V = ( tmp + (1.-e2)*z2 )**0.5
        zo = (b2*self.z)/(a*V)
        height = U*( 1. - b2/(a*V) )
#        print(ep*ep*zo,r)
        lat = math.atan( (self.z + ep*ep*zo)/r )
        temp = math.atan(self.y/self.x)
        
        if self.x >= 0.:
            longi = temp
        elif (self.x < 0.) and (self.y >= 0.):
            longi = math.pi + temp
        else:
            longi = temp - math.pi
        return (lat*180/math.pi , longi*180/math.pi, height)
    
#if __name__ == '__main__':
#    import xyz2llh as test
    
        