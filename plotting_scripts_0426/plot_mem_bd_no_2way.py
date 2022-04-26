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
parser.add_argument('--infile', type=str, default='mem_breakdown.csv')  
parser.add_argument('--outdir', type=str, default='mem_bd_plots')  
args = parser.parse_args()
infile = args.infile
outdir = args.outdir




packet_sizes = [1024, 512]
rb_counts = [2048,1024,512]
#mcs = ['6','3','2','ideal']
mcs = ['6','3','2']
batchsizes=['32']
#ddio_setups=['2','4','11','clean','cleans','clean11','cleans11']
ddio_setups=['2','11','cleans','cleans11']


pslen=len(packet_sizes)
rblen=len(rb_counts)
mclen=len(mcs)
ddioslen=len(ddio_setups)

toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]


def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

field_names=[]
field_names.append('app_dirty_evct')
field_names.append('rb_dirty_evct')
field_names.append('lb_dirty_evct')
field_names.append('NF_app_access')
field_names.append('rb_access')
field_names.append('lb_access')
field_names.append('Memhog_access')

##color_list= [[['black'] for l in range(ddioslen)] for k in range(mclen)]
##color_list[getindex('6',mcs)][getindex('2',ddio_setups)]='navy'
##color_list[getindex('6',mcs)][getindex('11',ddio_setups)]='blue'
##color_list[getindex('6',mcs)][getindex('cleans',ddio_setups)]='aqua'
##color_list[getindex('6',mcs)][getindex('cleans11',ddio_setups)]='lightcyan'
##
##color_list[getindex('3',mcs)][getindex('2',ddio_setups)]='darkgoldenrod'
##color_list[getindex('3',mcs)][getindex('11',ddio_setups)]='gold'
##color_list[getindex('3',mcs)][getindex('cleans',ddio_setups)]='yellow'
##color_list[getindex('3',mcs)][getindex('cleans11',ddio_setups)]='lemonchiffon'
##
##color_list[getindex('2',mcs)][getindex('2',ddio_setups)]='darkred'
##color_list[getindex('2',mcs)][getindex('11',ddio_setups)]='red'
##color_list[getindex('2',mcs)][getindex('cleans',ddio_setups)]='deeppink'
##color_list[getindex('2',mcs)][getindex('cleans11',ddio_setups)]='pink'

color_list=['black' for l in range(len(field_names))]
color_list[getindex('app_dirty_evct',field_names    )] ='navy'
color_list[getindex('rb_dirty_evct' ,field_names    )]  ='purple'
color_list[getindex('lb_dirty_evct' ,field_names    )]  ='aqua'
color_list[getindex('NF_app_access' ,field_names    )]  ='yellow'
color_list[getindex('Memhog_access' ,field_names    )]  ='orange'
color_list[getindex('rb_access'     ,field_names    )]  ='green'
color_list[getindex('lb_access'     ,field_names    )]  ='red'


#xtick_labels=[]
#for l in range(pslen):
#    for m in range(rblen):
#        ### * 18 for num cores
#        size_in_mb = packet_sizes[l]*rb_counts[m]*18 / 1000000;
#        size_in_mb  = size_in_mb - (size_in_mb % 0.1)
#        xtick_labels.append(str(packet_sizes[l])+'_'+str(rb_counts[m])+'_'+str(size_in_mb)+'MB')

