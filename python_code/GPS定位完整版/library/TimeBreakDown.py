# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 13:38:49 2018

@author: owo
"""

class TimeBreakDown:
    def __init__(self, F_Time):
        self.I_TimeInt = int(F_Time)
        self.F_TimeDecimal = F_Time%1
        self.F_TimeTotal = self.I_TimeInt + self.F_TimeDecimal