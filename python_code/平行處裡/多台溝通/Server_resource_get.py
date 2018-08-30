# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:05:59 2017

@author: owo
"""

import os
import numpy as np

def Fun_Search_resource():
    List_Resource = os.popen('pestat').readlines()[2:]
    Dist_Resource = {}
    for i in range(len(List_Resource)):
        if List_Resource[i][0:4] == 'lasc':
            Dist_Resource[List_Resource[i][0:6]] = float(List_Resource[i][31:33])/2 - float(List_Resource[i][16:21])
    np.save('Sever_resource.npy',Dist_Resource)

def Fun_Load_resource():
    return np.load('Sever_resource.npy').item()

if __name__ == '__main__':
    import Server_resource_get as Srg
    Srg.Fun_Search_resource()
    print(Srg.Fun_Load_resource())