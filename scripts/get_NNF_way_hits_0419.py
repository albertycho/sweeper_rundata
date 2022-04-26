#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

f_mem_lat = open('mem_lats.csv','w')
wr_lat_total=0
rd_lat_total=0
rd_count=0
wr_count=0

accesses=0

l3misses=0;

total_rb_evictions=0;


total_net_miss=0
total_net_hit=0

total_app_miss=0
total_app_hit=0
total_app_hit_put=0

total_net_miss_nic_rb=0
total_net_miss_nic_lb=0
total_net_hit_nic_rb=0
total_net_hit_nic_lb=0

total_net_miss_core_lb=0;
total_net_hit_core_lb=0;

total_net_miss_core_rb=0;
total_net_hit_core_rb=0;

net_l3_miss_ratio_core_rb=0
net_l3_miss_ratio_core_lb=0

total_app_miss_grp1=0
total_app_hit_grp1=0
total_app_hit_put_grp1=0

total_net_miss_nic_rb_grp1=0
total_net_miss_nic_lb_grp1=0
total_net_hit_nic_rb_grp1=0
total_net_hit_nic_lb_grp1=0

total_net_miss_core_lb_grp1=0;
total_net_hit_core_lb_grp1=0;

total_net_miss_core_rb_grp1=0;
total_net_hit_core_rb_grp1=0;

net_l3_miss_ratio_core_rb_grp1=0
net_l3_miss_ratio_core_lb_grp1=0


total_app_miss_NNF=0
total_app_hit_NNF=0
total_app_hit_put_NNF=0

#### mem access breakdown stats
recv_dirty_evict_total=0
lbuf_dirty_evict_total=0
app_dirty_evict_total=0
lb_mem_access=0
rb_mem_access=0



non_ddio_way_misses=0;
non_ddio_way_hits=0;
ddio_way_misses=0;
ddio_way_hits=0;

total_old_app_miss=0
total_old_app_hit=0


#sancheck counter
num_mem_con=0
num_llc_banks=0

#if exists('zsim.out'):
#    zsimout = open('zsim.out','r')
if exists('zsim_final.out'):
    zsimout = open('zsim_final.out','r')
    line = zsimout.readline()
    while line:
        if 'l3-' in line:

            while not 'array' in line:
                if 'netMiss_core_lb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    #total_net_miss += tmp2 #?
                    total_net_miss_core_lb += tmp2 
                if 'netHit_core_lb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    #total_net_miss += tmp2 #?
                    total_net_hit_core_lb += tmp2 
                if 'netMiss_core_rb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_core_rb += tmp2 
                if 'netHit_core_rb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_core_rb += tmp2 
                if 'netMiss_nic_lb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_nic_lb += tmp2
                if 'netHit_nic_lb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_nic_lb += tmp2
                if 'netMiss_nic_rb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_nic_rb += tmp2
                if 'netHit_nic_rb:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_nic_rb += tmp2
                if 'appMiss:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_miss += tmp2
                if 'appHit:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_hit += tmp2
                if 'appPutHit:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_hit_put += tmp2

                ##NF_grp1
                if 'netMiss_core_lb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_core_lb_grp1 += tmp2 
                if 'netHit_core_lb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_core_lb_grp1 += tmp2 
                if 'netMiss_core_rb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_core_rb_grp1 += tmp2 
                if 'netHit_core_rb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_core_rb_grp1 += tmp2 
                if 'netMiss_nic_lb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_nic_lb_grp1 += tmp2
                if 'netHit_nic_lb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_nic_lb_grp1 += tmp2
                if 'netMiss_nic_rb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_miss_nic_rb_grp1 += tmp2
                if 'netHit_nic_rb_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_net_hit_nic_rb_grp1 += tmp2
                if 'appMiss_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_miss_grp1 += tmp2
                if 'appHit_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_hit_grp1 += tmp2
                if 'appPutHit_grp1:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_hit_put_grp1 += tmp2

                #NNF
                if 'appMiss_NNF:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_miss_NNF += tmp2
                if 'appHit_NNF:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_hit_NNF += tmp2
                if 'appPutHit_NNF:' in line:
                    tmp1=line.split(': ')[1]
                    tmp2=int(tmp1.split(' #')[0])
                    total_app_hit_put_NNF += tmp2




                line=zsimout.readline()
                
            line=zsimout.readline()

