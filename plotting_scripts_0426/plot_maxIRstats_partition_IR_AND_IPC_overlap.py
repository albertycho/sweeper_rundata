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
parser.add_argument('--infile', type=str, default='max_ir_stats.csv')  
parser.add_argument('--outdir', type=str, default='IR_AND_IPC')  
args = parser.parse_args()
infile = args.infile
outdir = args.outdir




#packet_sizes = [1024, 512]
#packet_sizes = [1024]
#rb_counts = [2048,1024,512]
#mcs = ['ideal','8','4']
mcs = ['4']
batchsizes=['32']
#ddio_setups=['2','12','clean','clean12']
ddio_setups=['nocl','clean']
partitions=['2_10','4_8','6_6','8_4','10_2']
#partitions=['2_10','6_6','8_4','10_2']

#pslen=len(packet_sizes)
#rblen=len(rb_counts)
#mclen=len(mcs)
ddioslen=len(ddio_setups)
ptlen=len(partitions)


#toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]
toparr = [[[] for l in range(ddioslen)] for k in range(ptlen)]



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

color_list= [[['black'] for l in range(ddioslen)] for j in range(2)]

#color_list[0][getindex('clean',ddio_setups)]='color_list[0][0]' #IR
#color_list[0][getindex('nocl',ddio_setups)]='color_list[0][0]'   #IR
##color_list[0][getindex('clean',ddio_setups)]='#dba5ce' #IR
##color_list[0][getindex('nocl',ddio_setups)]='#dba5ce'   #IR
##
##
###color_list[1][getindex('clean',ddio_setups)]='green' #IPC
###color_list[1][getindex('nocl',ddio_setups)]='green'   #IPC
##color_list[1][getindex('clean',ddio_setups)]='#a4c1ab' #IPC
##color_list[1][getindex('nocl',ddio_setups)]='#a4c1ab'   #IPC

#color_list[0][getindex('clean',ddio_setups)]='#7B476F' #IR
#color_list[0][getindex('nocl',ddio_setups)]='#7B476F'   #IR
#
#color_list[1][getindex('clean',ddio_setups)]='#3b6d56' #IPC
#color_list[1][getindex('nocl',ddio_setups)]='#3b6d56'   #IPC

color_list[0][getindex('clean',ddio_setups)]='#42347E'  # '#799A82' #'#7B476F' #IR   
color_list[0][getindex('nocl',ddio_setups)]= '#42347E'  # '#799A82' #'#7B476F'   #IR 
color_list[1][getindex('clean',ddio_setups)]='#3D5A45'  #'#7C67D6' #'#3b6d56' #IPC
color_list[1][getindex('nocl',ddio_setups)]= '#3D5A45'  #'#7C67D6' #'#3b6d56'   #IPC
#3b6d56

#color_list[getindex('2',mcs)][getindex('2',ddio_setups)]='darkred'
#color_list[getindex('2',mcs)][getindex('11',ddio_setups)]='red'
#color_list[getindex('2',mcs)][getindex('clean',ddio_setups)]='deeppink'
#color_list[getindex('2',mcs)][getindex('clean11',ddio_setups)]='pink'


#for l in range(pslen):
#    for m in range(rblen):
#        ### * 18 for num cores
#        size_in_mb = packet_sizes[l]*rb_counts[m]*18 / 1000000;
#        size_in_mb  = size_in_mb - (size_in_mb % 0.1)
#        xtick_labels.append(str(packet_sizes[l])+'_'+str(rb_counts[m])+'_'+str(size_in_mb)+'MB')



### used for normalizing
max_ir=0
max_ipc=0
max_ir_cfg='0'
max_ipc_cfg='0'


