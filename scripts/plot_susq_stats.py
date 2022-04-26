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


parser = argparse.ArgumentParser()
parser.add_argument('--infile', type=str, default='leakyDMA_stats.csv')  
parser.add_argument('--outdir', type=str, default='leakyDMA_plots')  
args = parser.parse_args()
infile = args.infile
outdir = args.outdir




#packet_sizes = [1024, 512]
packet_sizes = [1024]
#rb_counts = [2048,1024,512]
#mcs = ['6','3','2','ideal']
#mcs = ['ideal','6','3','2']
#batchsizes=['32']
#ddio_setups=['2','4','11','clean','cleans','clean11','cleans11']
#q_depths =['50','150','200','250','300','350','400']
q_depths =['50','150','250','350','450']
#ddio_setups=['2','11','cleans','cleans11','mem']
ddio_setups=['2','12','clean','clean12']


#pslen=len(packet_sizes)
#rblen=len(rb_counts)
#mclen=len(mcs)
qdlen = len(q_depths)
ddioslen=len(ddio_setups)

#toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]
toparr = [[[] for l in range(ddioslen)] for k in range(qdlen)]

#### sanity check prints
##print(str(len(toparr)))
##print(str(len(toparr[0])))
##
##toparr[0][0][0][0].append(0.1234)
##toparr[0][0][0][0].append(0.1234)
##toparr[0][0][0][1].append(0.2)
##toparr[1][1][1][1].append(0.9876)
##print(toparr[0][0][0][0])
##print(toparr[1][1][1][1])

def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

field_names=[]
field_names.append('IR') ## raw data given by interval, need to convert
field_names.append('NIC_RB_Miss_Rate')
field_names.append('Core_RB_Miss_Rate')
field_names.append('MBW')
#field_names.append('Memhog_ipcs')

#color_list= [[['black'] for l in range(ddioslen)] for k in range(mclen)]
#color_list[getindex('6',mcs)][getindex('2',ddio_setups)]='navy'
##color_list[getindex('6',mcs)][getindex('4',ddio_setups)]='mediumblue'
#color_list[getindex('6',mcs)][getindex('11',ddio_setups)]='blue'
##color_list[getindex('6',mcs)][getindex('clean',ddio_setups)]='royalblue'
#color_list[getindex('6',mcs)][getindex('cleans',ddio_setups)]='aqua'
##color_list[getindex('6',mcs)][getindex('clean11',ddio_setups)]='aqua'
#color_list[getindex('6',mcs)][getindex('cleans11',ddio_setups)]='lightcyan'
#
#color_list[getindex('3',mcs)][getindex('2',ddio_setups)]='darkgoldenrod'
##color_list[getindex('3',mcs)][getindex('4',ddio_setups)]='orange'
#color_list[getindex('3',mcs)][getindex('11',ddio_setups)]='gold'
##color_list[getindex('3',mcs)][getindex('clean',ddio_setups)]='khaki'
#color_list[getindex('3',mcs)][getindex('cleans',ddio_setups)]='yellow'
##color_list[getindex('3',mcs)][getindex('clean11',ddio_setups)]='ivory'
#color_list[getindex('3',mcs)][getindex('cleans11',ddio_setups)]='lemonchiffon'
#
#color_list[getindex('2',mcs)][getindex('2',ddio_setups)]='darkred'
#color_list[getindex('2',mcs)][getindex('11',ddio_setups)]='red'
#color_list[getindex('2',mcs)][getindex('cleans',ddio_setups)]='deeppink'
#color_list[getindex('2',mcs)][getindex('cleans11',ddio_setups)]='pink'

color_list= [['black'] for l in range(ddioslen)]
color_list[getindex('2',ddio_setups)]='red'
color_list[getindex('12',ddio_setups)]='blue'
color_list[getindex('clean',ddio_setups)]='green'
color_list[getindex('clean12',ddio_setups)]='lightcyan'
#color_list[getindex('mem',ddio_setups)]='purple'



xtick_labels=[]
for l in range(qdlen):
    xtick_labels.append('depth_'+str(q_depths[l]))