###################################WIP

            #oldapphit/miss: temporary field for debug
            if 'oldappMiss' in line:
                tmp1=line.split(': ')[1]
                tmp2=int(tmp1.split(' #')[0])
                total_old_app_miss += tmp2
                line=zsimout.readline()

            if 'oldappHit' in line:
                tmp1=line.split(': ')[1]
                tmp2=int(tmp1.split(' #')[0])
                total_old_app_hit += tmp2
                line=zsimout.readline()

            if not 'way_inserts' in line:
                print('expected way_inserts but didnt find\n')
            line=zsimout.readline()
            while not 'way_hits' in line:
                tmp=line.split(': ')
                if (int(tmp[0]) < 9):
                    non_ddio_way_misses += int(tmp[1])
                else:
                    ddio_way_misses += int(tmp[1])
                line=zsimout.readline()
            line=zsimout.readline()
            while not 'nic_rb_way_hits' in line:
                tmp=line.split(': ')
                if (int(tmp[0]) < 9):
                    non_ddio_way_hits += int(tmp[1])
                else:
                    ddio_way_hits += int(tmp[1])
                line=zsimout.readline()



        line=zsimout.readline()

    zsimout.close()
    if(wr_count!=0):
        wr_lat_avg = wr_lat_total/wr_count
    else:
        print('no wr count logged')
        wr_lat_avg = 0
        
    if(rd_count!=0):
        rd_lat_avg = rd_lat_total/rd_count
    else:
        print('no rd count logged')
        rd_lat_avg = 0
    

