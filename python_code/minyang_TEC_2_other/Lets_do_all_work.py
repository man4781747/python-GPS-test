# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:38:00 2017

@author: owo
"""


import os

year_list = [int(x) for x in input('yy,yy(int): ').split()]    
doy_list = [int(x) for x in input('ddd,ddd(int): ').split()]        
processes_num = int(input("processes_num(int):"))
I_rate_of_data = int(input("I_rate_of_data:"))

for year in year_list:
    for doy in doy_list:
        print('{0:03d}\n'.format(doy))
        os.system('python ./async_garner_py3_muldays_argv.py {0} {1}'.format(year,doy)) 
        
        os.system('python ./d2o_mulsday_argv.py {0} {1}'.format(year,doy))
        
        ### matlab ####
        os.system('python ./rungnsstec_p_change_new.py {0} {1}'.format(year,doy))
        
        os.system('matlab15 -nodesktop -nodisplay -r rungnsstec_p_{0:02d}{1:03d}'.format(year,doy))
        
        os.remove('rungnsstec_p_{0:02d}{1:03d}.m'.format(year,doy))
        
        print('build odata dirs')        
        #################
        if os.path.exists('./data20{0:02d}{1:03d}/odata'.format(year,doy)) == False:
            os.makedirs('./data20{0:02d}{1:03d}/odata'.format(year,doy))
        
        print('move odata to odata dir')
        os.system('mv ./datanotminygang/**{1:03d}0.{0:02d}o ./data20{0:02d}{1:03d}/odata/'.format(year,doy))
        
        print('do minyang2aoves_m_argv.py \n\n')
        os.system('python ./minyang2aoves_m_argv.py {0} {1} {2}'.format(year,doy,processes_num,I_rate_of_data)) 
        
        print('do minyang2phase_m_argv.py \n\n')
        os.system('python ./minyang2phase_m_argv.py {0} {1} {2}'.format(year,doy,processes_num,I_rate_of_data)) 
        
        print('do phase2lose_m_argv.py \n\n')
        os.system('python ./phase2lose_m_argv.py {0} {1}'.format(year,doy)) 
        
        print('do phase2slip_m_argv.py \n\n')
        os.system('python ./phase2slip_m_argv.py {0} {1}'.format(year,doy)) 
        
        print('do v2ROTI_argv.py')
        os.system('python ./v2ROTI_argv.py {0} {1} \n\n'.format(year,doy)) 
        
        print('\rdoing odata2rnx2trkp_argv.py\r ',end='')
        os.system('python ./odata2rnx2trkp_argv.py {0} {1} {2}'.format(year,doy,processes_num)) 
        print('\rdoing trkt2npy_argv.py\r ',end='')
        os.system('python ./trkt2npy_argv.py {0} {1} {2}'.format(year,doy,processes_num)) 
        print('\rdoing trktnpy2position_argv.py\r ',end='')
        os.system('python ./trktnpy2position_argv.py {0} {1} {2}'.format(year,doy,processes_num)) 