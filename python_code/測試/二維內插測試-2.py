# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 14:27:37 2018

@author: owo
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

x =   np.array([[9.19632, 9.62141, 10.0829,np.isnan,np.isnan],
    [9.21164, 9.64347, 10.1392, 10.5698,np.isnan],
    [9.22175, 9.65439, 10.1423, 10.6301, 11.0323],
    [9.21632, 9.67060, 10.1474, 10.6230, 11.0818]])

y =  np.array([[11.5466,11.6485,11.7619,np.isnan,np.isnan],
    [12.4771, 12.5460, 12.5453, 12.7142,np.isnan],
    [13.5578, 13.5581, 13.5505, 13.5309, 13.6081],
    [14.5653, 14.5504, 14.5036, 14.5145, 14.5060]])

z = np.array([[0.466113, 0.0484404, -0.385355,np.isnan,np.isnan],
    [0.366125, -0.160165, -0.548668, -0.888301,np.isnan],
    [-0.0970777, -0.346734, -0.826576, -1.08412, -1.33129],
    [-0.259981, -0.586938, -1.03477, -1.32384, -1.61500]])

#x=x.ravel()              #Flat input into 1d vector
#x=list(x[x!=np.isnan])   #eliminate any NaN
#y=y.ravel()
#y=list(y[y!=np.isnan])
#z=z.ravel()
#z=list(z[z!=np.isnan])
#
#
#xnew = np.arange(9,11.5, 0.01)
#ynew = np.arange(9,15, 0.01)
#znew = griddata((x, y), z, (xnew[None,:], ynew[:,None]), method='linear')

from scipy.interpolate import SmoothBivariateSpline

x=x.ravel()
x=(x[x!=np.isnan])
y=y.ravel()
y=(y[y!=np.isnan])
z=z.ravel()
z=(z[z!=np.isnan])

xnew = np.arange(9,11.5, 0.01)
ynew = np.arange(10.5,15, 0.01)

f = SmoothBivariateSpline(x,y,z,kx=1,ky=1)

znew=np.transpose(f(xnew, ynew))

levels = np.linspace(min(z), max(z), 15)
plt.ylabel('Y', size=15)
plt.xlabel('X', size=15)
cmap = plt.cm.jet_r
cs = plt.contourf(xnew, ynew, znew, levels=levels, cmap=cmap)
cbar = plt.colorbar(cs)
cbar.set_label('Z', rotation=90, fontsize=15) # gas fraction
plt.show()

