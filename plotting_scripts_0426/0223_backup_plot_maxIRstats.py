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


setups_6con = []
setups_2con = []
setups_1con = []
setups_simp = []
max_ir_6con = []
max_ir_2con = []
max_ir_1con = []
max_ir_simp = []

setups=[]
setups.append(setups_6con)
setups.append(setups_2con)
setups.append(setups_1con)
setups.append(setups_simp)
max_ir=[]
max_ir.append(max_ir_6con)
max_ir.append(max_ir_2con)
max_ir.append(max_ir_1con)
max_ir.append(max_ir_simp)

mbw_6con=[]
mbw_2con=[]
mbw_1con=[]
mbw_simp=[]
mbw = []
mbw.append(mbw_6con)
mbw.append(mbw_2con)
mbw.append(mbw_1con)
mbw.append(mbw_simp)

avg_st_6con=[]
avg_st_2con=[]
avg_st_1con=[]
avg_st_simp=[]
avg_st = []
avg_st.append(avg_st_6con)
avg_st.append(avg_st_2con)
avg_st.append(avg_st_1con)
avg_st.append(avg_st_simp)

avg_e2e =[]
e2e_90=[]

nic_rb_mr_6con=[]
nic_rb_mr_2con=[]
nic_rb_mr_1con=[]
nic_rb_mr_simp=[]
nic_rb_mr=[]
nic_rb_mr.append(nic_rb_mr_6con)
nic_rb_mr.append(nic_rb_mr_2con)
nic_rb_mr.append(nic_rb_mr_1con)
nic_rb_mr.append(nic_rb_mr_simp)


wr_lat_6mc=[]
wr_lat_2mc=[]
wr_lat_1mc=[]
wr_lat_simp=[]
wr_lat=[]
wr_lat.append(wr_lat_6mc)
wr_lat.append(wr_lat_2mc)
wr_lat.append(wr_lat_1mc)
wr_lat.append(wr_lat_simp)

rd_lat_6mc=[]
rd_lat_2mc=[]
rd_lat_1mc=[]
rd_lat_simp=[]
rd_lat=[]
rd_lat.append(rd_lat_6mc)
rd_lat.append(rd_lat_2mc)
rd_lat.append(rd_lat_1mc)
rd_lat.append(rd_lat_simp)




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
        wrlat_in_ns = float(tmp[10])*0.4
        rdlat_in_ns = float(tmp[11])*0.4
        if '6con' in cons:
            setups_6con.append(su)
            #max_ir_6con.append(float(tmp[1]))
            max_ir_6con.append(ir_in_Gbps)
            mbw_6con.append(float(tmp[2]))
            #avg_st_6con.append(float(tmp[3]))
            avg_st_6con.append(st_in_ns)
            nic_rb_mr_6con.append(float(tmp[6]))
            #wr_lat_6mc.append(float(tmp[10]))
            #rd_lat_6mc.append(float(tmp[11]))
            wr_lat_6mc.append(wrlat_in_ns)
            rd_lat_6mc.append(rdlat_in_ns)

        if '2con' in cons:
            setups_2con.append(su)
            #max_ir_2con.append(float(tmp[1]))
            max_ir_2con.append(ir_in_Gbps)
            mbw_2con.append(float(tmp[2]))
            #avg_st_2con.append(float(tmp[3]))
            avg_st_2con.append(st_in_ns)
            nic_rb_mr_2con.append(float(tmp[6]))
            #wr_lat_2mc.append(float(tmp[10]))
            #rd_lat_2mc.append(float(tmp[11]))
            wr_lat_2mc.append(wrlat_in_ns)
            rd_lat_2mc.append(rdlat_in_ns)


        if '1con' in cons:
            setups_1con.append(su)
            #max_ir_1con.append(float(tmp[1]))
            max_ir_1con.append(ir_in_Gbps)
            mbw_1con.append(float(tmp[2]))
            #avg_st_1con.append(float(tmp[3]))
            avg_st_1con.append(st_in_ns)
            nic_rb_mr_1con.append(float(tmp[6]))
            #wr_lat_1mc.append(float(tmp[10]))
            #rd_lat_1mc.append(float(tmp[11]))
            wr_lat_1mc.append(wrlat_in_ns)
            rd_lat_1mc.append(rdlat_in_ns)



        if 'simp' in cons:
            setups_simp.append(su)
            #max_ir_simp.append(float(tmp[1]))
            max_ir_simp.append(ir_in_Gbps)
            mbw_simp.append(float(tmp[2]))
            #avg_st_simp.append(float(tmp[3]))
            avg_st_simp.append(st_in_ns)
            nic_rb_mr_simp.append(float(tmp[6]))
            wr_lat_simp.append(float(tmp[10])) #these two will be 0 for simp
            rd_lat_simp.append(float(tmp[11]))



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
    for i in {1,2,3,6,10 ,11}:
        ifig,iax=plt.subplots()
        
        iax.set_title(field_names[i])
        X_axis=np.arange(len(setups[0])) 
        iax.bar(X_axis-0.15, arrptr[i-1][3],edgecolor='black', alpha=0.5, color="black", label='simp', width=0.1)
        iax.bar(X_axis-0.05, arrptr[i-1][0],edgecolor='black', alpha=0.5, color="blue", label='6mc: 920Gbps', width=0.1)
        iax.bar(X_axis+0.05, arrptr[i-1][1],edgecolor='black', alpha=0.5, color="green", label='2mc: 307Gbps', width=0.1)
        iax.bar(X_axis+0.15, arrptr[i-1][2],edgecolor='black', alpha=0.5, color="red", label='1mc: 154Gbps', width=0.1)
        plt.xticks(X_axis,setups[0])
        plt.legend()
        plt.setp(iax.get_xticklabels(), rotation=30, horizontalalignment='right')
        ifig.set_size_inches(8,3)
        plt.subplots_adjust(bottom=0.3)
        #figure(figsize=(50, 50), dpi=720)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

        if(i==1):
            plt.ylabel('max nic arrival rate(Gbps)')
        if(i==2):
            plt.ylabel('avg memory BW consumption\n per controller(GBps)')
        if(i==3):
            plt.ylabel('avg service time(ns)')
        if(i==10):
            plt.ylabel('avg wr_lat (ns)')
        if(i==11):
            plt.ylabel('avg rd_lat (ns)')


        ifig.savefig(field_names[i]+'.png')

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


