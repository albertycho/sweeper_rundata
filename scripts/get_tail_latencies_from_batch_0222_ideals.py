#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

f_means = open('means.csv','w')
f_90s   = open('ninety.csv','w')
f_95s   = open('95s.csv','w')
f_99s   = open('99s.csv','w')

f_max_IR_stat = open('max_IR_stat.csv','w')
max_ir=0
mbw=0
avg_st=0
avg_e2e=0
e2e_90=0
nic_rb_mr=0
nic_lb_mr=0
ddio_ways_mr=0
non_ddio_ways_mr=0
wr_lat_avg=0
rd_lat_avg=0


tmp_mbw=0
tmp_avg_st=0
tmp_avg_e2e=0
tmp_e2e_90=0
tmp_nic_rb_mr=0
tmp_nic_lb_mr=0
tmp_ddio_ways_mr=0
tmp_non_ddio_ways_mr=0
tmp_wr_lat_avg=0
tmp_rd_lat_avg=0





script_dir = '/shared/acho44/'
os.system('cp '+script_dir+'process_timestamps.py .')
os.system('cp '+script_dir+'get_tail_latencies_from_batch.py .')
os.system('cp '+script_dir+'process_zsim_out.py .')

os.system('rm get_mem_lat.py')
os.system('cp '+script_dir+'get_mem_lat.py .')
os.system('cp '+script_dir+'get_avg_mbw.py .')



#for dd in os.listdir('.'):
for jj in range(1,50,1):
    dd = '0'+str(jj)
    if exists(dd):
        print(dd)
        os.chdir(dd)
        if 'run_success' in os.listdir('.'):
            if 'timestamps_core_3.txt' in os.listdir('.'):
                os.system('python3 ../process_zsim_out.py')
                os.system('python3 ../process_timestamps.py')
                os.system('python3 ../get_mem_lat.py')
                #os.system('python3 ../get_l3misses_memaccesses.py')
                os.system('python3 ../get_avg_mbw.py')
                if exists('stat_summary.txt'):
                    tmp_mbw=0
                    tmp_avg_st=0
                    tmp_avg_e2e=0
                    tmp_e2e_90=0
                    tmp_nic_rb_mr=0
                    tmp_nic_lb_mr=0
                    tmp_ddio_ways_mr=0
                    tmp_non_ddio_ways_mr=0

                    stat_file = open('stat_summary.txt','r')
                    line = stat_file.readline()
                    while line:
                        if 'service_time' in line:
                            line = stat_file.readline()
                            line = stat_file.readline()
                            if not 'avg:' in line:
                                print('expected avg service time, not found\n')
                            tmp = line.split(' ')[1]
                            tmp_avg_st = float(tmp)
                        if 'avge2e' in line:
                            tmp = line.split(' ')[1]
                            f_means.write(dd+','+tmp)
                            tmp_avg_e2e=float(tmp)
                        if '90%' in line:
                            tmp = line.split(' ')[1]
                            f_90s.write(dd+','+tmp)
                            tmp_e2e_90=float(tmp)
                        if '95%' in line:
                            tmp = line.split(' ')[1]
                            f_95s.write(dd+','+tmp)
                        if '99%' in line:
                            tmp = line.split(' ')[1]
                            f_99s.write(dd+','+tmp)
                        if 'net_l3_miss_ratio_nic_rb' in line:
                            tmp = line.split(',')[1]
                            tmp_nic_rb_mr=float(tmp)
                        if 'net_l3_miss_ratio_nic_lb' in line:
                            tmp = line.split(',')[1]
                            tmp_nic_lb_mr=float(tmp)
                        if 'memory_controller_0_bandwidth.txt' in line:
                            tmp = line.split(': ')[1]
                            tmp_mbw=float(tmp)
                        if 'non_ddio_ways_miss_rate' in line:
                            tmp = line.split(',')[1]
                            tmp_non_ddio_ways_mr=float(tmp)
                        if 'ddio_ways_miss_rate' in line:
                            tmp = line.split(',')[1]
                            tmp_ddio_ways_mr=float(tmp)
                        if 'wr_lat_avg' in line:
                            tmp = line.split(',')[1]
                            tmp_wr_lat_avg=float(tmp)
                        if 'rd_lat_avg' in line:
                            tmp = line.split(',')[1]
                            tmp_rd_lat_avg=float(tmp)

                        line=stat_file.readline()

                    stat_file.close()
                    if (int(dd) > max_ir):
                        max_ir=int(dd)
                        mbw=tmp_mbw
                        avg_st=tmp_avg_st
                        avg_e2e=tmp_avg_e2e
                        e2e_90=tmp_e2e_90
                        nic_rb_mr=tmp_nic_rb_mr
                        nic_lb_mr=tmp_nic_lb_mr
                        ddio_ways_mr=tmp_ddio_ways_mr
                        non_ddio_ways_mr=tmp_non_ddio_ways_mr
                        wr_lat_avg=tmp_wr_lat_avg
                        rd_lat_avg=tmp_rd_lat_avg


        os.chdir('..')

f_means.close()
f_90s.close()
f_95s.close()
f_99s.close()
f_max_IR_stat.write('max_ir, '+str(max_ir)+',\n')
f_max_IR_stat.write('mbw, '+str(mbw)+',\n')
f_max_IR_stat.write('avg_st, '+str(avg_st)+',\n')
f_max_IR_stat.write('avg_e2e, '+str(avg_e2e)+',\n')
f_max_IR_stat.write('e2e_90, '+str(e2e_90)+',\n')
f_max_IR_stat.write('nic_rb_mr, '+str(nic_rb_mr)+',\n')
f_max_IR_stat.write('nic_lb_mr, '+str(nic_lb_mr)+',\n')
f_max_IR_stat.write('ddio_ways_mr, '+str(ddio_ways_mr)+',\n')
f_max_IR_stat.write('non_ddio_ways_mr, '+str(non_ddio_ways_mr)+',\n')
f_max_IR_stat.write('wr_lat_avg, '+str(wr_lat_avg)+',\n')
f_max_IR_stat.write('rd_lat_avg, '+str(rd_lat_avg)+',\n')

