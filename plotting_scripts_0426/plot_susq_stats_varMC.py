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
#rb_counts = [2048,1024,512]
#mcs = ['6','3','2','ideal']
mcs = ['8','4']
#mcs = ['4']
#batchsizes=['32']
#ddio_setups=['2','4','11','clean','cleans','clean11','cleans11']
#q_depths =['50','150','200','250','300','350','400']
q_depths =['50','150','250','350','450']
#q_depths =['450']
#ddio_setups=['2','11','cleans','cleans11','mem']
#ddio_setups=['2','12','mem','clean','clean12']
ddio_setups=['2','12','clean','clean12']


#pslen=len(packet_sizes)
#rblen=len(rb_counts)
mclen=len(mcs)
qdlen = len(q_depths)
ddioslen=len(ddio_setups)

#toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]
toparr = [[[[] for l in range(ddioslen)] for k in range(qdlen)] for j in range(mclen)]

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
field_names.append('maxIR') ## raw data given by interval, need to convert
field_names.append('NIC_RB_Miss_Rate')
field_names.append('Core_RB_Miss_Rate')
field_names.append('MBW')
#field_names.append('Memhog_ipcs')

color_list= [[['black'] for l in range(ddioslen)] for k in range(mclen)]
color_list[getindex('8',mcs)][getindex('2',ddio_setups)]='navy'
color_list[getindex('8',mcs)][getindex('12',ddio_setups)]='blue'
#color_list[getindex('8',mcs)][getindex('mem',ddio_setups)]='slateblue'
color_list[getindex('8',mcs)][getindex('clean',ddio_setups)]='aqua'
color_list[getindex('8',mcs)][getindex('clean12',ddio_setups)]='lightcyan'

color_list[getindex('4',mcs)][getindex('2',ddio_setups)]='darkgoldenrod'
color_list[getindex('4',mcs)][getindex('12',ddio_setups)]='gold'
#color_list[getindex('4',mcs)][getindex('mem',ddio_setups)]='orange'
color_list[getindex('4',mcs)][getindex('clean',ddio_setups)]='yellow'
color_list[getindex('4',mcs)][getindex('clean12',ddio_setups)]='lemonchiffon'

#color_list[getindex('2',mcs)][getindex('2',ddio_setups)]='darkred'
#color_list[getindex('2',mcs)][getindex('12',ddio_setups)]='red'
##color_list[getindex('2',mcs)][getindex('mem',ddio_setups)]='violet'
#color_list[getindex('2',mcs)][getindex('clean',ddio_setups)]='deeppink'
#color_list[getindex('2',mcs)][getindex('clean12',ddio_setups)]='pink'

#color_list= [['black'] for l in range(ddioslen)]
#color_list[getindex('2',ddio_setups)]='red'
#color_list[getindex('11',ddio_setups)]='blue'
#color_list[getindex('cleans',ddio_setups)]='green'
#color_list[getindex('cleans11',ddio_setups)]='lightcyan'
#color_list[getindex('mem',ddio_setups)]='purple'




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
        mc=su[4]
        #print(mc)
        ##### get indexes in array
        qdi = getindex(qd,q_depths)
        dsi= getindex(ds, ddio_setups)
        mci= getindex(mc, mcs)

        validSetup=True
        if qdi==-1:
            line=f.readline();
            continue
        if dsi==-1:
            line=f.readline();
            continue
        if mci==-1:
            line=f.readline();
            continue


        interval_to_IR = 2.5*1024*8 #divide this by interval
        ir_in_Gbps=interval_to_IR / (float(tmp[1]))

        if (len(toparr[mci][qdi][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])
        
        toparr[mci][qdi][dsi].append(ir_in_Gbps)      ##0 IR
        toparr[mci][qdi][dsi].append(float(tmp[2]))   ##1 NIC_RB_MR
        toparr[mci][qdi][dsi].append(float(tmp[3]))   ##2 CORE_RB_MR
        toparr[mci][qdi][dsi].append(float(tmp[4]))   ##3 MBW

        line=f.readline();

    print('toparr populated')
    ###dbg
    qdi = getindex('50',q_depths)
    dsi= getindex('2', ddio_setups)
    mci= getindex('2', mcs)
    #print(str(toparr[mci][qdi][dsi][0]))

    os.system('mkdir '+outdir)
    os.chdir(outdir)

    xtick_labels=[]
    for l in range(qdlen):
        core_MR=str(int(toparr[0][l][0][2] * 100)) # leakyDMA rate with 2way DDIO
        xtick_labels.append('depth_'+str(q_depths[l])+'_('+core_MR+'%)')


    for i in range(len(field_names)):
        qdlen=len(q_depths)
        ddioslen=len(ddio_setups)

        #tmparr = [[[] for l in range(ddioslen)] for k in range(qdlen)]
        #tmparr = [[] for l in range(ddioslen)]
        tmparr = [[[] for l in range(ddioslen)] for k in range(mclen)]
    
        for l in range(mclen):
            for j in range(len(q_depths)):
                for k in range(len(ddio_setups)):
                    #print(str(l)+','+str(j)+','+str(k))
                    #tmparr[l][k].append(toparr[j][k][i])
                    if(len(toparr[l][j][k])!=0):
                        tmparr[l][k].append(toparr[l][j][k][i])
                    else:
                        tmparr[l][k].append(0)
                    #tmparr[l][k].append(1)

        
        ifig,iax=plt.subplots()
        iax.set_title(field_names[i])
        X_axis = np.arange(qdlen)

        barwidth = 0.075
        ### just plot one ideal mc

        #for j in range(1,len(mcs)):
        #    for k in range(len(ddio_setups)):
        for j in (range(mclen)):
            for k in range(len(ddio_setups)):

                xoffset = barwidth*(k+(j*ddioslen))
                iax.bar(X_axis-0.2+(xoffset), tmparr[j][k],edgecolor='black', alpha=0.6, color=color_list[j][k], label=str(ddio_setups[k])+"ways_"+str(mcs[j])+"_mc", width=barwidth)

        plt.xticks(X_axis, xtick_labels)
        #iax.legend(ncol=1)
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
    
