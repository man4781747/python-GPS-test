# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 21:33:09 2018

@author: owo
"""
import datetime

def DOY2GPSweek(I_year,I_doy):
    Mobj_date_input = datetime.datetime.strptime('20{0:02d} {1:03d}'.format(I_year,I_doy), '%Y %j')
#    I_month = int(Mobj_date_input.strftime('%m'))
#    I_day  = int(Mobj_date_input.strftime('%d'))
#    
    Mobj_GPSweek_start = datetime.datetime(1980,1,6)
    
    
    I_GPSweek_day = (Mobj_date_input - Mobj_GPSweek_start).days
    
    S_GPSweek = "{0}{1}".format(int(I_GPSweek_day/7),I_GPSweek_day%7)
    return S_GPSweek
