# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 11:37:01 2018

@author: owo
"""

import datetime
def YMD2DOY(I_year,I_month,I_day):
    Mobj_date_input = datetime.datetime(I_year,I_month,I_day)
    Mobj_GPSweek_start = datetime.datetime(I_year,1,1)
    I_GPSweek_day = (Mobj_date_input - Mobj_GPSweek_start).days
    return I_GPSweek_day+1

if __name__ == '__main__':
    print(YMD2DOY(15,3,14))