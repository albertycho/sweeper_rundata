#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

print('find memhog perf')
cycles = 0
cCycles = 0
instrs= 0
iter_count=0
cCycle_ratio=0
ipcs=0
if exists('zsim_final.out'):
    zsimout = open('zsim_final.out','r')
    line = zsimout.readline()
    while line:
        is_memhog_core = False;
        if 'OCore1-18' in line: 
            is_memhog_core = True;
        if 'OCore1-19' in line: 
            is_memhog_core = True;
        if 'OCore1-20' in line: 
            is_memhog_core = True;
        if 'OCore1-21' in line: 
            is_memhog_core = True;
        if 'OCore1-22' in line: 
            is_memhog_core = True;
        if 'OCore1-23' in line: 
            is_memhog_core = True;

        if (is_memhog_core):
            line=zsimout.readline()
            ###parse out cycles
            tmp1=line.split('cycles: ')[1]
            tmp2=int(tmp1.split(' #')[0])
            cycles = cycles+tmp2
            
            line=zsimout.readline()
            ##parse out cCycles
            tmp1=line.split('cCycles: ')[1]
            tmp2=int(tmp1.split(' #')[0])
            cCycles = cCycles+tmp2

            line=zsimout.readline()
            ##parse out instrs
            tmp1=line.split('instrs: ')[1]
            tmp2=int(tmp1.split(' #')[0])
            instrs=instrs+tmp2
            break
        line=zsimout.readline()


    zsimout.close()

mh_iter_count = 0
loop_count_pc = 0 ##loop count per cycle
iter_count_name = 'memhog_25_iter_count.txt'
if exists(iter_count_name):
    f_mh_iter_count = open(iter_count_name, 'r')
    line = f_mh_iter_count.readline()
    mh_iter_count = int(line)
    f_mh_iter_count.close()


if (cycles!=0):
    cCycle_ratio = cCycles/cycles
    ipcs = instrs / cycles
    loop_count_pc = mh_iter_count / cycles


f_mh_stats = open('memhog_stats.txt','w')
f_mh_stats.write('memhog_stats,\n')
f_mh_stats.write('cycles, '+str(cycles)+'\n')
f_mh_stats.write('ipcs, '+str(ipcs)+'\n')
f_mh_stats.write('cCycle_ratio, '+str(cCycle_ratio)+'\n')
f_mh_stats.write('loop_count_per_cycle, '+str(loop_count_pc)+'\n')
f_mh_stats.close()

os.system('cat memhog_stats.txt >> stat_summary.txt')

print('mh_stats written')