xtick_labels=[]
for dsi in range(1,ddioslen):
    xtick_labels.append(str(ddio_setups[dsi]))


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
        ps=su[0]
        rbc=su[1]
        mc=su[2]
        ds=su[3]
        ds=ds.split('ways')[0]
        ##### get indexes in array
        psi=getindex(ps, packet_sizes)
        rbci=getindex(rbc, rb_counts)
        mci = getindex(mc,mcs)
        dsi= getindex(ds, ddio_setups)

        validSetup=True
        if psi==-1:
            line=f.readline();
            continue
        if rbci==-1:
            line=f.readline();
            continue
        if mci==-1:
            line=f.readline();
            continue
        if dsi==-1:
            line=f.readline();
            continue


        #numpackets_multiplier = 2500000 * 8 / 1000000000#transslate to Gbps
        #ir_in_Gbps=float(tmp[1]) * packet_sizes[psi] * numpackets_multiplier
        #st_in_ns = float(tmp[3])*0.4
        #wrlat_in_ns = float(tmp[10])*0.4
        #rdlat_in_ns = float(tmp[11])*0.4

        if (len(toparr[psi][rbci][mci][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])
        
        toparr[psi][rbci][mci][dsi].append(float(tmp[1]))   ##0 app_dirty_ev
        toparr[psi][rbci][mci][dsi].append(float(tmp[2]))   ##1 rb_dirty_ev
        toparr[psi][rbci][mci][dsi].append(float(tmp[3]))   ##2 lb_dirty_ev
        toparr[psi][rbci][mci][dsi].append(float(tmp[4]))   ##3 NF_app_access
        toparr[psi][rbci][mci][dsi].append(float(tmp[6]))   ##4 rb_access
        toparr[psi][rbci][mci][dsi].append(float(tmp[7]))   ##5 lb_access
        #### repositioning memhog to be at the end
        toparr[psi][rbci][mci][dsi].append(float(tmp[5]))   ##6 memhog_access

        line=f.readline();

    print('toparr populated')

    ##produce one plot per packetsize_rbcount
    t_psi=0     ## 0 - 1024, 1 - 512 
    t_rbci=1    ## 0 - 2048, 1- 1024, 2 - 512


    os.system('mkdir '+outdir)
    os.chdir(outdir)


    pslen=len(packet_sizes)
    rblen=len(rb_counts)
    mclen=len(mcs)
    ddioslen=len(ddio_setups)

    #####debug code
    psii=getindex('1024', packet_sizes)
    rbcii=getindex('2048', rb_counts)
    mcii = getindex('6',mcs)
    dsii= getindex('11', ddio_setups)
    print('1024_2048_6_11: rb_dirty_evict: '+str(toparr[psii][rbcii][mcii][dsii][1]))

    

    for psi in range(pslen):
        for rbi in range(rblen):
            #for mci in range(1,mclen): 
            for mci in range(mclen): 
            
                ########### 1 plot per ps,rb,mc setup, all ddio setup in one plot
                tmparr=[[] for l in range(len(field_names))]
                for dsi in range(1,ddioslen):
                    for j in range(len(field_names)):
                        tmparr[j].append(toparr[psi][rbi][mci][dsi][j])


                ifig,iax=plt.subplots()
                iax.set_title(str(packet_sizes[psi])+'_'+str(rb_counts[rbi])+'_'+str(mcs[mci]))
                X_axis = np.arange(1,ddioslen)

                #####dbgprint
                if psi==0:
                    if rbi==0:
                        if mci==0:
                            print('1024_2048_6_11: rb_dirty_evict: '+str(tmparr[1][1]))


                barwidth = 0.5
                iax.bar(X_axis, tmparr[0], edgecolor='black',alpha=0.8,color=color_list[0], label=field_names[0], width=barwidth)
                botarr = tmparr[0];
                for j in range(1,len(field_names)):
                    #iax.bar(X_axis, tmparr[j], bottom=tmparr[j-1], edgecolor='black',alpha=1.0,color=color_list[j], label=field_names[j], width=barwidth)
                                        #botarr=botarr+tmparr[j-1]
                    iax.bar(X_axis, tmparr[j], bottom=botarr, edgecolor='black',alpha=1.0,color=color_list[j], label=field_names[j], width=barwidth)
                    for k in range(len(botarr)):
                        botarr[k]=botarr[k]+tmparr[j][k]

                plt.xticks(X_axis, xtick_labels)
                iax.legend(ncol=2)
                plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
                ifig.set_size_inches(16,3)
                plt.subplots_adjust(bottom=0.2)
                plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)

                #ifig.savefig(str(psi)+'_'+str(rbi)+'_'+str(mci)+'.png')
                ifig.savefig(str(packet_sizes[psi])+'_'+str(rb_counts[rbi])+'_'+str(mcs[mci]))


##################################



##    for i in range(len(field_names)):
##        pslen=len(packet_sizes)
##        rblen=len(rb_counts)
##        mclen=len(mcs)
##        ddioslen=len(ddio_setups)
##
##        tmparr = [[[] for l in range(ddioslen)] for k in range(mclen)]
##        #tmparr = [[[] for m in range(rblen)] for l in range(pslen)]
##    
##        for j in range(len(mcs)):
##            for k in range(len(ddio_setups)):
##                for l in range(pslen):
##                    for m in range(rblen):
##                        tmparr[j][k].append(toparr[l][m][j][k][i])
##
##        
##        ifig,iax=plt.subplots()
##        iax.set_title(field_names[i])
##        X_axis = np.arange(pslen*rblen)
##
##        barwidth = 0.05
##        ### just plot one ideal mc
##        iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)
##
##        #for j in range(1,len(mcs)):
##        #    for k in range(len(ddio_setups)):
##        for j in reversed(range(1,len(mcs))):
##            for k in reversed(range(len(ddio_setups))):
##                plot_ddioslen = 2
##                kk = k
##                #if k==getindex('cleans',ddio_setups):
##                #    kk=getindex('2',ddio_setups)
##                #if k==getindex('cleans11',ddio_setups):
##                #    kk=getindex('11',ddio_setups)
##
##                xoffset = barwidth*((j*ddioslen)+kk)
##                iax.bar(X_axis-0.4+(xoffset), tmparr[j][k],edgecolor='black', alpha=0.8, color=color_list[j][k], label=str(mcs[j])+'mc_'+str(ddio_setups[k])+'w', width=barwidth)
##
##        plt.xticks(X_axis, xtick_labels)
##        #iax.legend(ncol=2)
##        plt.setp(iax.get_xticklabels(), rotation=15, horizontalalignment='right')
##        ifig.set_size_inches(16,3)
##        plt.subplots_adjust(bottom=0.2)
##        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)
##
##        #####Y LABELS#####
##        #if 'maxIR' in field_names[i]:
##        #    plt.ylabel('Gbps')
##        #if 'MBW' in field_names[i]:
##        #    plt.ylabel('avg Memory BW per controller (GB/s)')
##        #if 'ST' in field_names[i]:
##        #    plt.ylabel('avg service time (ns)')
##        #if 'e2e' in field_names[i]:
##        #    plt.ylabel('avg e2e latency (ns)')
##
##
##
##
##        ifig.savefig(field_names[i]+'.png')
##        #ifig.savefig(field_names[i]+'.png',dpi=1000)
##        
##
##
##exit
##    
