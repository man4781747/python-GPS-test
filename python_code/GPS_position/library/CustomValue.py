# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 15:06:03 2018

@author: owo
"""

global F_f1_hz
global F_f2_hz 
global F_err_cbias # code bias error std (m)
global F_std_brdcclk # error of broadcast clock (m)
global F_EFACT_GPS  # error factor: GPS 
global F_ERR_BRDCI  # broadcast iono model error factor
global F_ERR_SAAS
global F_OMGE       # /* earth angular velocity (IS-GPS) (rad/s) */
global F_C

F_err_cbias = 0.3  # code bias error std (m)
F_f1_hz = 1575.42
F_f2_hz = 1227.6
F_std_brdcclk = 30.0 # error of broadcast clock (m)
F_EFACT_GPS = 1.0  # error factor: GPS 
F_ERR_BRDCI = 0.5
F_ERR_SAAS = 0.3   # /* saastamoinen model error std (m) */
F_OMGE = 7.2921151467E-5  # /* earth angular velocity (IS-GPS) (rad/s) */
F_C = 299792458.0


global S_phase_data_path
global S_aeosv_data_path
global S_n_data_path
global S_ans_position_path

S_PATH = r'D:/Ddddd/python/2003/Odata/test'

#S_phase_data_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/phase_data/'
#S_aeosv_data_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/aeosv_data/'
#S_n_data_path = '/pub3/man4781747/GPS_data/n_data/'
#S_ans_position_path = '/pub3/man4781747/GPS_data/data20{0:02d}{1:03d}/position_data/'

S_phase_data_path   = S_PATH + '/data20{0:02d}{1:03d}/phase_data/'
S_aeosv_data_path   = S_PATH + '/data20{0:02d}{1:03d}/aeosv_data/'
S_n_data_path       = S_PATH + '/n_data/'
S_ans_position_path = S_PATH + '/data20{0:02d}{1:03d}/position_data/'