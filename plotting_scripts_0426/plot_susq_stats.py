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
parser.add_argument('--nocl', type=bool, default=False)  
args = parser.parse_args()
infile = args.infile
outdir = args.outdir
nocl = args.nocl

print(infile)

freq_in_Ghz = 3.2


#mcs = ['8']
#q_depths =['50','150','200','250','300','350','400']
#q_depths =['50','150','250','350','450']
q_depths =['50','250','450']
#q_depths =['250','450']
#q_depths =['450']
#ddio_setups=['2','11','cleans','cleans11','mem']
#ddio_setups=['2','12','mem','clean','clean12']
#ddio_setups=['2','12','clean','clean12']
ways=['2','6','12']
ddio_setups=['nocl','clean']
if (nocl):
    ddio_setups=['nocl']


qdlen = len(q_depths)
ddioslen=len(ddio_setups)
wlen=len(ways)

#toparr = [[[[[] for l in range(ddioslen)] for k in range(mclen)] for j in range(rblen)] for i in range(pslen)]
toparr = [[[[] for l in range(ddioslen)] for j in range(wlen)] for k in range(qdlen)]

idealarr = [[] for k in range(qdlen)]



def getindex(elem, arr):
    for i in range(len(arr)):
        if str(arr[i])==elem:
            return i
    print('didnt find elem '+elem+' in arr')
    exit
    return -1

def get_ds_index(elem):
    if 'clean' in elem:
        if ('clean' in ddio_setups):
            return 1
        else:
            return -1
    else:
        return 0



field_names=[]
field_names.append('NWThroughput') ## raw data given by interval, need to convert
field_names.append('NIC_RB_Miss_Rate')
field_names.append('Core_RB_Miss_Rate')
field_names.append('MBW')
#field_names.append('Memhog_ipcs')

#color_list= [['black'] for l in range(wlen*2)]
#color_list[getindex('2',ways)]='#ABBFB0'
#color_list[getindex('6',ways)]='#799A82'
#color_list[getindex('12',ways)]='#3D5A45'

color_list=[ '#ABBFB0', '#799A82', '#3D5A45', '#A89AE4', '#7C67D6', '#42347E']

#colors = [ '#ABBFB0', '#799A82', '#3D5A45',       '#C26989', '#6e92f2']
# greens: '#a4c1ab','#3b6d56',                                                  
#purples warm: '#dba5ce','#7B476F','#451539',                                   
# oranges: '#FFC966','#e58606','#ffa500'                                        
# reds: '#4B0215',                                                              
# blues:'#6e92f2',  

