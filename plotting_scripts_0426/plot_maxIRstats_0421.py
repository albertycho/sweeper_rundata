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
parser.add_argument('--infile', type=str, default='max_ir_stats_0420_l3fwd_ALONE.csv')  
parser.add_argument('--outdir', type=str, default='max_ir_plots')  
args = parser.parse_args()
infile = args.infile
outdir = args.outdir




#packet_sizes = [1024, 512]
rb_counts = [512,1024,2048]
#mcs = ['ideal','8','4']
#mcs = ['4']
#ddio_setups=['2','12','clean','clean12']
ddio_setups=['nocl','clean']

#partitions=['2','4','6','8','10','12']
partitions=['2','6','12','ideal']

rblen=len(rb_counts)
ddioslen=len(ddio_setups)
ptlen=len(partitions)


#toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]
toparr = [[[[] for l in range(ddioslen)] for k in range(ptlen)] for j in range(rblen)]



def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

field_names=[]
field_names.append('maxIR')
field_names.append('MBW')
field_names.append('ST')
field_names.append('NIC_RB_Miss_Rate')
field_names.append('Memhog_ipcs')
field_names.append('Memhog_L3_Miss_Rate')
field_names.append('Memhog_cCycle_ratio')
field_names.append('core_rb_mr')

color_list= [[['black'] for l in range(ddioslen)] for k in range(ptlen)]

color_list[getindex('2',partitions)][getindex('clean',ddio_setups)]='blue'
color_list[getindex('6',partitions)][getindex('clean',ddio_setups)]='blue'
color_list[getindex('12',partitions)][getindex('clean',ddio_setups)]='blue'

color_list[getindex('2',partitions)][getindex('nocl',ddio_setups)]='red'
color_list[getindex('6',partitions)][getindex('nocl',ddio_setups)]='orange'
color_list[getindex('12',partitions)][getindex('nocl',ddio_setups)]='purple'



xtick_labels=[]
for l in range(rblen):
    xtick_labels.append(rb_counts[l])

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
        tmp[0]=tmp[0].replace('pack','')
        tmp[0]=tmp[0].replace('recv','')
        su = tmp[0].split('_')
        ps=su[0] #don't need
        rbc=su[1]
        mc=su[2] #don't need
        pts=su[3].replace('ways','')
        ds=su[4]
        ##### get indexes in array
        #psi=getindex(ps, packet_sizes)
        #mci = getindex(mc,mcs)
        rbci=getindex(rbc, rb_counts)
        dsi= getindex(ds, ddio_setups)
        pti= getindex(pts,partitions)

        validSetup=True
        #if psi==-1:
        #    line=f.readline();
        #    continue
        #if mci==-1:
        #    line=f.readline();
        #    continue
        if rbci==-1:
            line=f.readline();
            continue
        if dsi==-1:
            line=f.readline();
            continue
        if pti==-1:
            line=f.readline();
            continue


        packet_size=1024
        numpackets_multiplier = 3210000 * 8 / 1000000000#transslate to Gbps
        ir_in_Gbps=float(tmp[1]) * packet_size * numpackets_multiplier
        ir_in_Mrps=ir_in_Gbps*1024/(1024*8)
        
        st_in_ns = float(tmp[3])*0.4
        wrlat_in_ns = float(tmp[10])*0.4
        rdlat_in_ns = float(tmp[11])*0.4

        if (len(toparr[rbci][pti][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])
        
        toparr[rbci][pti][dsi].append(ir_in_Mrps)      ##0 IR
        toparr[rbci][pti][dsi].append(float(tmp[2])*4)   ##1 MBW
        toparr[rbci][pti][dsi].append(st_in_ns)        ##2 ST
        toparr[rbci][pti][dsi].append(float(tmp[6]))   ##3 nic_rb_mr
        toparr[rbci][pti][dsi].append(float(tmp[12]))  ##4 mh_ipcs
        toparr[rbci][pti][dsi].append(float(tmp[13]))  ##5 mh_l3_mr
        toparr[rbci][pti][dsi].append(float(tmp[14]))  ##6 mh_cCycle_ratio
        toparr[rbci][pti][dsi].append(float(tmp[15]))  ##7 core_rb_mr

        line=f.readline();

    print('toparr populated')

    ##produce one plot per packetsize_rbcount
    t_psi=0     ## 0 - 1024, 1 - 512 
    t_rbci=1    ## 0 - 2048, 1- 1024, 2 - 512


    #os.system('mkdir '+outdir)
    #os.chdir(outdir)
    matplotlib.rcParams.update({'font.size': 20})
    for i in range(len(field_names)):
    #for i in range(2):

        tmparr = [[[] for l in range(ddioslen)] for j in range(ptlen)]
        #tmparr = [[[] for m in range(rblen)] for l in range(pslen)]
        for l in range(rblen):
            for j in range(len(partitions)):
                for k in range(len(ddio_setups)):
                        #print(str(l)+str(j)+str(k))
                        tmparr[j][k].append(toparr[l][j][k][i])

        
        ifig,iax=plt.subplots()
        #iax.set_title(field_names[i])
        #X_axis = np.arange(pslen*rblen)
        X_axis = np.arange(rblen)

        barwidth = 0.2
        ### just plot one ideal mc
        #iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)

        #for j in range(1,len(mcs)):
        #    for k in range(len(ddio_setups)):
        for j in range(ptlen):
            if i==0:
                for k in reversed(range(len(ddio_setups))):
                    alval=0.7
                    if 'nocl' in ddio_setups[k]:
                        alval=1
                    if (not (('nocl' in ddio_setups[k]) and ('ideal' in partitions[j]))): # plot just one ideal

                        xoffset = barwidth*(j)
                        iax.bar(X_axis-0.2+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, color=color_list[j][k], label=str(partitions[j]), width=barwidth)

            else:
                for k in (range(len(ddio_setups))):
                    alval=0
                    if 'nocl' in ddio_setups[k]:
                        alval=1
                    if (not (('nocl' in ddio_setups[k]) and ('ideal' in partitions[j]))): # plot just one ideal

                        xoffset = barwidth*(j)
                        iax.bar(X_axis-0.2+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, color=color_list[j][k], label=str(partitions[j]), width=barwidth)


        #iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)
        plt.xticks(X_axis, xtick_labels)
        #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upper left')
        iax.legend(ncol=4,bbox_to_anchor=[0.5,1.2], loc='center')

        plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
        ifig.set_size_inches(10,4)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

        ####Y LABELS#####
        if 'maxIR' in field_names[i]:
            plt.ylabel('L3fwd Throughput (Mrps)')
        if 'MBW' in field_names[i]:
            plt.ylabel('avg Memory BW per controller (GB/s)')
        if 'ST' in field_names[i]:
            plt.ylabel('avg service time (ns)')
        if 'e2e' in field_names[i]:
            plt.ylabel('avg e2e latency (ns)')




        ifig.savefig(field_names[i]+'.png', bbox_inches='tight')
        #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
