#!/usr/bin/env python3

import os
import sys
import csv
import math
import statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt 

import argparse


from matplotlib.pyplot import figure

#figure(figsize=(50, 50), dpi=720)

parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str, default='max_ir_stats.csv')  
parser.add_argument('--outdir', type=str, default='max_ir_plots')  
args = parser.parse_args()
infile = args.infile
outdir = args.outdir


setups_6mc = []
setups_2mc = []
setups_3mc = []
setups_simp = []
setups_ideal = []
max_ir_6mc = []
max_ir_2mc = []
max_ir_3mc = []
max_ir_simp = []
max_ir_ideal = []


setups=[]
setups.append(setups_6mc)
setups.append(setups_3mc)
setups.append(setups_2mc)
setups.append(setups_simp)
setups.append(setups_ideal)
max_ir=[]
max_ir.append(max_ir_6mc)
max_ir.append(max_ir_3mc)
max_ir.append(max_ir_2mc)
max_ir.append(max_ir_simp)
max_ir.append(max_ir_ideal)

mbw_6mc=[]
mbw_2mc=[]
mbw_3mc=[]
mbw_simp=[]
mbw_ideal=[]
mbw = []
mbw.append(mbw_6mc)
mbw.append(mbw_3mc)
mbw.append(mbw_2mc)
mbw.append(mbw_simp)
mbw.append(mbw_ideal)

avg_st_6mc=[]
avg_st_2mc=[]
avg_st_3mc=[]
avg_st_simp=[]
avg_st_ideal=[]
avg_st = []
avg_st.append(avg_st_6mc)
avg_st.append(avg_st_3mc)
avg_st.append(avg_st_2mc)
avg_st.append(avg_st_simp)
avg_st.append(avg_st_ideal)

avg_e2e_6mc=[]
avg_e2e_3mc=[]
avg_e2e_2mc=[]
avg_e2e_simp=[]
avg_e2e_ideal=[]

avg_e2e =[]
avg_e2e.append(avg_e2e_6mc)
avg_e2e.append(avg_e2e_3mc)
avg_e2e.append(avg_e2e_2mc)
avg_e2e.append(avg_e2e_simp)
avg_e2e.append(avg_e2e_ideal)


e2e_90=[]

nic_rb_mr_6mc=[]
nic_rb_mr_2mc=[]
nic_rb_mr_3mc=[]
nic_rb_mr_simp=[]
nic_rb_mr_ideal=[]
nic_rb_mr=[]
nic_rb_mr.append(nic_rb_mr_6mc)
nic_rb_mr.append(nic_rb_mr_3mc)
nic_rb_mr.append(nic_rb_mr_2mc)
nic_rb_mr.append(nic_rb_mr_simp)
nic_rb_mr.append(nic_rb_mr_ideal)


wr_lat_6mc=[]
wr_lat_2mc=[]
wr_lat_3mc=[]
wr_lat_simp=[]
wr_lat_ideal=[]
wr_lat=[]
wr_lat.append(wr_lat_6mc)
wr_lat.append(wr_lat_3mc)
wr_lat.append(wr_lat_2mc)
wr_lat.append(wr_lat_simp)
wr_lat.append(wr_lat_ideal)

rd_lat_6mc=[]
rd_lat_2mc=[]
rd_lat_3mc=[]
rd_lat_simp=[]
rd_lat_ideal=[]
rd_lat=[]
rd_lat.append(rd_lat_6mc)
rd_lat.append(rd_lat_3mc)
rd_lat.append(rd_lat_2mc)
rd_lat.append(rd_lat_simp)
rd_lat.append(rd_lat_ideal)




nic_lb_mr=[]
ddio_ways_mr=[]
non_ddio_ways_mr=[]





#field_names=[]