if infile in os.listdir('.'):
    f=open(infile,'r')
    line=f.readline();
    ##field_names=line.split(',')
    ##print(str(len(field_names)))
    ##field_names.remove('\n')
    ##print(str(len(field_names)))
    line=f.readline();
    while line:
        tmp=line.split(',')
        #### parse setup
        #su=tmp[0]
        #tmp[0]=tmp[0].replace('pack','')
        #tmp[0]=tmp[0].replace('recv','')
        su = tmp[0].split('_')
        qd=su[1]
        ds=su[3]
        ##### get indexes in array
        qdi = getindex(qd,q_depths)
        dsi= getindex(ds, ddio_setups)

        validSetup=True
        if qdi==-1:
            line=f.readline();
            continue
        if dsi==-1:
            line=f.readline();
            continue

        psi=0
        numpackets_multiplier = 2500000 * 8 / 1000000000#transslate to Gbps
        ir_in_Gbps=float(tmp[1]) * packet_sizes[psi] * numpackets_multiplier
        st_in_ns = float(tmp[3])*0.4
        #wrlat_in_ns = float(tmp[10])*0.4
        #rdlat_in_ns = float(tmp[11])*0.4

        if (len(toparr[psi][rbci][mci][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])
        
        toparr[psi][rbci][mci][dsi].append(ir_in_Gbps)      ##0 IR
        toparr[psi][rbci][mci][dsi].append(float(tmp[2]))   ##1 MBW
        toparr[psi][rbci][mci][dsi].append(st_in_ns)        ##2 ST
        toparr[psi][rbci][mci][dsi].append(float(tmp[6]))   ##3 nic_rb_mr
        toparr[psi][rbci][mci][dsi].append(float(tmp[12]))  ##4 mh_ipcs
        toparr[psi][rbci][mci][dsi].append(float(tmp[13]))  ##5 mh_lcpc
        toparr[psi][rbci][mci][dsi].append(float(tmp[14]))  ##6 mh_cCycle_ratio

        line=f.readline();

    print('toparr populated')

    ##produce one plot per packetsize_rbcount
    t_psi=0     ## 0 - 1024, 1 - 512 
    t_rbci=1    ## 0 - 2048, 1- 1024, 2 - 512


    os.system('mkdir '+outdir)
    os.chdir(outdir)

    for i in range(len(field_names)):
        pslen=len(packet_sizes)
        rblen=len(rb_counts)
        mclen=len(mcs)
        ddioslen=len(ddio_setups)

        tmparr = [[[] for l in range(ddioslen)] for k in range(mclen)]
        #tmparr = [[[] for m in range(rblen)] for l in range(pslen)]
    
        for j in range(len(mcs)):
            for k in range(len(ddio_setups)):
                for l in range(pslen):
                    for m in range(rblen):
                        tmparr[j][k].append(toparr[l][m][j][k][i])

        
        ifig,iax=plt.subplots()
        iax.set_title(field_names[i])
        X_axis = np.arange(pslen*rblen)

        barwidth = 0.05
        ### just plot one ideal mc
        iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)

        #for j in range(1,len(mcs)):
        #    for k in range(len(ddio_setups)):
        for j in reversed(range(1,len(mcs))):
            for k in reversed(range(len(ddio_setups))):
                plot_ddioslen = 2
                kk = k
                #if k==getindex('cleans',ddio_setups):
                #    kk=getindex('2',ddio_setups)
                #if k==getindex('cleans11',ddio_setups):
                #    kk=getindex('11',ddio_setups)

                xoffset = barwidth*((j*ddioslen)+kk)
                iax.bar(X_axis-0.4+(xoffset), tmparr[j][k],edgecolor='black', alpha=0.8, color=color_list[j][k], label=str(mcs[j])+'mc_'+str(ddio_setups[k])+'w', width=barwidth)

        plt.xticks(X_axis, xtick_labels)
        #iax.legend(ncol=2)
        plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
        ifig.set_size_inches(16,3)
        plt.subplots_adjust(bottom=0.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

        ####Y LABELS#####
        if 'maxIR' in field_names[i]:
            plt.ylabel('Gbps')
        if 'MBW' in field_names[i]:
            plt.ylabel('avg Memory BW per controller (GB/s)')
        if 'ST' in field_names[i]:
            plt.ylabel('avg service time (ns)')
        if 'e2e' in field_names[i]:
            plt.ylabel('avg e2e latency (ns)')




        ifig.savefig(field_names[i]+'.png')
        #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