if infile in os.listdir('.'):
    f=open(infile,'r')
    #line=f.readline();
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
        #ds=ds.split('ways')[0]
        pts=su[4]+'_'+su[5]
        ##### get indexes in array
        #psi=getindex(ps, packet_sizes)
        #rbci=getindex(rbc, rb_counts)
        #mci = getindex(mc,mcs)
        dsi= getindex(ds, ddio_setups)
        pti= getindex(pts,partitions)

        validSetup=True
        #if psi==-1:
        #    line=f.readline();
        #    continue
        #if rbci==-1:
        #    line=f.readline();
        #    continue
        #if mci==-1:
        #    line=f.readline();
        #    continue
        if dsi==-1:
            line=f.readline();
            continue
        if pti==-1:
            line=f.readline();
            continue


        packet_size=1024
        numpackets_multiplier = 2500000 * 8 / 1000000000#transslate to Gbps
        ir_in_Gbps=float(tmp[1]) * packet_size * numpackets_multiplier
        st_in_ns = float(tmp[3])*0.4
        wrlat_in_ns = float(tmp[10])*0.4
        rdlat_in_ns = float(tmp[11])*0.4

        if (len(toparr[pti][dsi])!=0):
            print('ERROR: duplicate setup found, '+tmp[0])
        
        toparr[pti][dsi].append(ir_in_Gbps)      ##0 IR
        toparr[pti][dsi].append(float(tmp[2]))   ##1 MBW
        toparr[pti][dsi].append(st_in_ns)        ##2 ST
        toparr[pti][dsi].append(float(tmp[6]))   ##3 nic_rb_mr
        toparr[pti][dsi].append(float(tmp[12]))  ##4 mh_ipcs
        toparr[pti][dsi].append(float(tmp[13]))  ##5 mh_l3_mr
        toparr[pti][dsi].append(float(tmp[14]))  ##6 mh_cCycle_ratio

        if(ir_in_Gbps > max_ir):
            max_ir=ir_in_Gbps
            max_ir_cfg=pts+' '+ds
            max_ir_cfg=max_ir_cfg.replace('clean','Sweep')
        if((float(tmp[12])) > max_ipc):
            max_ipc = float(tmp[12])
            max_ipc_cfg=pts+' '+ds
            max_ipc_cfg=max_ipc_cfg.replace('clean','Sweep')


        line=f.readline();

    print('toparr populated')

    ##produce one plot per packetsize_rbcount
    t_psi=0     ## 0 - 1024, 1 - 512 
    t_rbci=1    ## 0 - 2048, 1- 1024, 2 - 512


    #os.system('mkdir '+outdir)
    
    partitions=['(2,10)','(4,8)','(6,6)','(8,4)','(10,2)']
    xtick_labels=[]
    for l in range(ptlen):
        xtick_labels.append(partitions[l])
    #os.chdir(outdir)

    
    ##############plotting#############

    ddioslen=len(ddio_setups)
    ptlen=len(partitions)

    irarr = [[] for l in range(ddioslen)]
    ipcarr = [[] for l in range(ddioslen)]
    #tmparr = [[[] for m in range(rblen)] for l in range(pslen)]
   
    matplotlib.rcParams.update({'font.size': 20})
    
    for j in range(len(partitions)):
        for k in range(len(ddio_setups)):
            irarr[k].append(toparr[j][k][0] / (max_ir))
            ipcarr[k].append(toparr[j][k][4] / (max_ipc))

    ### for legend
    dummy_whitebar = []
    for j in range(len(partitions)):
        dummy_whitebar.append(0)

    
    ifig,iax=plt.subplots()
    #iax.set_title('normalized l3fwd_IR and xmem_IPC')
    #X_axis = np.arange(pslen*rblen)
    X_axis = np.arange(ptlen)

    barwidth = 0.2
    ### just plot one ideal mc
    #iax.bar(X_axis-0.4+(barwidth*3), tmparr[0][0],edgecolor='black', alpha=0.5, color="black", label='ideal', width=barwidth)

    #for j in range(1,len(mcs)):
    #    for k in range(len(ddio_setups)):
    #for k in reversed(range(len(ddio_setups))):

    

    for k in reversed(range(len(ddio_setups))):

        xoffset = 0 # barwidth*4*(k)

        alval=1
        hpat=''
        ipclabel='XMEM IPC'
        irlabel='NW Throughput'
        if(k==1):
            alval=0.5
            hpat='/'
            ipclabel=''
            irlabel=''

        iax.bar(X_axis-barwidth*0.55+(xoffset), irarr[k],edgecolor='black', alpha=alval, hatch=hpat, color=color_list[0][k], label=irlabel, width=barwidth)
        iax.bar(X_axis-barwidth*0.55+(xoffset+barwidth*1.2), ipcarr[k],edgecolor='black', alpha=alval, hatch=hpat, color=color_list[1][k], label=ipclabel, width=barwidth)

    

    ### for legend
    iax.bar(X_axis-barwidth/2, dummy_whitebar, edgecolor='black', alpha=1, hatch='/', color='white', label='+Sweeper', width=barwidth)
    
    plt.xticks(X_axis, xtick_labels)
    handles, labels = iax.get_legend_handles_labels()
    #iax.legend(ncol=2, reversed(handles), reversed(labels), loc='upperleft')
    iax.legend(ncol=4,bbox_to_anchor=[0.5,1.15], loc='center')
    plt.setp(iax.get_xticklabels(), horizontalalignment='center')#rotation=15,)
    ifig.set_size_inches(10,4)
    #plt.subplots_adjust(bottom=0.2)
    plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int)
    #plt.tick_params(labelright=True)
    iax.yaxis.label.set_color(color_list[0][0])
    iax.spines['left'].set_color(color_list[0][0])
    iax.spines['left'].set_linewidth(2)
    iax.tick_params(axis='y', colors=color_list[0][0])

    iax.spines['right'].set_color(color_list[1][0])
    iax.spines['right'].set_linewidth(2)

    plt.xlabel('Partition: (DDIO_ways , collocated_app_ways)')
    iax.set_ylabel('Normalized to TP\n@ '+str(max_ir_cfg))
    #iax.set_ylabel('Normalized\nNW Thruput')

    #iax.right_ax.set_ylabel('right yaxis label')
    iax2=iax.twinx()
    iax2.yaxis.label.set_color(color_list[1][0])
    iax2.tick_params(axis='y', colors=color_list[1][0],bottom=True)
    iax2.set_ylabel('Normalized to\nIPC @ '+str(max_ipc_cfg))
    #iax2.set_ylabel('Normalized\nX-MEM IPCs')

    #plt.tight_layout()


    ifig.savefig('partition_IR_IPC'+'.png',bbox_inches='tight')
    #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