if infile in os.listdir('.'):
    f=open(infile,'r')
    line=f.readline();
    field_names=line.split(',')
    print(str(len(field_names)))
    field_names.remove('\n')
    print(str(len(field_names)))
    line=f.readline();
    while line:
        tmp=line.split(',')
        cons = tmp[0].split('v_')[1]
        su = tmp[0].split('v_')[0]
        su=su.replace('pack','p')
        su=su.replace('rec','rb')
        numpackets_multiplier = 2500000 * 8 / 1000000000#transslate to Gbps
        psize=512;
        if '1024p' in su:
            psize=1024
        elif '512p' in su:
            psize=512
        else:
            print('unexpected packet size: '+su);

        ir_in_Gbps=float(tmp[1]) * psize * numpackets_multiplier
        st_in_ns = float(tmp[3])*0.4
        avg_e2e_in_ns =float(tmp[4])*0.4
        wrlat_in_ns = float(tmp[10])*0.4
        rdlat_in_ns = float(tmp[11])*0.4
        if '6' in cons:
            setups_6mc.append(su)
            #max_ir_6mc.append(float(tmp[1]))
            max_ir_6mc.append(ir_in_Gbps)
            mbw_6mc.append(float(tmp[2]))
            #avg_st_6mc.append(float(tmp[3]))
            avg_st_6mc.append(st_in_ns)
            avg_e2e_6mc.append(avg_e2e_in_ns)
            nic_rb_mr_6mc.append(float(tmp[6]))
            #wr_lat_6mc.append(float(tmp[10]))
            #rd_lat_6mc.append(float(tmp[11]))
            wr_lat_6mc.append(wrlat_in_ns)
            rd_lat_6mc.append(rdlat_in_ns)

        if '2' in cons:
            setups_2mc.append(su)
            #max_ir_2mc.append(float(tmp[1]))
            max_ir_2mc.append(ir_in_Gbps)
            mbw_2mc.append(float(tmp[2]))
            #avg_st_2mc.append(float(tmp[3]))
            avg_st_2mc.append(st_in_ns)
            avg_e2e_2mc.append(avg_e2e_in_ns)
            nic_rb_mr_2mc.append(float(tmp[6]))
            #wr_lat_2mc.append(float(tmp[10]))
            #rd_lat_2mc.append(float(tmp[11]))
            wr_lat_2mc.append(wrlat_in_ns)
            rd_lat_2mc.append(rdlat_in_ns)


        if '3' in cons:
            setups_3mc.append(su)
            #max_ir_3mc.append(float(tmp[1]))
            max_ir_3mc.append(ir_in_Gbps)
            mbw_3mc.append(float(tmp[2]))
            #avg_st_3mc.append(float(tmp[3]))
            avg_st_3mc.append(st_in_ns)
            avg_e2e_3mc.append(avg_e2e_in_ns)
            nic_rb_mr_3mc.append(float(tmp[6]))
            #wr_lat_3mc.append(float(tmp[10]))
            #rd_lat_3mc.append(float(tmp[11]))
            wr_lat_3mc.append(wrlat_in_ns)
            rd_lat_3mc.append(rdlat_in_ns)



        if 'simp' in cons:
            setups_simp.append(su)
            #max_ir_simp.append(float(tmp[1]))
            max_ir_simp.append(ir_in_Gbps)
            mbw_simp.append(float(tmp[2]))
            #avg_st_simp.append(float(tmp[3]))
            avg_st_simp.append(st_in_ns)
            avg_e2e_simp.append(avg_e2e_in_ns)
            nic_rb_mr_simp.append(float(tmp[6]))
            wr_lat_simp.append(float(tmp[10])) #these two will be 0 for simp
            rd_lat_simp.append(float(tmp[11]))

        if 'ideal' in cons:
            setups_ideal.append(su)
            #max_ir_ideal.append(float(tmp[1]))
            max_ir_ideal.append(ir_in_Gbps)
            mbw_ideal.append(float(tmp[2]))
            #avg_st_ideal.append(float(tmp[3]))
            avg_st_ideal.append(st_in_ns)
            avg_e2e_ideal.append(avg_e2e_in_ns)
            nic_rb_mr_ideal.append(float(tmp[6]))
            wr_lat_ideal.append(wrlat_in_ns) 
            rd_lat_ideal.append(rdlat_in_ns)




        ##setups.append((tmp[0]))
        ##max_ir.append(float(tmp[1]))
        #mbw.append(float(tmp[2]))
        #avg_st.append(float(tmp[3]))
        #avg_e2e.append(float(tmp[4]))
        #e2e_90.append(float(tmp[5]))
        #nic_rb_mr.append(float(tmp[6]))
        #nic_lb_mr.append(float(tmp[7]))
        #ddio_ways_mr.append(float(tmp[8]))
        #non_ddio_ways_mr.append(float(tmp[9]))
        
        line=f.readline()
                        
    f.close()

    arrptr=[]
    arrptr.append(max_ir)
    arrptr.append(mbw)
    arrptr.append(avg_st)
    arrptr.append(avg_e2e)
    arrptr.append(e2e_90)
    arrptr.append(nic_rb_mr)
    arrptr.append(nic_lb_mr)
    arrptr.append(ddio_ways_mr)
    arrptr.append(non_ddio_ways_mr)
    arrptr.append(wr_lat)
    arrptr.append(rd_lat)
    print('arrptr len: '+str(len(arrptr)))


    os.system('mkdir '+outdir)
    os.chdir(outdir)

    color_i=0;


