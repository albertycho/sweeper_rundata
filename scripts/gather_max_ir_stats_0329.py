#!/usr/bin/env python3

import os
import sys 
import argparse
import csv 
import math
import statistics
import numpy as np
from os.path import exists

parser = argparse.ArgumentParser()
#parser.add_argument('--out_file', type=str, default='max_ir_stats.csv')
#parser.add_argument('--out_file', type=str, default='max_ir_stats_0322_l3f_memhog_nonincl_noclean.csv')

#parser.add_argument('--out_file', type=str, default='max_ir_stats_0414_matmul_500_BATCH.csv')
#parser.add_argument('--out_file', type=str, default='max_ir_stats_0415_xmem_6MB.csv')
parser.add_argument('--out_file', type=str, default='max_ir_stats_0420_l3fwd_ALONE.csv')

args=parser.parse_args()

outfile = args.out_file

f1=open(outfile,'w')
#f1.write('cfg,max_ir,mbw,avg_st,avg_e2e,e2e_90,nic_rb_mr,nic_lb_mr,ddio_ways_mr,non_ddio_ways_mr,wr_lat_avg,rd_lat_avg,\n')
f1.write('cfg,max_ir,mbw,avg_st,avg_e2e,e2e_90,nic_rb_mr,nic_lb_mr,ddio_ways_mr,non_ddio_ways_mr,wr_lat_avg,rd_lat_avg,mh_ipcs,mh_l3_mr,mh_cCycle_ratio, core_rb_mr,\n')


#script_dir = '/shared/acho44/'

#regress_pre = '/shared/acho44/0415_l3fwd_xmem_BATCH_6MB/'
regress_pre = '/shared/acho44/0420_l3fwd_ALONE_BATCH/'



#psizes = ['1024','512']
psizes = ['1024']
rbcounts = ['2048','1024','512']
#rbcounts = ['1024','512','256']

#memconts = ['6','3','2','simplemem','ideal']
memconts = ['4']
#ddio_setups=['2','4','11','clean','clean11','cleans','cleans11']
ddio_setups=['2','6','12','ideal']
clean_setups=['clean','nocl']


max_ir='0'
mbw='0'
avg_st='0'
avg_e2e='0'
e2e_90='0'
nic_rb_mr='0'
nic_lb_mr='0'
ddio_ways_mr='0'
non_ddio_ways_mr='0'
wr_lat_avg='0'
rd_lat_avg='0'
###memhog stats
mh_ipcs='0'
mh_l3_mr='0'
mh_cCycle_ratio='0'

core_rb_mr ='0'

for ps in psizes:
    for rbc in rbcounts:
        for mc in memconts:
            for ds in ddio_setups:
                for cs in clean_setups:
                    target_path = regress_pre + ps+'pack_'+rbc+'recv_'+mc+'_batch32_'+ds+'ways_'+cs+'/max_IR_stat.csv'
                    print (target_path)

                    max_ir='0'
                    mbw='0'
                    avg_st='0'
                    avg_e2e='0'
                    e2e_90='0'
                    nic_rb_mr='0'
                    nic_lb_mr='0'
                    ddio_ways_mr='0'
                    non_ddio_ways_mr='0'
                    wr_lat_avg='0'
                    rd_lat_avg='0'
                    mh_ipcs='0'
                    mh_l3_mr='0'
                    mh_cCycle_ratio='0'

                    core_rb_mr ='0'

                    if os.path.isfile(target_path):

                        print (target_path)
                        f2=open(target_path,'r')
                        #f1.write(ps+'pack_'+rbc+'recv_'+mc+',')
                        f1.write(ps+'pack_'+rbc+'recv_'+mc+'_'+ds+'ways_'+cs+',')
                        line=f2.readline()
                        while line:
                            if 'max_ir' in line:
                                max_ir=line.split(',')[1]
                            if 'mbw' in line:
                                mbw=line.split(',')[1]
                            if 'avg_st' in line:
                                avg_st=line.split(',')[1]
                            if 'avg_e2e' in line:
                                avg_e2e=line.split(',')[1]
                            if 'e2e_90' in line:
                                e2e_90=line.split(',')[1]
                            if 'nic_rb_mr' in line:
                                nic_rb_mr=line.split(',')[1]
                            if 'nic_lb_mr' in line:
                                nic_lb_mr=line.split(',')[1]
                            if 'ddio_ways_mr' in line:
                                ddio_ways_mr=line.split(',')[1]
                            if 'non_ddio_ways_mr' in line:
                                non_ddio_ways_mr=line.split(',')[1]
                            if 'wr_lat_avg' in line:
                                wr_lat_avg=line.split(',')[1]
                            if 'rd_lat_avg' in line:
                                rd_lat_avg=line.split(',')[1]
                            if 'mh_ipcs' in line:
                                mh_ipcs=line.split(',')[1]
                            if 'mh_cCycle_ratio' in line:
                                mh_cCycle_ratio=line.split(',')[1]
                            if 'NNF_l3_mr,' in line:
                                mh_l3_mr=line.split(',')[1]

                            if 'core_rb_mr,' in line:
                                core_rb_mr=line.split(',')[1]


                            line=f2.readline()
                        f2.close()
                        f1.write(max_ir+','+mbw+','+avg_st+','+avg_e2e+','+e2e_90+','+nic_rb_mr+','+nic_lb_mr+','+ddio_ways_mr+','+non_ddio_ways_mr+','+wr_lat_avg+','+rd_lat_avg+','+mh_ipcs+','+mh_l3_mr+','+mh_cCycle_ratio+','+core_rb_mr+',\n')
                        #os.chdir(target_path)
                    else:
                        print('target path does not exits\n')
                        f1.write(ps+'pack_'+rbc+'recv_'+mc+'_'+ds+'ways_'+cs+',')
                        #f1.write(max_ir+','+mbw+','+avg_st+','+avg_e2e+','+e2e_90+','+nic_rb_mr+','+nic_lb_mr+','+ddio_ways_mr+','+non_ddio_ways_mr+ ','+wr_lat_avg+','+rd_lat_avg+',\n')
                        f1.write(max_ir+','+mbw+','+avg_st+','+avg_e2e+','+e2e_90+','+nic_rb_mr+','+nic_lb_mr+','+ddio_ways_mr+','+non_ddio_ways_mr+','+wr_lat_avg+','+rd_lat_avg+','+mh_ipcs+','+mh_l3_mr+','+mh_cCycle_ratio+','+core_rb_mr+',\n')


f1.close()

