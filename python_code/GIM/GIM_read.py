# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:47:29 2018

@author: owo
1. GIM2sTEC(Ay_TEC_lon,Ay_TEC_lat,Ay_GIM,Ay_elv):
丟入各 TEC點的 lon lat elv 以及 總共GIM的資料後輸出各TEC點的vTEC以及sTEC 

input:(Ay_TEC_lon,Ay_TEC_lat,Ay_GIM,Ay_elv)
Ay_TEC_lon: np.array (2880,32)
Ay_TEC_lat: np.array (2880,32)
Ay_GIM: np.array(71,73,25)  #(lat,lon,hr) lat:arange(-180,180,5)
                                          lon:arange(87.5,-87.5,2.5)
                                          hr: 0~24
Ay_elv: np.array (2880,32)           
              
output: (Ay_zi_stec, Ay_zi_vtec)        
Ay_zi_stec: np.array (2880,32)
Ay_zi_vtec: np.array (2880,32)

2. GIM2TEC_data_make(S_station_name,I_year,I_doy):
使用 GIM2sTEC() 來直接存取 GIM vTEC及sTEC資料
input:
S_station_name: "Str" EX: 'aknd'
I_year: int  EX: 15
I_doy:  int  EX: 73
 
3. GIM2globalTEC(I_year,I_doy):
將整天的GIM(已跑過Octave的GIM程式)轉換成 RIM(此非RIM_read.py 而是孫楊亦的RIM程式)使用的mat檔案
!!! 注意 此程式內的
    Lst_lon_chose = [110.,140.]
    Lst_lat_chose = [10.,40.]
    
    test_x = 1.
    test_y = 1.
    test_time = 1/60./2.
參數並無防呆 要確認此參數與RIM程式內參數設定相同

