# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:55:37 2018

@author: owo

1. RIM_read(S_station_name,I_year,I_doy):
使用孫楊亦的RIM程式輸出之 RIM_data.mat 來內差出各TEC點的 sTEC值以及vTEC值
input:
    S_station_name: Str 
    I_year: int  EX:15
    I_doy: int EX: 73
注意!!!
程式內
    Lst_lon_chose = [110.,140.]
    Lst_lat_chose = [10.,40.]
    test_x = 1.
    test_y = 1.
經緯網格參數請確認與 GIM_read 以及 孫楊亦的RIM程式內經緯網格一致(無防呆小心)
"""
import scipy.io
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt 
from slant2 import slant2

def RIM_read(S_station_name,I_year,I_doy):
    Lst_lon_chose = [110.,140.]
    Lst_lat_chose = [10.,40.]
        
    test_x = 1.
    test_y = 1.
    
    S_data_path = r'/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/'.format(I_year,I_doy)
    S_data_save_path = S_data_path + 'GIM_svTEC/'
#    S_RIM_data_path = r'D:/Ddddd/python/2003/Odata/test/RIM2015073.mat'
#    S_aeosv_data_path = r'D:/Ddddd/python/2003/Odata/test/data2015073/aeosv_data/30s/'
    S_RIM_data_path = S_data_path + 'Code_GIM_data/'
    S_aeosv_data_path = S_data_path + 'aeosv_data/30s/'
    Ay_TEC_lon = np.load(S_aeosv_data_path+'o{0}{1:03d}.npy'.format(S_station_name,I_doy))[:,:32].reshape(2880*32)
    Ay_TEC_lat = np.load(S_aeosv_data_path+'a{0}{1:03d}.npy'.format(S_station_name,I_doy))[:,:32].reshape(2880*32)
    Ay_TEC_elv = np.load(S_aeosv_data_path+'e{0}{1:03d}.npy'.format(S_station_name,I_doy))[:,:32]
    Ay_TEC_lon[np.where(Ay_TEC_lon==0)]=np.nan
    Ay_TEC_lat[np.where(Ay_TEC_lat==0)]=np.nan
    Ay_TEC_lon -= Lst_lon_chose[0]
    Ay_TEC_lat -= Lst_lat_chose[0]
    Ay_TEC_lon /= test_x
    Ay_TEC_lat /= test_y
    Ay_time = (np.meshgrid(np.arange(0,2880,1),np.zeros(32))[0].T).reshape(2880*32)
    
    Ay_coords = np.concatenate((np.array([Ay_time]),np.array([Ay_TEC_lat]),np.array([Ay_TEC_lon])))
    
    Ay_RIM_data = np.asarray(scipy.io.loadmat(S_RIM_data_path+'RIM20{0:02d}{1:03d}.mat'.format(I_year,I_doy))['RIM_cell'])
    Ay_RIM_data = np.asarray(scipy.io.loadmat(r'D:\Ddddd\python\2003\Odata\test\RIM2015073.mat')['RIM_cell'])

    
    Ay_RIM_GIM = np.zeros((len(Ay_RIM_data),31,31))
    Ay_RIM_RIM = np.zeros((len(Ay_RIM_data),31,31))
    Ay_RIM_tec = np.zeros((len(Ay_RIM_data),31,31))
    
    for i in range(len(Ay_RIM_data)):
        Ay_RIM_tec[i,:,:] = Ay_RIM_data[i,1][::-1,:]
        Ay_RIM_GIM[i,:,:] = Ay_RIM_data[i,0][::-1,:]
        Ay_RIM_RIM[i,:,:] = Ay_RIM_data[i,2][::-1,:]
    
    Ay_RIM_vtec = ndimage.map_coordinates(Ay_RIM_RIM, Ay_coords, order=3, mode='nearest').reshape(2880,32)
    Ay_GIM_vtec = ndimage.map_coordinates(Ay_RIM_GIM, Ay_coords, order=3, mode='nearest').reshape(2880,32)
    Ay_RIM_stec = Ay_RIM_vtec/slant2(-Ay_TEC_elv+90,325)[0]
    Ay_GIM_stec = Ay_GIM_vtec/slant2(-Ay_TEC_elv+90,325)[0]
    
    np.save(S_data_save_path+'v{0}{1:02d}{2:03d}_GIM.npy'.format(S_station_name,I_year,I_doy),Ay_GIM_vtec)
    np.save(S_data_save_path+'s{0}{1:02d}{2:03d}_GIM.npy'.format(S_station_name,I_year,I_doy),Ay_GIM_stec)
    
    np.save(S_data_save_path+'v{0}{1:02d}{2:03d}_RIM.npy'.format(S_station_name,I_year,I_doy),Ay_RIM_vtec)
    np.save(S_data_save_path+'s{0}{1:02d}{2:03d}_RIM.npy'.format(S_station_name,I_year,I_doy),Ay_RIM_stec)

if __name__ == '__main__':
    RIM_read('aknd',15,73)
#Lst_lon_chose = [110.,140.]
#Lst_lat_chose = [10.,40.]
#    
#test_x = 1.
#test_y = 1.
#test_time = 1/60./2.
#
#S_RIM_data_path = r'D:/Ddddd/python/2003/Odata/test/RIM2015073.mat'
#S_aeosv_data_path = r'D:/Ddddd/python/2003/Odata/test/data2015073/aeosv_data/30s/'
#Ay_TEC_lon = np.load(S_aeosv_data_path+'oaknd073.npy')[:,:32].reshape(2880*32)
#Ay_TEC_lat = np.load(S_aeosv_data_path+'aaknd073.npy')[:,:32].reshape(2880*32)
#Ay_TEC_elv = np.load(S_aeosv_data_path+'eaknd073.npy')[:,:32]
#Ay_TEC_lon[np.where(Ay_TEC_lon==0)]=np.nan
#Ay_TEC_lat[np.where(Ay_TEC_lat==0)]=np.nan
#Ay_TEC_lon -= Lst_lon_chose[0]
#Ay_TEC_lat -= Lst_lat_chose[0]
#Ay_TEC_lon /= test_x
#Ay_TEC_lat /= test_y
#Ay_time = (np.meshgrid(np.arange(0,2880,1),np.zeros(32))[0].T).reshape(2880*32)
#
#Ay_coords = np.concatenate((np.array([Ay_time]),np.array([Ay_TEC_lat]),np.array([Ay_TEC_lon])))
#
#Ay_RIM_data = np.asarray(scipy.io.loadmat(S_RIM_data_path)['RIM_cell'])
#
#Ay_RIM_GIM = np.zeros((len(Ay_RIM_data),31,31))
#Ay_RIM_RIM = np.zeros((len(Ay_RIM_data),31,31))
#
#for i in range(len(Ay_RIM_data)):
#    Ay_RIM_GIM[i,:,:] = Ay_RIM_data[i,0][::-1,:]
#    Ay_RIM_RIM[i,:,:] = Ay_RIM_data[i,2][::-1,:]
#
#Ay_RIM_vtec = ndimage.map_coordinates(Ay_RIM_RIM, Ay_coords, order=3, mode='nearest').reshape(2880,32)
#Ay_GIM_vtec = ndimage.map_coordinates(Ay_RIM_GIM, Ay_coords, order=3, mode='nearest').reshape(2880,32)
#Ay_RIM_stec = Ay_RIM_vtec/slant2(-Ay_TEC_elv+90,325)[0]
#Ay_GIM_stec = Ay_GIM_vtec/slant2(-Ay_TEC_elv+90,325)[0]
#
#if True:
#    for i in range(2880):
#        plt.subplot(1,2,1)
#        plt.pcolor(Ay_RIM_GIM[i,::-1,:])
#        plt.title(i)
#        plt.clim(20,60)
#        if i%10 == 0:
#            plt.clf()
#            plt.subplot(1,2,1)
#            plt.pcolor(Ay_RIM_GIM[i,::-1,:])
#            plt.title(i)
#        plt.clim(20,60)
#        
#        plt.pause(0.01)
#    
#            
#        plt.subplot(1,2,2)
#        plt.pcolor(Ay_RIM_RIM[i,::-1,:])
#        plt.title(i)
#        plt.clim(20,60)
#        if i%10 == 0:
#            plt.clf()
#            plt.subplot(1,2,2)
#            plt.pcolor(Ay_RIM_RIM[i,::-1,:])
#            plt.title(i)
#            plt.clim(20,60)
#        plt.pause(0.01)
