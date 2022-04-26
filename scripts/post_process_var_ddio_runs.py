#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists


script_dir = '/shared/acho44/'
#regress_pre = '/shared/acho44/0329_l3fwd_llc_resident_memhog_VAR_POLICIES/'
#regress_pre = '/shared/acho44/0417_l3fwd_xmem_6MB_partition_rerun_BATCH/'
#regress_pre = '/shared/acho44/0419_l3fwd_xmem_varddio_12C_BATCH/'
regress_pre = '/shared/acho44/0420_l3fwd_xmem_varddio_12C_DDR32_BATCH/'
psizes = {'1024'}
rbcounts = {'1024','2048'}

#memconts = {'6','4','2','simplemem','ideal'}
memconts = {'4'}

#ddio_setups=['2','4','11','clean','clean11','cleans','cleans11']
#ddio_setups=['2','11','clean','clean11']
ddio_setups=['clean','nocl']

partition_setups=['2_10','4_8','6_6','8_4','10_2']
ddio_ways = ['2','4','6','8','10','12'] 

for ps in psizes:
    for ds in ddio_setups:
        for rbc in rbcounts:
            for mc in memconts:
                for dw in ddio_ways:
                    #target_path = regress_pre + ps+'pack_'+rbc+'recv/ddio_var_mem_ctrl/'+mc+'/'+day
                    #target_path = regress_pre + str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_'+day+'_batch_32'
                    target_path = regress_pre + str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_batch_32'+ds+'_'+dw+'ways'
                    print (target_path)
                    if os.path.isdir(target_path):
                        os.chdir(target_path)
                        print('running postprocessing script')
                        os.system('/shared/acho44/get_tail_latencies_from_batch.py')
                        #os.system('ls')
                    else:
                        print('target path does not exits\n')


