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
#parser.add_argument('--infile', type=str, default='mbd_stats.csv')  
parser.add_argument('--infile', type=str, default='0420_l3fwd_alone_mem_breakdown.csv')  
parser.add_argument('--outdir', type=str, default='mbd_plots')  
parser.add_argument('--nocl', type=bool, default=False)
args = parser.parse_args()
infile = args.infile
outdir = args.outdir
nocl = args.nocl



#packet_sizes = [1024, 512]
#mcs = ['6','3','2','ideal']
#mcs = ['ideal','6','3','2']
#batchsizes=['32']
#ddio_setups=['2','4','11','clean','cleans','clean11','cleans11']
#q_depths =['50','150','250','350','450']
#q_depths =['50','250','450']
#base_miss_perc =[' (1%)',' (15%)',' (36%)']
#ddio_setups=['2','11','cleans','cleans11','mem']
#ddio_setups=['2','6','12','clean2','clean6','clean12','ideal']


rb_counts = [512,1024,2048]
ddio_setups=['nocl','clean']
partitions=['2','6','12','ideal']

num_packets=500000


#pslen=len(packet_sizes)
#rblen=len(rb_counts)
#mclen=len(mcs)

rblen=len(rb_counts)
ddioslen=len(ddio_setups)
ptlen=len(partitions)

#toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]
toparr = [[[[] for l in range(ddioslen)] for k in range(ptlen)] for j in range(rblen)]


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
    #exit
    return -1

field_names=[]

field_names.append('NF_app_dirty_evct')
field_names.append('rb_dirty_evct')
field_names.append('lb_dirty_evct')
field_names.append('NF_app_access')
field_names.append('rb_access')
field_names.append('lb_access')

#field_names.append('Memhog_access')



color_list=['black' for l in range(len(field_names))]
color_list[getindex('NF_app_dirty_evct',field_names    )] ='navy'
color_list[getindex('rb_dirty_evct' ,field_names    )]  ='purple'
color_list[getindex('NF_app_access' ,field_names    )]  ='yellow'
color_list[getindex('rb_access'     ,field_names    )]  ='green'
color_list[getindex('lb_access'     ,field_names    )]  ='red'
color_list[getindex('lb_dirty_evct' ,field_names    )]  ='aqua'
#color_list[getindex('Memhog_access' ,field_names    )]  ='orange'


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


        ##qd=su[1]
        ##ds=su[3]
        ####### get indexes in array
        ##dsi= getindex(ds, ddio_setups)

        if rbci==-1:
            line=f.readline();
            continue
        if dsi==-1:
            line=f.readline();
            continue
        if pti==-1:
            line=f.readline();
            continue


        if (len(toparr[rbci][pti][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])


        toparr[rbci][pti][dsi].append((float(tmp[1]))/num_packets)   ##0 app_dirty_ev
        toparr[rbci][pti][dsi].append(float(tmp[2])/num_packets)   ##1 rb_dirty_ev
        toparr[rbci][pti][dsi].append(float(tmp[3])/num_packets)   ##2 lb_dirty_ev
        toparr[rbci][pti][dsi].append((float(tmp[4]))/num_packets)   ##3 NF_app_access
        toparr[rbci][pti][dsi].append(float(tmp[6])/num_packets)   ##4 rb_access
        toparr[rbci][pti][dsi].append(float(tmp[7])/num_packets)   ##5 lb_access
        #### repositioning memhog to be at the end
        #### didn't run with memhog for susq




        line=f.readline();

    print('toparr populated')

    os.system('mkdir '+outdir)
    os.chdir(outdir)
    matplotlib.rcParams.update({'font.size': 20})

    xtick_labels=[]
    for dsi in range(ddioslen):
        for pti in range(ptlen):
            xtick_labels.append(str(partitions[pti]+'_'+str(ddio_setups[dsi])))


    ifig,iax=plt.subplots(1,rblen)
    X_axis = np.arange(ddioslen*ptlen)
    
    #print(str(toparr[0][2][1]))
    for rbi in range(rblen):
        tmparr = [[]for l in range(len(field_names))]
        for dsi in range(ddioslen):
            for pti in range(ptlen):
                for j in range(len(field_names)):
                    #print(str(rbi)+', '+str(pti)+', '+str(j))
                    tmparr[j].append(toparr[rbi][pti][dsi][j])


        #ifig,iax=plt.subplots()
        #X_axis = np.arange(ddioslen)

        barwidth = 0.8
        iax[rbi].bar(X_axis, tmparr[0], edgecolor='black',alpha=0.6,color=color_list[0], label=field_names[0], width=barwidth)
        #iax.bar(X_axis, tmparr[0], edgecolor='black',alpha=0.8,color=color_list[0], label=field_names[0], width=barwidth)
        botarr = tmparr[0];
        for j in range(1,len(field_names)):
            iax[rbi].bar(X_axis, tmparr[j], bottom=botarr, edgecolor='black',alpha=0.7,color=color_list[j], label=field_names[j], width=barwidth)
            for k in range(len(botarr)):
                botarr[k]=botarr[k]+tmparr[j][k]

        iax[rbi].set_title(str(rb_counts[rbi])+'_recv_bufs')
        #plt.xticks(X_axis, xtick_labels)
        #iax.legend(ncol=2)
        #plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
        ifig.set_size_inches(10,4)
        #plt.subplots_adjust(bottom=0.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)
        #ifig.tight_layout()
    for ax in iax.flat:
        #ax.set(xlabel='x-label', ylabel='Accesses per request')
        ax.set(ylabel='Accesses per request')
        #ax.label_outer()
    for ax in iax.flat:
        ax.label_outer()
        ax.set_xticks(X_axis)
        ax.set_xticklabels(xtick_labels)
        plt.setp(ax.get_xticklabels(), rotation=70, horizontalalignment='right')


    iax[1].legend(ncol=3,bbox_to_anchor=(0.5,1.3), loc='center')
    iax[1].set(xlabel='DDIO WAYS')
    #iax[1].set_xticks(X_axis)
    #iax[1].set_xticklabels(xtick_labels)
    print(xtick_labels)
    #plt.xticks(range(4),['2','6','12','infinite'])
    iax[1].sharex(iax[0])
    iax[2].sharex(iax[0])
    #plt.ylabel('MEM Accesses per request')
    #plt.xlabel('DDIO Setup')
    ifig.savefig('MEM Access Breakdown.png', bbox_inches='tight')
    #ifig.savefig('q_depth_'+str(q_depths[rbi])+base_miss_perc[rbi]+'.png', bbox_inches='tight')
        #iax[rbi].set_title('q_depth: '+str(q_depths[rbi])+base_miss_perc[rbi])





exit
    
