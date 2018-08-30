# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:05:08 2018

@author: owo
"""
import numpy as np
class NDataRead:
    def __init__(self, S_DataPath):
        self.Ay_NData = np.load(S_DataPath)
        
    def GetData(self, Ay_Pr, F_TimeInput):
        Ay_NDataChose = np.zeros((0,38))
        for I_SateNum in np.where(Ay_Pr != 0)[0]+1:
            Ay_NDataChose_ = self.Ay_NData[np.where(self.Ay_NData[:,0]==I_SateNum),:][0]
            F_TimeSec = Ay_NDataChose_[:,4]*60*60 + Ay_NDataChose_[:,5]*60 + Ay_NDataChose_[:,6]
            try:
                Ay_NDataChoseEnd = np.array([Ay_NDataChose_[np.where(F_TimeInput >= F_TimeSec)[0][-1],:]])
#               print(Ay_NDataChoseEnd)
            except:
                Ay_NDataChoseEnd = Ay_NDataChose_[0:1]
#                Ay_NDataChoseEnd = np.zeros((0,38))
            Ay_NDataChose = np.concatenate((Ay_NDataChose, Ay_NDataChoseEnd))
        return Ay_NDataChose, (Ay_NDataChose[:,0] - 1).astype('int')