#    for i in range(1,len(field_names)):
    #for i in range(1,2):
    #for i in {1,2,3,6,10 ,11}:
    for i in {0,1,2,3,5,9 ,10}:
        ifig,iax=plt.subplots()
        
        iax.set_title(field_names[i+1])
        X_axis=np.arange(len(setups[0])) 
        iax.bar(X_axis-0.15, arrptr[i][4],edgecolor='black', alpha=0.5, color="black", label='ideal', width=0.1)
        #iax.bar(X_axis-0.15, arrptr[i][3],edgecolor='black', alpha=0.5, color="gray", label='simp', width=0.1)
        iax.bar(X_axis-0.05, arrptr[i][0],edgecolor='black', alpha=0.5, color="blue", label='6mc: 920Gbps', width=0.1)
        iax.bar(X_axis+0.05, arrptr[i][1],edgecolor='black', alpha=0.5, color="green", label='3mc: 460Gbps', width=0.1)
        iax.bar(X_axis+0.15, arrptr[i][2],edgecolor='black', alpha=0.5, color="red", label='2mc: 307Gbps', width=0.1)
        plt.xticks(X_axis,setups[0])
        #plt.legend()
        iax.legend(ncol=2)
        if(i==1 or i==5):
            #iax.legend(ncol=1, bbox_to_anchor=(1.1, 1.1))
            iax.legend(ncol=1)
        #iax.legend(bbox_to_anchor=(1.1,1.2)) #loc='upper right'
        #iax.legend(ncol=3, fancybox=True, bbox_to_anchor=(0.7,1.2)) #loc='upper right'
        plt.setp(iax.get_xticklabels(), rotation=30, horizontalalignment='right')
        ifig.set_size_inches(8,3)
        plt.subplots_adjust(bottom=0.3)
        #figure(figsize=(50, 50), dpi=720)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

        if(i==0):
            plt.ylabel('max nic arrival rate(Gbps)')
        if(i==1):
            plt.ylabel('avg memory BW consumption\n per controller(GBps)')
        if(i==2):
            plt.ylabel('avg service time(ns)')
        if(i==3):
            plt.ylabel('avg e2e latency(ns)')
            #iax.set_ylim([0,10000])

        if(i==9):
            plt.ylabel('avg wr_lat (ns)')
        if(i==10):
            plt.ylabel('avg rd_lat (ns)')


        ifig.savefig(field_names[i+1]+'.png')

    print('exiting\n')
    exit(0)



##    for i in range(1,len(field_names)):
##        ifig,iax=plt.subplots()
##
##        iax.set_title(field_names[i])
##        
##
##        iax.bar(setups, arrptr[i-1])
##        plt.setp(iax.get_xticklabels(), rotation=30, horizontalalignment='right')
##        ifig.savefig(field_names[i]+'.png')
##
##    print('exiting\n')
##    exit(0)
##    print('dont get here plz\n')



#st_hist, bin_edges = np.histogram(cumulative_st, bins=10)

#mybins = [1000,2000,3000,4000,5000,6000]
#plt.hist(cumulative_st, bins=mybins)
#plt.savefig('st_hist.png')

#plt.scatter(x,cumulative_st,color="blue")
#plt.scatter(x,cumulative_e2e,color="black")
#plt.plot(x,cumulative_st,color="blue", linewidth=0.1)

##comment this back in when using plot
#x = np.linspace(0, len(cumulative_st), len(cumulative_st))
#plt.plot(x,cumulative_e2e,color="black", linewidth=0.1)
#plt.plot(x,cumulative_hft,color="green", linewidth=0.1)
#plt.savefig('service_times.png',dpi=720)


