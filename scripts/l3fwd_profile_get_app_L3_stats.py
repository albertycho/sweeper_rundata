#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists


tmp_nic_rb_mr=0
tmp_nic_lb_mr=0
tmp_ddio_ways_mr=0
tmp_non_ddio_ways_mr=0


nic_rb_mr=tmp_nic_rb_mr
nic_lb_mr=tmp_nic_lb_mr
ddio_ways_mr=tmp_ddio_ways_mr
non_ddio_ways_mr=tmp_non_ddio_ways_mr

app_miss_rate=0
app_miss_count=0
app_total_accesses=0

output_path_base = '/shared/acho44/0312_L3FWD_PROFILING_RUNS/'
#base_cfg_name = ' ddio_DDR4_base.cfg '
base_cfg_name = ' l3fwd_ddio.cfg '
#packet_sizes = [512, 1024]
#rb_counts = [256, 512, 1024]
#mcs = ['6']

packet_sizes = [512]
rb_counts = [256]
mcs = ['ideal']


batchsizes=['1']
date = '0312'
key_sizes=['1','1024','4096','16392','65536','262144']

outfile=open('0312_l3fwd_appL3stats_ideal.txt','w')
outfile.write('runcfg, app_l3_missrate, app_l3_total_accesses\n')
for mc in mcs:
    for ps in packet_sizes:
        for rbc in rb_counts:
            for bs in batchsizes: #just keeping the name convention
                for ks in key_sizes:
                    rb_pool_size=ps*rbc
                    outdirname =output_path_base+date+'_'+str(ps)+'_'+str(rbc)+'_mc'+mc+'_'+ks+'keys'
                    print(outdirname)
                    os.chdir(outdirname)
                    if exists(outdirname+'/stat_summary.txt'):
                        tmp_nic_rb_mr=0
                        tmp_nic_lb_mr=0
                        tmp_ddio_ways_mr=0
                        tmp_non_ddio_ways_mr=0
                        app_miss_rate=0
                        app_miss_count=0
    
                        stat_file = open('stat_summary.txt','r')
                        line = stat_file.readline()
                        while line:
                            if 'net_l3_miss_ratio_nic_rb,' in line:
                                tmp = line.split(',')[1]
                                tmp_nic_rb_mr=float(tmp)
                            if 'net_l3_miss_ratio_nic_lb,' in line:
                                tmp = line.split(',')[1]
                                tmp_nic_lb_mr=float(tmp)
                            if 'non_ddio_ways_miss_rate,' in line:
                                tmp = line.split(',')[1]
                                tmp_non_ddio_ways_mr=float(tmp)
                            if 'ddio_ways_miss_rate,' in line:
                                tmp = line.split(',')[1]
                                tmp_ddio_ways_mr=float(tmp)
                            if 'app_l3_miss_ratio,' in line:
                                tmp = line.split(',')[1]
                                app_miss_rate=float(tmp)                               
                            if 'app_l3_miss,' in line:
                                tmp = line.split(',')[1]
                                app_miss_count=float(tmp)
                            if 'app_l3_hit' in line:
                                tmp = line.split(',')[1]
                                app_hit=float(tmp)
                                app_total_accesses=app_miss_count+app_hit
                                
                              
                            line=stat_file.readline()
    
                        stat_file.close()
                        runcfg=str(ps)+'_'+str(rbc)+'_mc'+mc+'_'+ks+'keys'
                        outfile.write(runcfg+', '+str(app_miss_rate)+', '+str(app_total_accesses)+'\n')
    
outfile.close()


