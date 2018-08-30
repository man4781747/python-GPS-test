# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 19:28:47 2018

@author: owo

LDL decopsition 練習

https://zh.wikipedia.org/wiki/Cholesky%E5%88%86%E8%A7%A3
"""

import numpy as np

def D_design_in(I_j,Ay_A,Ay_L,Ay_D):
    Ay_D[I_j,I_j] = Ay_A[I_j,I_j]
    if I_j > 0:
        for I_k in range(I_j):
            Ay_D[I_j,I_j] -= (Ay_L[I_j,I_k]**2)*Ay_D[I_k,I_k]
    return Ay_A,Ay_L,Ay_D
            
def L_design_in(I_i,I_j,Ay_L,Ay_D,Ay_A):
    Ay_L[I_i,I_j] = Ay_A[I_i,I_j]/Ay_D[I_j,I_j]
    if I_j > 0:
        for I_k in range(I_j):
           Ay_L[I_i,I_j] -= Ay_L[I_i,I_k]*Ay_L[I_j,I_k]*Ay_D[I_k,I_k]/Ay_D[I_j,I_j]
    return Ay_L,Ay_D,Ay_A

def D_L_design(Ay_A):
    Ay_D = np.matrix(np.zeros((len(Ay_A),len(Ay_A))))
    Ay_L = np.matrix(np.eye(len(Ay_A)))
    for I_i in range(len(Ay_A)):
        for I_j in range(len(Ay_A)):
            if I_i >= I_j:
                Ay_A,Ay_L,Ay_D = D_design_in(I_j,Ay_A,Ay_L,Ay_D)
                Ay_L,Ay_D,Ay_A = L_design_in(I_i,I_j,Ay_L,Ay_D,Ay_A)
    return Ay_L,Ay_D

if __name__ == '__main__':
#    Ay_A = np.matrix([[  4, 12,-16],
#                      [ 12, 37,-43],
#                      [-16,-43, 98]])
    Ay_A = np.matrix([[6.290,5.978,0.544],
                      [5.978,6.292,2.340],
                      [0.544,2.340,6.288]])
    Ay_L,Ay_D = D_L_design(Ay_A)