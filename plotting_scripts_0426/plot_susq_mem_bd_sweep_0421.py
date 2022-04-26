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
parser.add_argument('--infile', type=str, default='mbd_stats.csv')  
parser.add_argument('--outdir', type=str, default='mbd_plots')  
parser.add_argument('--nocl', type=bool, default=False)
args = parser.parse_args()
infile = args.infile
outdir = args.outdir
nocl = args.nocl



#packet_sizes = [1024, 512]
#rb_counts = [2048,1024,512]
#mcs = ['6','3','2','ideal']
#mcs = ['ideal','6','3','2']
#batchsizes=['32']
#ddio_setups=['2','4','11','clean','cleans','clean11','cleans11']
#q_depths =['50','150','250','350','450']
#q_depths =['50','250','450']
q_depths =['250','450']
base_miss_perc =[' (1%)',' (15%)',' (36%)']
#ddio_setups=['2','11','cleans','cleans11','mem']
#ddio_setups=['2','6','12','clean2','clean6','clean12','ideal']
ddio_setups=['2','clean2','6','clean6','12','clean12','ideal']

if (nocl):
    ddio_setups=['2','6','12','ideal']


num_packets=500000


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
    #exit
    return -1

field_names=[]

#field_names.append('Other Evct')
#field_names.append('RX Evct')
#field_names.append('TX Evct')
#field_names.append('CPU Other Rd')
#field_names.append('CPU RX Rd')
#field_names.append('CPU TX Rd/Wr')

field_names.append('CPU RX Rd')
field_names.append('CPU TX Rd/Wr')
field_names.append('CPU Other Rd')
field_names.append('RX Evct')
field_names.append('TX Evct')
field_names.append('Other Evct')


#titles = ['CPU RX Rd','CPU TX Rd/Wr','CPU Other Rd','RX Evct','TX Evct','Other Evct']
#colors = ['#EDC339','#fffa90', '#4a6bc4','#c7cefa','#2A325E', '#BB979C','#481D22','#F59B8B']


#color_list=['black' for l in range(len(field_names))]
#color_list[getindex('CPU Rx Rd',field_names    )] ='navy'
#color_list[getindex('rb_dirty_evct' ,field_names    )]  ='purple'
#color_list[getindex('NF_app_access' ,field_names    )]  ='yellow'
#color_list[getindex('rb_access'     ,field_names    )]  ='green'
#color_list[getindex('lb_access'     ,field_names    )]  ='red'
#color_list[getindex('lb_dirty_evct' ,field_names    )]  ='aqua'

