#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

script_dir = '/shared/acho44/'
os.system('cp '+script_dir+'process_zsim_out.py .')

#os.system('rm get_mem_lat.py')
os.system('cp '+script_dir+'get_mem_lat.py .')
os.system('cp '+script_dir+'get_avg_mbw.py .')
os.system('cp '+script_dir+'get_memhog_perf.py .')

f1=open('leakyDMA_stats.csv','w')
f1.write('setup, interval, nic_rb_mr, core_rb_mr, mbw, NNF_l3_mr,\n')

f2=open('mbd_stats.csv','w')
f2.write('setup,app_dirty_evct,rb_dirty_evct,lb_dirty_evct,NF_mem_acc,lb_mem_acc,rb_mem_acc,memhog_acc\n')


for dd in os.listdir('.'):
#for jj in range(1,50,1):
    #dd = '0'+str(jj)
    if os.path.isdir(dd):
        print(dd)
        os.chdir(dd)
        interval='0';
        nic_rb_mr='0';
        core_rb_mr='0';
        mbw='0';

        app_dirty_evict='0'                                      
        rb_dirty_evict='0'                                       
        lb_dirty_evict='0'                                   
        NF_app_mem_access='0' 
        memhog_app_mem_access='0'                                 
        lb_mem_access='0'                                         
        rb_mem_access='0'
        NNF_l3_mr = '0'


        if 'run_success' in os.listdir('.'):
            if 'timestamps_core_3.txt' in os.listdir('.'):
                os.system('python3 ../process_zsim_out.py')
                #os.system('python3 ../process_timestamps.py')
                os.system('python3 ../get_mem_lat.py')
                #os.system('python3 ../get_l3misses_memaccesses.py')
                os.system('python3 ../get_avg_mbw.py')
                os.system('python3 ../get_memhog_perf.py')
                interval='0';
                nic_rb_mr='0';
                core_rb_mr='0';
                mbw='0';

                app_dirty_evict='0'                                      
                rb_dirty_evict='0'                                       
                lb_dirty_evict='0'                                   
                NF_app_mem_access='0' 
                memhog_app_mem_access='0'                                 
                lb_mem_access='0'                                         
                rb_mem_access='0'
                NNF_l3_mr = '0'

                if exists('stat_summary.txt'):
                    stat_file = open('stat_summary.txt','r')

                    line = stat_file.readline()
                    while line:
                        if 'average interval' in line:
                            tmp = line.split(': ')[1]
                            interval=tmp.replace("\n","")
                        if 'net_l3_miss_ratio_nic_rb' in line:
                            tmp = line.split(',')[1]
                            nic_rb_mr=tmp    
                        if 'net_l3_miss_ratio_core_rb' in line:
                            tmp = line.split(',')[1]
                            core_rb_mr=tmp
                        if 'memory_controller_0_bandwidth.txt' in line:
                            tmp = line.split(': ')[1]
                            mbw=tmp.replace("\n","")

                        ##################################
                        if 'app_dirty_evict' in line:
                            tmp = line.split(',')[1]
                            app_dirty_evict=(tmp)

                        if 'rb_dirty_evict' in line:
                            tmp = line.split(',')[1]
                            rb_dirty_evict=(tmp)

                        if 'lb_dirty_evict' in line:
                            tmp = line.split(',')[1]
                            lb_dirty_evict=(tmp)
                        if 'NF_app_mem_access' in line:
                            tmp = line.split(',')[1]
                            NF_app_mem_access=(tmp)
                        if 'memhog_app_mem_access' in line:
                            tmp = line.split(',')[1]
                            memhog_app_mem_access=(tmp)
                        if 'rb_mem_access' in line:
                            tmp = line.split(',')[1]
                            rb_mem_access=(tmp)
                        if 'lb_mem_access' in line:
                            tmp = line.split(',')[1]
                            lb_mem_access=(tmp)
                        if 'app_l3_miss_ratio_NNF,' in line:
                            tmp = line.split(',')[1]
                            NNF_l3_mr=tmp



                        
                        line=stat_file.readline()
                else:
                    print('stat_summary.txt did not exist')

  
                    
                f1.write(dd+', '+interval+','+ nic_rb_mr+','+ core_rb_mr+','+ mbw+','+NNF_l3_mr+',\n')
                f2.write(dd+', '+app_dirty_evict+','+rb_dirty_evict+','+lb_dirty_evict+','+NF_app_mem_access+','+memhog_app_mem_access+','+rb_mem_access+','+lb_mem_access+',\n')
                
                ##     rb_dirty_evict=0
                ##     lb_dirty_evict=0
                ##     NF_app_mem_access=0
                ##     memhog_app_mem_access=0
                ##     lb_mem_access=0
                ##     rb_mem_access=0

                ##    stat_file = open('stat_summary.txt','r')
                ##    line = stat_file.readline()
                ##    while line:
                ##        if 'service_time' in line:
                ##            line = stat_file.readline()
                ##            line = stat_file.readline()
                ##            if not 'avg:' in line:
                ##                print('expected avg service time, not found\n')
                ##            tmp = line.split(' ')[1]
                ##             avg_st = float(tmp)
                ##        if 'avge2e' in line:
                ##            tmp = line.split(' ')[1]
                ##            f_means.write(dd+','+tmp)
                ##             avg_e2e=float(tmp)
                ##        if '90%' in line:
                ##            tmp = line.split(' ')[1]
                ##            f_90s.write(dd+','+tmp)
                ##             e2e_90=float(tmp)

        else:
            print("didn't run_success")
            f1.write(dd+', '+interval+','+ nic_rb_mr+','+ core_rb_mr+','+ mbw+','+NNF_l3_mr+',\n')
            f2.write(dd+', '+app_dirty_evict+','+rb_dirty_evict+','+lb_dirty_evict+','+NF_app_mem_access+','+memhog_app_mem_access+','+rb_mem_access+','+lb_mem_access+',\n')
        os.chdir('..')

f1.close()
f2.close()
