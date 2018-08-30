# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 14:14:23 2018

@author: owo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

def func(x, y):
    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

# @profile
def interp1(x, y, values):
    # regard as rectangular grid
    f1 = interp2d(x, y, values, kind='cubic')
    return f1

def interp2(xx, yy, values):
    # regard as unstructured grid
    x_flat, y_flat, z_flat = map(np.ravel, [xx, yy, values])
    f2 = interp2d(x_flat, y_flat, z_flat, kind='cubic')
    return f2


if __name__ == "__main__":
    # Data point coordinates
    x = np.linspace(0, 1, 20)
    y = np.linspace(0, 1, 30)
    xx, yy = np.meshgrid(x, y)
    values = func(xx, yy)
    
    values[10:15, 7:12] = np.nan
    
    f1 = interp1(x, y, values)
    f2 = interp2(xx, yy, values)
    
    # Points which to interpolate data
    x_flat = np.linspace(0, 1, 100)
    y_flat = np.linspace(0, 1, 200)
    
    z1 = f1(x_flat, y_flat)
    z2 = f2(x_flat, y_flat)
    plt.figure()
    plt.imshow(values, extent=(0, 1, 0, 1))
    plt.title("Origin")
    plt.figure()
    plt.subplot(211)
    plt.imshow(z1, extent=(0, 1, 0, 1))
    plt.title("rectangular grid")
    plt.subplot(212)
    plt.imshow(z2, extent=(0, 1, 0, 1))
    plt.title("unstructured grid")
    plt.show()