#titles = ['CPU RX Rd','CPU TX Rd/Wr','CPU Other Rd','RX Evct','TX Evct','Other Evct']
#color_list = ['#4a6bc4','#c7cefa','#2A325E', '#BB979C','#481D22','#F59B8B']
color_list = ['#4a6bc4','#c7cefa','#2A325E', '#BB979C','#6d031c','#F59B8B']



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


        if (len(toparr[qdi][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])

        if dsi==2:
            print('dsi==2')

        
        toparr[qdi][dsi].append(float(tmp[6])/num_packets)   ##4 rb_access
        toparr[qdi][dsi].append(float(tmp[7])/num_packets)   ##5 lb_access
        toparr[qdi][dsi].append((float(tmp[4]))/num_packets)   ##3 NF_app_access
        toparr[qdi][dsi].append(float(tmp[2])/num_packets)   ##1 rb_dirty_ev
        toparr[qdi][dsi].append(float(tmp[3])/num_packets)   ##2 lb_dirty_ev
        toparr[qdi][dsi].append((float(tmp[1]))/num_packets)   ##0 app_dirty_ev

        #toparr[qdi][dsi].append((float(tmp[1]))/num_packets)   ##0 app_dirty_ev
        #toparr[qdi][dsi].append(float(tmp[2])/num_packets)   ##1 rb_dirty_ev
        #toparr[qdi][dsi].append(float(tmp[3])/num_packets)   ##2 lb_dirty_ev
        #toparr[qdi][dsi].append((float(tmp[4]))/num_packets)   ##3 NF_app_access
        #toparr[qdi][dsi].append(float(tmp[6])/num_packets)   ##4 rb_access
        #toparr[qdi][dsi].append(float(tmp[7])/num_packets)   ##5 lb_access
        ##### repositioning memhog to be at the end
        ##### didn't run with memhog for susq
        ##toparr[qdi][dsi].append(float(tmp[5])/num_packets)   ##6 memhog_access





        line=f.readline();

    print('toparr populated')

    os.system('mkdir '+outdir)
    os.chdir(outdir)
    matplotlib.rcParams.update({'font.size': 55})

    #xtick_labels=[]
    #for dsi in range(ddioslen):
    #    xtick_labels.append(str(ddio_setups[dsi]))
    #xtick_labels=['DDIO 2 ways','+ Sweeper','DDIO 6 ways','+ Sweeper','DDIO 12 ways','+ Sweeper','Infinite DDIO']
    #if (nocl):
    #    xtick_labels=['DDIO 2 ways','DDIO 6 ways','DDIO 12 ways','Infinite DDIO']

    xtick_labels=['DDIO 2 ways  \n    + Sweeper','DDIO 6 ways  \n+ Sweeper','DDIO 12 ways  \n+ Sweeper','Ideal DDIO  \n']
    #xtick_labels=['DDIO 2 ways','DDIO 6 ways','DDIO 12 ways','Infinite DDIO\n']
    #xtick_labels2=['+ Sweeper','+ Sweeper','+ Sweeper']

    ifig,iax=plt.subplots(1,qdlen)
    X_axis = np.arange(4)
    X_axis2 = np.arange(3)
    
    #print(str(toparr[0][2][1]))
    for qdi in range(qdlen):
        tmparr = [[]for l in range(len(field_names))]
        tmparr2 = [[]for l in range(len(field_names))]
        for dsi in range(ddioslen):
            for j in range(len(field_names)):
                #print(str(qdi)+', '+str(dsi)+', '+str(j))
                if(dsi%2==0):
                    tmparr[j].append(toparr[qdi][dsi][j])
                else:
                    tmparr2[j].append(toparr[qdi][dsi][j])


        #ifig,iax=plt.subplots()
        #X_axis = np.arange(ddioslen)

        barwidth = 0.4
        iax[qdi].bar(X_axis, tmparr[0], edgecolor='black',alpha=1,color=color_list[0], label=field_names[0], width=barwidth, zorder=5)
        iax[qdi].bar(X_axis2+barwidth, tmparr2[0], edgecolor='black',alpha=1,color=color_list[0], label='', width=barwidth, zorder=5)
        #iax.bar(X_axis, tmparr[0], edgecolor='black',alpha=0.8,color=color_list[0], label=field_names[0], width=barwidth)
        botarr = tmparr[0]
        botarr2 = tmparr2[0]
        for j in range(1,len(field_names)):
            iax[qdi].bar(X_axis, tmparr[j], bottom=botarr, edgecolor='black',alpha=1,color=color_list[j], label=field_names[j], width=barwidth, zorder=5)
            iax[qdi].bar(X_axis2+barwidth, tmparr2[j], bottom=botarr2, edgecolor='black',alpha=1,color=color_list[j], label='', width=barwidth, zorder=5)
            for k in range(len(botarr)):
                botarr[k]=botarr[k]+tmparr[j][k]
            for k in range(len(botarr2)):
                botarr2[k]=botarr2[k]+tmparr2[j][k]

        iax[qdi].set_title('queued \npackets: '+str(q_depths[qdi]), fontsize=50)
        #ifig.suptitle('queued \npackets: '+str(q_depths[qdi]), fontsize=30)
        #plt.xticks(X_axis, xtick_labels)
        #iax.legend(ncol=2)
        #plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
        ifig.set_size_inches(20,15)
        #plt.subplots_adjust(bottom=0.2)
        #plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=0, axis='y')
        #ifig.tight_layout()
    for ax in iax.flat:
        #ax.set(xlabel='x-label', ylabel='Accesses per request')
        ax.set(ylabel='Memory Accesses per Request\n')
        #ax.label_outer()
    for ax in iax.flat:
        ax.label_outer()
        ax.set_xticks(X_axis+0.2)
        ax.set_xticklabels(xtick_labels, fontsize=45)
        plt.setp(ax.get_xticklabels(), rotation=50, horizontalalignment='right')
        
        dx = 0.8; dy = 0.45 
        offset = matplotlib.transforms.ScaledTranslation(dx, dy, ifig.dpi_scale_trans) 
        # apply offset transform to all x ticklabels.
        for label in ax.xaxis.get_majorticklabels():
            label.set_transform(label.get_transform() + offset)

        #offset=0.5
        #for label in ax.xaxis.get_majorticklabels():
        #    label.set_transform(label.get_transform() + offset)
        ax.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=0, axis='y')
        #plt.setp(ax,ylim=(0,30))


    handles, labels = plt.gca().get_legend_handles_labels()
    order=[0,1,2,3,4,5]
    #fig.legend([handles[i] for i in order], [labels[i] for i in order], ncol=3, loc='upper center', bbox_to_anchor(0.5,1.3) #bbox_to_anchor=(0.5,1.3), loc='center', columnspacing=0.6)
    iax[1].legend([handles[i] for i in order], [labels[i] for i in order], ncol=2, bbox_to_anchor=(1.0,1.48), columnspacing=0.6) #loc='center'
    #iax[1].legend(ncol=3,bbox_to_anchor=(0.5,1.3), loc='center', columnspacing=0.7)
    #iax[1].set(xlabel='DDIO WAYS')
    #iax[1].set_xtick_labels(xtick_labels)
    plt.xticks(range(4),['2','6','12','infinite'])
    iax[1].sharex(iax[0])
    #iax[2].sharex(iax[0])
    #plt.ylabel('MEM Accesses per request')
    #plt.xlabel('DDIO Setup')
    ifig.savefig('TLDMEMAccessBreakdown_sweep.pdf', bbox_inches='tight')
    #ifig.savefig('q_depth_'+str(q_depths[qdi])+base_miss_perc[qdi]+'.png', bbox_inches='tight')
        #iax[qdi].set_title('q_depth: '+str(q_depths[qdi])+base_miss_perc[qdi])





exit
    