#purples:  '#A89AE4', '#7C67D6', '#42347E',

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
        if 'ideal' in ds:
            qdi = getindex(qd,q_depths)
            if qdi==-1:
                line=f.readline();
                continue
            
            interval_to_IR = freq_in_Ghz*1024*8 #divide this by interval
            ir_in_Gbps=0
            if( float(tmp[1]) != 0):
                ir_in_Gbps=interval_to_IR / (float(tmp[1]))

            ir_in_Mrps=ir_in_Gbps*1024/(1024*8)

            if (len(idealarr[qdi])!=0):
                print('ERROR: duplicate setup found, '+tmp[0])
            
            idealarr[qdi].append(ir_in_Mrps)      ##0 IR
            idealarr[qdi].append(float(tmp[2]))   ##1 NIC_RB_MR
            idealarr[qdi].append(float(tmp[3]))   ##2 CORE_RB_MR
            idealarr[qdi].append(float(tmp[4]))   ##3 MBW

 
        else:
            #print(mc)
            ##### get indexes in array
            qdi = getindex(qd,q_depths)
            dsi= get_ds_index(ds)
            dw= ds.replace('clean','')
            dwi=getindex(dw,ways)

            validSetup=True
            if qdi==-1:
                line=f.readline();
                continue
            if dsi==-1:
                line=f.readline();
                continue
            if dwi==-1:
                line=f.readline();
                continue


            interval_to_IR = freq_in_Ghz*1024*8 #divide this by interval
            ir_in_Gbps=0
            if( float(tmp[1]) != 0):
                ir_in_Gbps=interval_to_IR / (float(tmp[1]))

            ir_in_Mrps=ir_in_Gbps*1024/(1024*8)

            if (len(toparr[qdi][dwi][dsi])!=0):
                print('ERROR: duplicate setup found, '+tmp[0])
            
            toparr[qdi][dwi][dsi].append(ir_in_Mrps)      ##0 IR
            toparr[qdi][dwi][dsi].append(float(tmp[2]))   ##1 NIC_RB_MR
            toparr[qdi][dwi][dsi].append(float(tmp[3]))   ##2 CORE_RB_MR
            toparr[qdi][dwi][dsi].append(4*float(tmp[4]))   ##3 MBW

            #print(str(mci)+str(qdi)+str(dsi))

        line=f.readline();

    print('toparr populated')
    ###dbg
    qdi = getindex('50',q_depths)
    #dsi= getindex('2', ddio_setups)
    #mci= getindex('2', mcs)
    #print(str(toparr[mci][qdi][dsi][0]))

    os.system('mkdir '+outdir)
    os.chdir(outdir)

    matplotlib.rcParams.update({'font.size': 50})

    xtick_labels=[]
    for l in range(qdlen):
        #print(str(l))
        core_MR=str(int(toparr[l][0][0][2] * 100)) # leakyDMA rate with 2way DDIO
        xtick_labels.append(str(q_depths[l]))


    ### for legend
    dummy_whitebar = []
    for j in range(qdlen):
        dummy_whitebar.append(0)

    for i in range(len(field_names)):
        qdlen=len(q_depths)

        #tmparr = [[[] for l in range(ddioslen)] for k in range(qdlen)]
        #tmparr = [[] for l in range(ddioslen)]
        tmparr = [[[] for l in range(ddioslen)] for k in range(wlen)]
        tmpidealarr=[]

        for l in range(qdlen):
            
            tmpidealarr.append(idealarr[l][i])

            for j in range(wlen):
                for k in range(len(ddio_setups)):
                    #print(str(l)+','+str(j)+','+str(k))
                    #tmparr[l][k].append(toparr[j][k][i])
                    if(len(toparr[l][j][k])!=0):
                        tmparr[j][k].append(toparr[l][j][k][i])
                    else:
                        tmparr[j][k].append(0)
                    #tmparr[l][k].append(1)

        
        ifig,iax=plt.subplots()
        #iax.set_title(field_names[i])
        X_axis = np.arange(qdlen)

        barwidth = 0.2
        ### just plot one ideal mc

        #for j in range(1,len(mcs)):
        #    for k in range(len(ddio_setups)):
        if ('MBW' in field_names[i]) or ('NIC_RB_Miss_Rate' in field_names[i]): 
            for k in range(len(ddio_setups)):

                for j in range(len(ways)):

                    xoffset = barwidth*(j)
                    alval = 1 #clean
                    label_name='DDIO '+str(ways[j])+' ways'
                    if(k==1):#clean
                        #alval=1
                        label_name='DDIO '+str(ways[j])+' ways + Sweeper'

                    iax.bar(X_axis-barwidth*1.5+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, hatch='', color=color_list[j+(k*wlen)], label=label_name, width=barwidth, zorder=5)




        else:
            for k in reversed(range(len(ddio_setups))):
                for j in range(len(ways)):
                    xoffset = barwidth*(j)
                    alval = 1 #clean
                    label_name='DDIO '+str(ways[j])+' ways'
                    if(k==1):#clean
                    #    alval=1
                    #    hpat=''
                    #    label_name='DDIO '+str(ways[j])+' ways'
                        label_name='DDIO '+str(ways[j])+' ways + Sweeper'

                    iax.bar(X_axis-barwidth*1.5+(xoffset), tmparr[j][k],edgecolor='black', alpha=alval, hatch='', color=color_list[j+(k*wlen)], label=label_name, width=barwidth, zorder=5)


        ##plot ideal bar
        iax.bar(X_axis-barwidth*1.5 + barwidth*3, tmpidealarr,edgecolor='black', alpha=1, hatch='', color='#C26989', label='Ideal DDIO', width=barwidth, zorder=5)


        ### for legend
        #if(not nocl):
        #    iax.bar(X_axis-barwidth/2, dummy_whitebar, edgecolor='black', alpha=1, hatch='/', color='white', label='+Sweeper', width=barwidth, zorder=5)


        plt.xticks(X_axis, xtick_labels)
        iax.legend(bbox_to_anchor=(0.5,1.2) , ncol=2, loc='center')#, columnspacing=)
        plt.setp(iax.get_xticklabels(), horizontalalignment='center')
        #ifig.set_size_inches(16,3)
        ifig.set_size_inches(20,16.5)
        #plt.subplots_adjust(bottom=0.2)
        plt.grid(color='gray', linestyle='--', linewidth=0.2, markevery=int, zorder=0, axis='y')

        plt.xlabel('\nQueued Packets per Core')

        ####Y LABELS#####
        if 'NWThroughput' in field_names[i]:
            plt.ylabel('Throughput (Mrps)\n')
        if 'MBW' in field_names[i]:
            plt.ylabel('Memory Bandwidth (GB/s)\n')
        if 'ST' in field_names[i]:
            plt.ylabel('avg service time (ns)')
        if 'e2e' in field_names[i]:
            plt.ylabel('avg e2e latency (ns)')




        ifig.savefig('TLD_'+field_names[i]+'.pdf', bbox_inches='tight')
        #ifig.savefig(field_names[i]+'.png',dpi=1000)
        


exit
    
