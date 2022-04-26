#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists


output_path_base = '/shared/acho44/0420_l3fwd_ALONE_BATCH/'
#base_cfg_name = ' l3fwd_ddio.cfg '
base_cfg_name = ' l3fwd_ddio_ICL.cfg '
#packet_sizes = [512, 1024]
packet_sizes = [1024]
rb_counts = [512,1024,2048]
mcs = ['4']
#num_keys = '16384'
num_keys = '1024'

batchsizes=['32']

ddio_ways=['2','6','12','ideal']
#clean_setup=['clean','nocl']
clean_setup=['clean','nocl']



for ps in packet_sizes:
    for ds in ddio_ways:
        for rbc in rb_counts:
            for mc in mcs:
                for bs in batchsizes: #just keeping the name convention
                    for cs in clean_setup:
                        target_path=output_path_base+str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_batch'+bs+'_'+ds+'ways_'+cs
                        print (target_path)
                        if os.path.isdir(target_path):
                            os.chdir(target_path)
                            print('running postprocessing script')
                            os.system('/shared/acho44/get_tail_latencies_from_batch.py')
                            #os.system('ls')
                        else:
                            print('target path does not exits\n')

#script_dir = '/shared/acho44/'
##regress_pre = '/shared/acho44/0329_l3fwd_llc_resident_memhog_VAR_POLICIES/'
#regress_pre = '/shared/acho44/0420_l3fwd_ALONE_BATCH/'
#psizes = {'1024'}
#rbcounts = {'512','1024','2048'}
#
#memconts = {'4'}
#
##ddio_setups=['2','4','11','clean','clean11','cleans','cleans11']
#ddio_setups=['2','6','12']
#clean_setup=['clean','nocl']
#
#for ps in psizes:
#    for ds in ddio_setups:
#        for rbc in rbcounts:
#            for mc in memconts:
#                #target_path = regress_pre + ps+'pack_'+rbc+'recv/ddio_var_mem_ctrl/'+mc+'/'+day
#                #target_path = regress_pre + str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_'+day+'_batch_32'
#                target_path = regress_pre + str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_batch_32'+ds+'ways'
#                print (target_path)
#                if os.path.isdir(target_path):
#                    os.chdir(target_path)
#                    print('running postprocessing script')
#                    os.system('/shared/acho44/get_tail_latencies_from_batch.py')
#                    #os.system('ls')
#                else:
#                    print('target path does not exits\n')
#
#