##    if((total_net_hit+total_net_miss)==0):
##        net_l3_miss_ratio=0
##    else:
##        net_l3_miss_ratio = total_net_miss/(total_net_hit+total_net_miss)
    
    if((total_app_hit+total_app_miss)==0):
        app_l3_miss_ratio=0
    else:
        app_l3_miss_ratio = total_app_miss/(total_app_hit+total_app_miss)

    if( (total_net_hit_nic_rb + total_net_miss_nic_rb)==0):
        net_l3_miss_ratio_nic_rb=0
    else:
        net_l3_miss_ratio_nic_rb = total_net_miss_nic_rb / (total_net_hit_nic_rb + total_net_miss_nic_rb)


    net_l3_miss_ratio_nic_lb = 0;
    if((total_net_hit_nic_lb + total_net_miss_nic_lb)!=0):
        net_l3_miss_ratio_nic_lb = total_net_miss_nic_lb / (total_net_hit_nic_lb + total_net_miss_nic_lb)
    
   
    if((total_net_hit_core_rb + total_net_miss_core_rb)==0):
        net_l3_miss_ratio_core_rb=0
    else:
        net_l3_miss_ratio_core_rb = total_net_miss_core_rb / (total_net_hit_core_rb+ total_net_miss_core_rb)

    if((total_net_hit_core_lb + total_net_miss_core_lb)==0):
        net_l3_miss_ratio_core_lb=0
    else:
        net_l3_miss_ratio_core_lb = total_net_miss_core_lb / (total_net_hit_core_lb + total_net_miss_core_lb)


    ##NF1
    if((total_app_hit_grp1+total_app_miss_grp1)==0):
        app_l3_miss_ratio_grp1=0
    else:
        app_l3_miss_ratio_grp1 = total_app_miss_grp1/(total_app_hit_grp1+total_app_miss_grp1)

    if( (total_net_hit_nic_rb_grp1 + total_net_miss_nic_rb_grp1)==0):
        net_l3_miss_ratio_nic_rb_grp1=0
    else:
        net_l3_miss_ratio_nic_rb_grp1 = total_net_miss_nic_rb_grp1 / (total_net_hit_nic_rb_grp1 + total_net_miss_nic_rb_grp1)


    net_l3_miss_ratio_nic_lb_grp1 = 0;
    if((total_net_hit_nic_lb_grp1 + total_net_miss_nic_lb_grp1)!=0):
        net_l3_miss_ratio_nic_lb_grp1 = total_net_miss_nic_lb_grp1 / (total_net_hit_nic_lb_grp1 + total_net_miss_nic_lb_grp1)
    
   
    if((total_net_hit_core_rb_grp1 + total_net_miss_core_rb_grp1)==0):
        net_l3_miss_ratio_core_rb_grp1=0
    else:
        net_l3_miss_ratio_core_rb_grp1 = total_net_miss_core_rb_grp1 / (total_net_hit_core_rb_grp1+ total_net_miss_core_rb_grp1)

    if((total_net_hit_core_lb_grp1 + total_net_miss_core_lb_grp1)==0):
        net_l3_miss_ratio_core_lb_grp1=0
    else:
        net_l3_miss_ratio_core_lb_grp1 = total_net_miss_core_lb_grp1 / (total_net_hit_core_lb_grp1 + total_net_miss_core_lb_grp1)


    #NNF
    if((total_app_hit_NNF+total_app_miss_NNF)==0):
        app_l3_miss_ratio_NNF=0
    else:
        app_l3_miss_ratio_NNF = total_app_miss_NNF/(total_app_hit_NNF+total_app_miss_NNF)




    ######temporary fields for debug
    old_app_miss_ratio=0
    if((total_old_app_miss + total_old_app_hit)==0):
        old_app_miss_ratio=0
    else:
        old_app_miss_ratio = total_old_app_miss / (total_old_app_miss + total_old_app_hit)



    ##net_l3_miss_ratio = total_net_miss/(total_net_hit+total_net_miss)
    ##app_l3_miss_ratio = total_app_miss/(total_app_hit+total_app_miss)

    ##net_l3_miss_ratio_nic_rb = total_net_miss_nic_rb / (total_net_hit_nic_rb + total_net_miss_nic_rb)
    ##net_l3_miss_ratio_nic_lb = 0;
    ##if((total_net_hit_nic_lb + total_net_miss_nic_lb)!=0):
    ##    net_l3_miss_ratio_nic_lb = total_net_miss_nic_lb / (total_net_hit_nic_lb + total_net_miss_nic_lb)
    ##
    ##
    ##net_l3_miss_ratio_core = total_net_miss_core / (total_net_hit_core + total_net_miss_core)

    non_ddio_way_miss_rate = 0
    ddio_way_miss_Rate =0

    if((non_ddio_way_hits+non_ddio_way_misses)!=0):
        non_ddio_way_miss_rate = non_ddio_way_misses / (non_ddio_way_hits+non_ddio_way_misses)

    if((ddio_way_hits+ddio_way_misses)!=0):
        ddio_way_miss_rate = ddio_way_misses /  (ddio_way_hits+ddio_way_misses)


    f_mem_lat.write('\nMEM:\n')
    
    f_mem_lat.write('\nwr_lat_avg, '+str(wr_lat_avg)+',\n')
    f_mem_lat.write('rd_lat_avg, '+str(rd_lat_avg)+',\n')
    #f_mem_lat.write('net_l3_miss_ratio, '+str(net_l3_miss_ratio)+',\n')
    #f_mem_lat.write('net_l3_miss_count, '+str(total_net_miss)+',\n')
    #f_mem_lat.write('net_l3_hit_count, '+str(total_net_hit)+',\n')


    f_mem_lat.write('rb_dirty_evictions to mem, '+str(total_rb_evictions)+',\n')


    f_mem_lat.write('\nL3:\n')
    f_mem_lat.write('\nNF0:\n')

    f_mem_lat.write('\nnet_l3_miss_ratio_nic_rb, '+str(net_l3_miss_ratio_nic_rb)+',\n')
    f_mem_lat.write('net_l3_miss_count_nic_rb, '+str(total_net_miss_nic_rb)+',\n')
    f_mem_lat.write('net_l3_hit_count_nic_rb, '+str(total_net_hit_nic_rb)+',\n')
    f_mem_lat.write('rb_dirty_evictions to mem, '+str(total_rb_evictions)+',\n')
 
    f_mem_lat.write('\nnet_l3_miss_ratio_nic_lb, '+str(net_l3_miss_ratio_nic_lb)+',\n')
    f_mem_lat.write('net_l3_miss_count_nic_lb, '+str(total_net_miss_nic_lb)+',\n')
    f_mem_lat.write('net_l3_hit_count_nic_lb, '+str(total_net_hit_nic_lb)+',\n')
    
   
    f_mem_lat.write('\nnet_l3_miss_ratio_core_rb, '+str(net_l3_miss_ratio_core_rb)+',\n')
    f_mem_lat.write('net_l3_miss_count_core_rb, '+str(total_net_miss_core_rb)+',\n')
    f_mem_lat.write('net_l3_hit_count_core_rb, '+str(total_net_hit_core_rb)+',\n')

    f_mem_lat.write('\nnet_l3_miss_ratio_core_lb, '+str(net_l3_miss_ratio_core_lb)+',\n')
    f_mem_lat.write('net_l3_miss_count_core_lb, '+str(total_net_miss_core_lb)+',\n')
    f_mem_lat.write('net_l3_hit_count_core_lb, '+str(total_net_hit_core_lb)+',\n')
 

    f_mem_lat.write('\napp_l3_miss_ratio, '+str(app_l3_miss_ratio)+',\n')
    f_mem_lat.write('app_l3_miss, '+str(total_app_miss)+',\n')
    f_mem_lat.write('app_l3_hit , '+str(total_app_hit)+',\n')

    ####NF1
    ##f_mem_lat.write('\nNF1:\n')
    ##f_mem_lat.write('\nnet_l3_miss_ratio_nic_rb_grp1, '+str(net_l3_miss_ratio_nic_rb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_miss_count_nic_rb_grp1, '+str(total_net_miss_nic_rb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_hit_count_nic_rb_grp1, '+str(total_net_hit_nic_rb_grp1)+',\n')
 
    ##f_mem_lat.write('\nnet_l3_miss_ratio_nic_lb_grp1, '+str(net_l3_miss_ratio_nic_lb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_miss_count_nic_lb_grp1, '+str(total_net_miss_nic_lb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_hit_count_nic_lb_grp1, '+str(total_net_hit_nic_lb_grp1)+',\n')
    ##
   
    ##f_mem_lat.write('\nnet_l3_miss_ratio_core_rb_grp1, '+str(net_l3_miss_ratio_core_rb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_miss_count_core_rb_grp1, '+str(total_net_miss_core_rb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_hit_count_core_rb_grp1, '+str(total_net_hit_core_rb_grp1)+',\n')

    ##f_mem_lat.write('\nnet_l3_miss_ratio_core_lb_grp1, '+str(net_l3_miss_ratio_core_lb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_miss_count_core_lb_grp1, '+str(total_net_miss_core_lb_grp1)+',\n')
    ##f_mem_lat.write('net_l3_hit_count_core_lb_grp1, '+str(total_net_hit_core_lb_grp1)+',\n')
 

    ##f_mem_lat.write('\napp_l3_miss_ratio_grp1, '+str(app_l3_miss_ratio_grp1)+',\n')
    ##f_mem_lat.write('app_l3_miss_grp1, '+str(total_app_miss_grp1)+',\n')
    ##f_mem_lat.write('app_l3_hit_grp1 , '+str(total_app_hit_grp1)+',\n')

    #NNF
    f_mem_lat.write('\nNNF:\n')
    f_mem_lat.write('\napp_l3_miss_ratio_NNF, '+str(app_l3_miss_ratio_NNF)+',\n')
    f_mem_lat.write('app_l3_miss_NNF, '+str(total_app_miss_NNF)+',\n')
    f_mem_lat.write('app_l3_hit_NNF , '+str(total_app_hit_NNF)+',\n')





    ## rename to avoid parsing from postprocessing script
    f_mem_lat.write('\nOLD appl3_miss_ratio, '+str(old_app_miss_ratio)+',\n')
    f_mem_lat.write('OLD appl3_miss, '+str(total_old_app_miss)+',\n')
    f_mem_lat.write('OLD appl3_hit , '+str(total_old_app_hit)+',\n')
 


    
    f_mem_lat.write('\nWAYS:\n')
    f_mem_lat.write('non_ddio_ways_miss_rate , '+str(non_ddio_way_miss_rate)+',\n')
    f_mem_lat.write('ddio_ways_miss_rate , '+str(ddio_way_miss_rate)+',\n')
    
    f_mem_lat.write('l3misses ,    '+str(l3misses)+',\n')
  
    f_mem_lat.write('\nmem accesses        ,'+str(accesses)+',\n')
    f_mem_lat.write('app_dirty_evict       ,'+str(app_dirty_evict_total)+',\n')
    f_mem_lat.write('rb_dirty_evict        ,'+str(recv_dirty_evict_total)+',\n')
    f_mem_lat.write('lb_dirty_evict        ,'+str(lbuf_dirty_evict_total)+',\n')

    f_mem_lat.write('NF_app_mem_access    ,'+str(total_app_miss)+',\n')
    f_mem_lat.write('memhog_app_mem_access,'+str(total_app_miss_NNF)+',\n')
    lb_mem_access= total_net_miss_core_lb + total_net_miss_nic_lb;
    f_mem_lat.write('lb_mem_access        ,'+str(lb_mem_access)+',\n')
    f_mem_lat.write('rb_mem_access        ,'+str(total_net_miss_core_rb)+',\n')
   
 
    f_mem_lat.close()



    avg_intervals=[]
    if 'latency_hist.txt' in os.listdir('.'):
        f_lat_hist = open('latency_hist.txt','r')
        #avg_interval_line = f_lat_hist.readline()
        avg_interval_line = f_lat_hist.readline()
        while avg_interval_line:
            avg_intervals.append(avg_interval_line)
            avg_interval_line=f_lat_hist.readline()
    
            
    f_stat_summary = open('stat_summary.txt','w')
    if 'latency_hist.txt' in os.listdir('.'):
        #f_stat_summary.write(avg_interval_line)
        for avg_interval_line_out in avg_intervals:
            f_stat_summary.write(avg_interval_line_out)
        f_lat_hist.close()
    
    f_stat_summary.close()

    os.system('cat mem_lats.csv >> stat_summary.txt')

    #print('num llc banks: '+(str(num_llc_banks)))
    #print('num mem con: '+(str(num_mem_con)))

