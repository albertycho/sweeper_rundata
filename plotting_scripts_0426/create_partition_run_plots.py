#!/usr/bin/env python3

import os
import sys
import csv
import math

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str, default='max_ir_stats.csv')  
args = parser.parse_args()
infile = args.infile

#os.system('mkdir 512')
#os.system('mkdir 1024')
#os.system('mkdir 2048')
#
#os.systme('grep -ir "1024pack_512recv" '+infile+'> 512/512_stats.csv')
#os.systme('grep -ir "1024pack_1024recv" '+infile+'> 1024/1024_stats.csv')
#os.systme('grep -ir "1024pack_2048recv" '+infile+'> 2048/2048_stats.csv')

curdir=os.getcwd()

packet_sizes = ['1024','2048']
for ps in packet_sizes:
    os.system('mkdir '+ps)
    ###os.system('grep -ir /"1024pack_/"'+ps+'recv" '+infile+'/> '+ps+'//'+ps+'_stats.csv')
    #os.system('grep -ir "1024pack_"'+ps+'recv" '+infile+'> '+ps+'/'+ps+'_stats.csv')
    #os.system('grep -ir "1024pack_'+ps+'recv" '+infile+'> '+ps+'/'+ps+'_stats.csv')
    os.system('grep -ir "512pack_'+ps+'recv" '+infile+'> '+ps+'/'+ps+'_stats.csv')
    #os.system('cd '+ps)
    os.chdir(ps)
    print(os.getcwd())
    #os.system('~/INDIE/plot_maxIRstats_partition_IR_AND_IPC.py --infile '+ps+'_stats.csv')
    os.system('../../plot_maxIRstats_partition_IR_AND_IPC.py --infile '+ps+'_stats.csv')
    #print('~/INDIE/plot_maxIRstats_partition_IR_AND_IPC.py --infile '+ps+'_stats.csv')
    os.system('~/INDIE/plot_maxIRstats_partition.py --infile '+ps+'_stats.csv')
    #os.system('cd ..')
    os.chdir(curdir)
