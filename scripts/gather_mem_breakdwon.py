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
#parser.add_argument('--out_file', type=str, default='mem_breakdown.csv')
parser.add_argument('--out_file', type=str, default='0420_l3fwd_alone_mem_breakdown.csv')

args=parser.parse_args()

outfile = args.out_file

f1=open(outfile,'w')
#f1.write('cfg,max_ir,mbw,avg_st,avg_e2e,e2e_90,nic_rb_mr,nic_lb_mr,ddio_ways_mr,non_ddio_ways_mr,wr_lat_avg,rd_lat_avg,mh_ipcs,mh_lcpc,mh_cCycle_ratio,\n')

f1.write('cfg,app_dirty_evict, rb_dirty_evict, lb_dirty_evict, NF_app_access, memhog_access, rb_access, lb_access,\n')

#script_dir = '/shared/acho44/'

#regress_pre = '/shared/acho44/0328_l3fwd_alone_oldeviction/'
regress_pre = '/shared/acho44/0420_l3fwd_ALONE_BATCH/'



#psizes = ['1024','512']
psizes = ['1024']
rbcounts = ['2048','1024','512']
#rbcounts = ['1024','512','256']

#memconts = ['6','3','2','simplemem','ideal']
memconts = ['4']
#ddio_setups=['2','4','11','clean','clean11','cleans','cleans11']
#ddio_setups=['2','12','clean','clean12']
ddio_setups=['2','6','12','ideal']                                              
clean_setups=['clean','nocl']                                                   
                              



#mem accesses        
app_dirty_evict        ='0'      
rb_dirty_evict         ='0'      
lb_dirty_evict         ='0'     
NF_app_mem_access      ='0'     
memhog_app_mem_access  ='0' 
rb_mem_access          ='0'  
lb_mem_access          ='0'  



for ps in psizes:
    for rbc in rbcounts:
        for mc in memconts:
            for ds in ddio_setups:
                for cs in clean_setups:
                    target_path = regress_pre + ps+'pack_'+rbc+'recv_'+mc+'_batch32_'+ds+'ways_'+cs+'/max_IR_stat.csv'
                    #print (target_path)

                    app_dirty_evict        ='0'      
                    rb_dirty_evict         ='0'      
                    lb_dirty_evict         ='0'     
                    NF_app_mem_access      ='0'     
                    memhog_app_mem_access  ='0' 
                    rb_mem_access          ='0'  
                    lb_mem_access          ='0'  



                    if os.path.isfile(target_path):

                        print (target_path)
                        f2=open(target_path,'r')
                        #f1.write(ps+'pack_'+rbc+'recv_'+mc+',')
                        f1.write(ps+'pack_'+rbc+'recv_'+mc+'_'+ds+'ways_'+cs+',')
                        line=f2.readline()
                        while line:
                            if 'app_dirty_evict' in line:
                                app_dirty_evict=line.split(',')[1]
                            if 'rb_dirty_evict' in line:
                                rb_dirty_evict=line.split(',')[1]
                            if 'lb_dirty_evict' in line:
                                lb_dirty_evict=line.split(',')[1]
                            if 'lb_mem_access' in line:
                                lb_mem_access=line.split(',')[1]
                            if 'rb_mem_access' in line:
                                rb_mem_access=line.split(',')[1]
                            if 'NF_app_mem_access' in line:
                                NF_app_mem_access=line.split(',')[1]
                            if 'memhog_app_mem_access' in line:
                                memhog_app_mem_access=line.split(',')[1]







                            line=f2.readline()
                        f2.close()
                        f1.write(app_dirty_evict+','+rb_dirty_evict+','+lb_dirty_evict+','+NF_app_mem_access+','+memhog_app_mem_access+','+rb_mem_access+','+lb_mem_access+',\n')
                        #os.chdir(target_path)
                    else:
                        print('target path does not exits\n')
                        f1.write(ps+'pack_'+rbc+'recv_'+mc+'_'+ds+'ways_'+cs+',')
                        f1.write(app_dirty_evict+','+rb_dirty_evict+','+lb_dirty_evict+','+NF_app_mem_access+','+memhog_app_mem_access+','+rb_mem_access+','+lb_mem_access+',\n')
                        #f1.write(max_ir+','+mbw+','+avg_st+','+avg_e2e+','+e2e_90+','+nic_rb_mr+','+nic_lb_mr+','+ddio_ways_mr+','+non_ddio_ways_mr+','+wr_lat_avg+','+rd_lat_avg+','+mh_ipcs+','+mh_lcpc+','+mh_cCycle_ratio+',\n')


f1.close()

