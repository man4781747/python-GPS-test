# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 16:08:22 2018

@author: owo
"""
import DOY2GPSweek
from CustomValue import *
import ftplib

def SP3DataDownload(I_Year, I_Doy):
    if os.path.exists(S_SP3DataPath) == False:
        os.makedirs(S_SP3DataPath)
        
    sp3_url_path = r'pub/product/{0}/'
    sp3_dataname = r'igs{2}.sp3'
    
    S_GPSWeek = DOY2GPSweek.DOY2GPSweek(I_Year, I_Doy)
    
    path_local_sp3 = (S_SP3DataPath+sp3_dataname).format(I_Year, I_Doy, S_GPSWeek)
    sp3_chcek_num = 0
    
    while not os.path.isfile(path_local_sp3):
        if sp3_chcek_num > 2:
            print('!!!!!!!!!! {0:02d}/{1:03d} cont find sp3 data'.format(I_Year, I_Doy))
            os._exit()
        print('download sp3 data')
        sp3_dataname_chose = sp3_dataname.format(0,0,S_GPSWeek)+'.Z'
        sp3_dataname_chose_path = sp3_url_path.format(S_GPSWeek[0:4])
        
        login_rul = ftplib.FTP(r'ftp.igs.org')
        login_rul.login()
        login_rul.cwd(sp3_dataname_chose_path)
        login_rul.retrbinary("RETR " + sp3_dataname_chose ,open(path_local_sp3+'.Z', 'wb').write)
        login_rul.quit()
        if platform.system() == 'Linux':
            os.system('uncompress {0}'.format(path_local_sp3+'.Z'))
        elif platform.system() == 'Windows':
#            print('{0} x {1} {2} -y'.format(WinRARPath, path_local_sp3+'.Z', path_local_sp3))
            os.system('{0} x {1} {2} -y'.format(WinRARPath, path_local_sp3+'.Z', S_SP3DataPath))
        
        sp3_chcek_num += 1

if __name__ == '__main__':
    try:
        I_year = [int(sys.argv[1])]
        I_doy = [int(sys.argv[2])]
    except:
        I_year = int(input("I_year:"))
        I_doy = int(input("I_doy:"))
    SP3DataDownload(I_year,I_doy )