Code GIM 資料網址
ftp://ftp.aiub.unibe.ch/CODE/
"""

import scipy.io
import numpy as np
import matplotlib.pyplot as plt 
from scipy import ndimage
from slant2 import slant2
import os

def GIM2sTEC(Ay_TEC_lon,Ay_TEC_lat,Ay_GIM,Ay_elv):
    Ay_TEC_lon_chang = ((Ay_TEC_lon+180.)/5.).reshape(np.size(Ay_TEC_lon))
    Ay_TEC_lat_chang = ((Ay_TEC_lat+87.5)/2.5).reshape(np.size(Ay_TEC_lat))
    Ay_TEC_lon_chang[np.where(Ay_TEC_lon_chang==36.)]=np.nan
    Ay_TEC_lat_chang[np.where(Ay_TEC_lat_chang==35.)]=np.nan
    Ay_time = np.meshgrid(np.zeros(32),np.arange(0,24,24/2880))[1].reshape(2880*32)
    Ay_coords = np.concatenate((np.array([Ay_TEC_lat_chang]),np.array([Ay_TEC_lon_chang]),np.array([Ay_time])))
    Ay_zi_vtec = ndimage.map_coordinates(Ay_GIM, Ay_coords, order=3, mode='nearest').reshape(2880,32)
    Ay_zi_vtec[np.where(Ay_zi_vtec==0)]=np.nan
    Ay_zi_stec = Ay_zi_vtec/slant2(-Ay_elv+90,325)[0]
    return Ay_zi_stec, Ay_zi_vtec

def GIM2TEC_data_make(S_station_name,I_year,I_doy):
#    S_data_path = r'D:/Ddddd/python/2003/Odata/test/data20{0:02d}{1:03d}/'.format(I_year,I_doy)
    S_data_path = r'/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/'.format(I_year,I_doy)
    Ay_TEC_lon = np.load(S_data_path+'aeosv_data/30s/o{0}{1:03d}.npy'.format(S_station_name,I_doy))[:,:32]
    Ay_TEC_lat = np.load(S_data_path+'aeosv_data/30s/a{0}{1:03d}.npy'.format(S_station_name,I_doy))[:,:32]
    Ay_TEC_elv = np.load(S_data_path+'aeosv_data/30s/e{0}{1:03d}.npy'.format(S_station_name,I_doy))[:,:32]
    Ay_GIM = scipy.io.loadmat(S_data_path+'Code_GIM_data/codg{0:03d}0.mat'.format(I_doy))['tec']
    Ay_GIM_stec,Ay_GIM_vtec = GIM2sTEC(Ay_TEC_lon,Ay_TEC_lat,Ay_GIM,Ay_TEC_elv)
    
    S_data_save_path = S_data_path + 'GIM_svTEC/'
    if not os.path.exists(S_data_save_path):
        os.makedirs(S_data_save_path)
    np.save(S_data_save_path+'v{0}{1:02d}{2:03d}_GIM.npy'.format(S_station_name,I_year,I_doy),Ay_GIM_vtec)
    np.save(S_data_save_path+'s{0}{1:02d}{2:03d}_GIM.npy'.format(S_station_name,I_year,I_doy),Ay_GIM_stec)

def GIM2globalTEC(I_year,I_doy):
#    S_data_path = r'D:\Ddddd\python\2003\Odata\test\codg0730.mat'Code_GIM_data
    S_data_path = r'/nishome/man4781747/GIM/codg{0:03d}0.mat'.format(I_doy,I_year)
    S_GIM_mat_save_path = r'/pub3/man4781747/GPS_data/data20{1:02d}{0:03d}/Code_GIM_data/'.format(I_doy,I_year)

    Ay_lon = scipy.io.loadmat(S_data_path)['lon']
    Ay_lat = scipy.io.loadmat(S_data_path)['lat']
    Ay_TEC = scipy.io.loadmat(S_data_path)['tec']
    Ay_lon_net, Ay_lat_net = np.meshgrid(Ay_lon, Ay_lat)
    
    Lst_lon_chose = [110.,140.]
    Lst_lat_chose = [10.,40.]
    
    test_x = 1.
    test_y = 1.
    test_time = 1/60./2.
    
    Ay_lon_chose = Ay_lon[np.where((Ay_lon>= Lst_lon_chose[0])&(Ay_lon<= Lst_lon_chose[1]))]
    Ay_lat_chose = Ay_lat[np.where((Ay_lat>= Lst_lat_chose[0])&(Ay_lat<= Lst_lat_chose[1]))]
    Ay_TEC_chose = Ay_TEC[np.where((Ay_lat>= Lst_lat_chose[0])&(Ay_lat<= Lst_lat_chose[1]))[1],:,:][:,np.where((Ay_lon>= Lst_lon_chose[0])&(Ay_lon<= Lst_lon_chose[1]))[1],:]
    Ay_lon_chose_net, Ay_lat_chose_net = np.meshgrid(Ay_lon_chose, Ay_lat_chose)
    
    Ay_lon_linspace = np.arange(0,Lst_lon_chose[1]-Lst_lon_chose[0]+test_x,test_x)/(Lst_lon_chose[1]-Lst_lon_chose[0])*(len(Ay_lon_chose)-1)
    Ay_lat_linspace = np.arange(0,Lst_lat_chose[1]-Lst_lat_chose[0]+test_y,test_y)/(Lst_lat_chose[1]-Lst_lat_chose[0])*(len(Ay_lat_chose)-1)
    Ay_time_linspace = np.arange(0,len(Ay_TEC_chose[0,0,:]),test_time)
    
    
    Ay_lon_linspace_net, Ay_lat_linspace_net ,Ay_time_linspace_net = np.meshgrid(Ay_lon_linspace, Ay_lat_linspace, Ay_time_linspace)
    
    
    Ay_coords = np.concatenate((np.array([Ay_lat_linspace_net.reshape(len(Ay_lon_linspace)*len(Ay_lat_linspace)*len(Ay_time_linspace))]),
                                np.array([Ay_lon_linspace_net.reshape(len(Ay_lon_linspace)*len(Ay_lat_linspace)*len(Ay_time_linspace))]),
                                np.array([Ay_time_linspace_net.reshape(len(Ay_lon_linspace)*len(Ay_lat_linspace)*len(Ay_time_linspace))])
                                ))
    
    zi = ndimage.map_coordinates(Ay_TEC_chose, Ay_coords, order=3, mode='nearest').reshape(len(Ay_lat_linspace),len(Ay_lon_linspace),len(Ay_time_linspace))
    scipy.io.savemat(S_GIM_mat_save_path+'GIM_20{0:02d}{1:03d}_11014001_104001.mat'.format(I_year,I_doy),{'GIM_TEC':zi})
    
    return None
if __name__ == '__main__':
    try:
        import sys
        S_station_name = str(sys.argv[1])
        I_year = int(sys.argv[2])
        I_doy = int(sys.argv[3])
    except:
        S_station_name = str(input('S_station_name: '))
        I_year = int(input('I_year: '))
        I_doy = int(input('I_doy: '))
        
    GIM2globalTEC(I_year,I_doy)
#    
#    GIM2TEC_data_make(S_station_name,I_year,I_doy)
#    test_TEC_lon = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\oaknd073.npy')[:,:32]
#    test_TEC_lat = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\aaknd073.npy')[:,:32]
#    test_TEC_elv = np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\eaknd073.npy')[:,:32]
#    S_data_path = r'D:\Ddddd\python\2003\Odata\test\codg0730.mat'
#    Ay_TEC = scipy.io.loadmat(S_data_path)['tec']
#    test_go_s,test_go_v = GIM2sTEC(test_TEC_lon,test_TEC_lat,Ay_TEC,test_TEC_elv)
    
    
    
#Ay_TEC_chose = scipy.io.loadmat(S_data_path)['tec']
#test_TEC_lon = ((np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\oaknd073.npy')[:,:32]+180.)/5.).reshape(2880*32)
#test_TEC_lat = ((np.load(r'D:\Ddddd\python\2003\Odata\test\data2015073\aeosv_data\30s\aaknd073.npy')[:,:32]+87.5)/2.5).reshape(2880*32)
#test_TEC_lat[np.where(test_TEC_lat==35.)]=np.nan
#test_TEC_lon[np.where(test_TEC_lon==36.)]=np.nan
#test_time = np.meshgrid(np.zeros(32),np.arange(0,24,24/2880))[1].reshape(2880*32)
#test_all = np.concatenate((np.array([test_TEC_lon]),np.array([test_TEC_lat]),np.array([test_time])))
#zi = ndimage.map_coordinates(Ay_TEC_chose, test_all, order=3, mode='nearest').reshape(2880,32)

#S_data_path = r'D:\Ddddd\python\2003\Odata\test\codg0730.mat'
#
#Ay_lon = scipy.io.loadmat(S_data_path)['lon']
#Ay_lat = scipy.io.loadmat(S_data_path)['lat']
#Ay_TEC = scipy.io.loadmat(S_data_path)['tec']
#Ay_lon_net, Ay_lat_net = np.meshgrid(Ay_lon, Ay_lat)
#
#Lst_lon_chose = [110.,140.]
#Lst_lat_chose = [10.,40.]
#
##Lst_lon_chose = [-180.,180.]
##Lst_lat_chose = [-90.,90.]
#test_x = 1.
#test_y = 1.
#test_time = 1/60./2.
#
#Ay_lon_chose = Ay_lon[np.where((Ay_lon>= Lst_lon_chose[0])&(Ay_lon<= Lst_lon_chose[1]))]
##Ay_lon_chose = np.concatenate((Ay_lon_chose,np.zeros(1)+max(Ay_lon_chose)+5.))
#Ay_lat_chose = Ay_lat[np.where((Ay_lat>= Lst_lat_chose[0])&(Ay_lat<= Lst_lat_chose[1]))]
##Ay_lon_chose = np.concatenate((Ay_lat_chose,np.zeros(1)+max(Ay_lat_chose)+2.5))
#Ay_TEC_chose = Ay_TEC[np.where((Ay_lat>= Lst_lat_chose[0])&(Ay_lat<= Lst_lat_chose[1]))[1],:,:][:,np.where((Ay_lon>= Lst_lon_chose[0])&(Ay_lon<= Lst_lon_chose[1]))[1],:]
#Ay_lon_chose_net, Ay_lat_chose_net = np.meshgrid(Ay_lon_chose, Ay_lat_chose)
#
##Ay_lon_linspace = np.linspace(0,len(Ay_lon_chose)-1,test_x)
##Ay_lat_linspace = np.linspace(0,len(Ay_lat_chose)-1,test_y)
##Ay_time_linspace = np.linspace(0,len(Ay_TEC_chose[0,0,:]),test_time)
#
#Ay_lon_linspace = np.arange(0,Lst_lon_chose[1]-Lst_lon_chose[0]+test_x,test_x)/(Lst_lon_chose[1]-Lst_lon_chose[0])*(len(Ay_lon_chose)-1)
#Ay_lat_linspace = np.arange(0,Lst_lat_chose[1]-Lst_lat_chose[0]+test_y,test_y)/(Lst_lat_chose[1]-Lst_lat_chose[0])*(len(Ay_lat_chose)-1)
#Ay_time_linspace = np.arange(0,len(Ay_TEC_chose[0,0,:]),test_time)
#
##Ay_lon_loc_num = np.arange(0,test_x).astype('int')
##Ay_lat_loc_num = np.arange(0,test_y).astype('int')
##Ay_time_loc_num = np.arange(0,test_time).astype('int')
#
#Ay_lon_linspace_net, Ay_lat_linspace_net ,Ay_time_linspace_net = np.meshgrid(Ay_lon_linspace, Ay_lat_linspace, Ay_time_linspace)
#
##Ay_lon_loc_num_net, Ay_lat_loc_num_net ,Ay_time_loc_num_net = np.meshgrid(Ay_lon_loc_num, Ay_lat_loc_num, Ay_time_loc_num)
#
#
#Ay_coords = np.concatenate((np.array([Ay_lat_linspace_net.reshape(len(Ay_lon_linspace)*len(Ay_lat_linspace)*len(Ay_time_linspace))]),
#                            np.array([Ay_lon_linspace_net.reshape(len(Ay_lon_linspace)*len(Ay_lat_linspace)*len(Ay_time_linspace))]),
#                            np.array([Ay_time_linspace_net.reshape(len(Ay_lon_linspace)*len(Ay_lat_linspace)*len(Ay_time_linspace))])
#                            ))
##Ay_coords_loc = np.concatenate((np.array([Ay_lat_loc_num_net.reshape(len(Ay_lon_loc_num)*len(Ay_lat_loc_num)*len(Ay_time_loc_num))]),
##                            np.array([Ay_lon_loc_num_net.reshape(len(Ay_lon_loc_num)*len(Ay_lat_loc_num)*len(Ay_time_loc_num))]),
##                            np.array([Ay_time_loc_num_net.reshape(len(Ay_lon_loc_num)*len(Ay_lat_loc_num)*len(Ay_time_loc_num))])
##                            ))
#
#zi = ndimage.map_coordinates(Ay_TEC_chose, Ay_coords, order=3, mode='nearest').reshape(len(Ay_lat_linspace),len(Ay_lon_linspace),len(Ay_time_linspace))
#
##test = Ay_coords_loc[1,:].reshape(len(Ay_lon_linspace),len(Ay_lat_linspace),len(Ay_time_linspace))
#
#
#Ay_lat_linspace_net_test = Ay_lat_linspace_net[::-1,:,:]
#
#i = 0
#while i < 3000:
#    plt.figure(1)
##    Ay_lon_pcolor_test = 
#    test = plt.pcolor(Ay_lon_chose_net,Ay_lat_chose_net,Ay_TEC_chose[:,:,int(i/120)])
##    test = plt.scatter(Ay_lon_chose_net,Ay_lat_chose_net,c=Ay_TEC_chose[:,:,int(i/120)])
#    plt.title(i)
#    plt.clim(20,60)
##    if i%40 == 0:
##        plt.colorbar()
#    plt.pause(0.01)
#
#    if i%40 == 0:
#        plt.clf()
#    plt.figure(2)
#    test_2 = plt.pcolor(Ay_lon_linspace_net[:,:,0]/len(Ay_lon_chose)*(Lst_lon_chose[1]-Lst_lon_chose[0])+Lst_lon_chose[0],
#                        Ay_lat_linspace_net[::-1,:,0]/len(Ay_lat_chose)*(Lst_lat_chose[1]-Lst_lat_chose[0])+Lst_lat_chose[0],
#                        zi[:,:,i])
##    test_2 = plt.scatter(Ay_lon_linspace_net[:,:,0]/len(Ay_lon_chose)*(Lst_lon_chose[1]-Lst_lon_chose[0])+Lst_lon_chose[0],
##                        Ay_lat_linspace_net[::-1,:,0]/len(Ay_lat_chose)*(Lst_lat_chose[1]-Lst_lat_chose[0])+Lst_lat_chose[0],
##                        c=zi[:,:,i])
#    plt.title(i)
#    plt.clim(20,60)
##    if i%40 == 0:
##        plt.colorbar()
#    plt.pause(0.01)
#    
#    if i%40 == 0:
#        plt.clf()
#    i += 1
#    if i == 3000:
#        i = 0