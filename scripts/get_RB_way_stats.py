#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

f_nic_rb_ways = open('rb_ways_hit.txt','w')

#support upto 32 ways?
nic_rb_ways_hit = [0 for i in range(32)]
nic_rb_ways_miss = [0 for i in range(32)]

#if exists('zsim.out'):
#    zsimout = open('zsim.out','r')
if exists('zsim_final.out'):
    zsimout = open('zsim_final.out','r')
    line = zsimout.readline()
    while line:
        if 'l3-' in line:
            while not 'nic_rb_way_hits' in line:
                line=zsimout.readline()

            line=zsimout.readline()
            while not 'nic_rb_way_inserts' in line:
                tmp1=line.split(': ')
                way = int(tmp1[0])
                hitcount=int(tmp1[1])
                nic_rb_ways_hit[way]+=hitcount
                line=zsimout.readline()
            line=zsimout.readline()
            while not 'part' in line:
                tmp1=line.split(': ')
                way = int(tmp1[0])
                misscount=int(tmp1[1])
                nic_rb_ways_miss[way]+=misscount
                line=zsimout.readline()




        line=zsimout.readline()

    zsimout.close()
  
    for i in range(32):
        if(nic_rb_ways_hit[i] != 0):
            f_nic_rb_ways.write('way '+str(i)+', '+str(nic_rb_ways_hit[i])+' rb hits\n')

    for i in range(32):
        if(nic_rb_ways_miss[i] != 0):
            f_nic_rb_ways.write('way '+str(i)+', '+str(nic_rb_ways_miss[i])+' rb_misses\n')


    f_nic_rb_ways.close()
    
else:
    print('zsim_final.out not found\n')