else:
    print('zsim_final.out not found\n')






#            while not 'netMiss_nic' in line:
#                line=zsimout.readline()
#            if not 'netMiss_nic_rb' in line:
#                print('expected netMiss_nic_rb but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_net_miss += tmp2
#            total_net_miss_nic_rb += tmp2
#            line=zsimout.readline()
#            if not 'netMiss_nic_lb' in line:
#                print('expected netMiss_nic_lb but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_net_miss += tmp2
#            total_net_miss_nic_lb += tmp2
#            line=zsimout.readline()
#            if not 'netMiss_core' in line:
#                print('expected netMiss_core but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_net_miss += tmp2
#            total_net_miss_core += tmp2
#            line=zsimout.readline()
#            if not 'netHit_nic_rb' in line:
#                print('expected netHit_nic_rb but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_net_hit += tmp2
#            total_net_hit_nic_rb += tmp2
#            line=zsimout.readline()
#            if not 'netHit_nic_lb' in line:
#                print('expected netHit_nic_lb but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_net_hit += tmp2
#            total_net_hit_nic_lb += tmp2
#            line=zsimout.readline()
#
#            if not 'netHit_core' in line:
#                print('expected netHit_core but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_net_hit += tmp2
#            total_net_hit_core += tmp2
#            line=zsimout.readline()
#            if not 'appMiss' in line:
#                print('expected appMiss but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_app_miss += tmp2
#            line=zsimout.readline()
#            if not 'appHit' in line:
#                print('expected apphit but didnt find\n')
#            tmp1=line.split(': ')[1]
#            tmp2=int(tmp1.split(' #')[0])
#            total_app_hit += tmp2
#            line=zsimout.readline()
###########################################################################


