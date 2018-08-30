# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 10:30:21 2017

@author: owo
"""

with open('./Binary2017-12-16_093014.obs') as f:
    test = f.readlines()

rrr = []
num = 0
while num < len(test):
    if test[num][0:2] != 'J ':
        rrr.append(test[num])
    num += 1