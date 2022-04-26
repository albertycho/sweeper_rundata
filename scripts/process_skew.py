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



home = '/nethome/acho/zsim/zSim'
outdir = '/shared/mvemmou/zSim'

ingress = ["ideal"]#,"mem","llc","llc"]
egress = ["ideal"]#,"mem","llc_inval","llc_non_inval"]

cumulative_skew_sample = []
idx = 0

for k in range(len(ingress)):
    
    ingr = ingress[k]
    egr = egress[k]

    total = []

    #os.chdir(outdir+'/phase_length_sens/ingr_'+ingr+'_egr_'+egr+'/phase_len_10000')

    for d in os.listdir('.'):
        if 'skew_core' in d:
            
            cumulative_skew = []
            
            arr = []
            core_id = d.split('_')[3].split('.')[0]
            skew_file = open(d,'r')
            skew_outf = open('skew_out_core'+core_id+'.csv', 'w')
            line = skew_file.readline()
            line = skew_file.readline()
            while line:
                if 'zinfo' in line:
                    line=skew_file.readline()
                    break;
                tmparr = line.split(': ')
                phase = tmparr[1]
                tss = tmparr[2].split(' ')
                skew = int(tss[1]) - int(tss[0])
                skew_outf.write(phase+', ' + str(skew)+',\n')

                cumulative_skew.append(skew)
                line=skew_file.readline()
            if '3' in core_id:
                print ('core_3')
                cumulative_skew_sample = cumulative_skew
                
            skew_file.close()


            if(len(cumulative_skew)!=0):
                skew_outf.write("avgSkew, "+str(sum(cumulative_skew)/len(cumulative_skew))+",\n")
                skew_outf.write("maxSkew, "+str(max(cumulative_skew))+",\n")
                skew_outf.write("minSkew, "+str(min(cumulative_skew))+",\n")
                skew_outf.write("90%Skew, "+str(np.percentile(cumulative_skew,90))+",\n")
                skew_outf.write("99%Skew, "+str(np.percentile(cumulative_skew,99))+",\n")
            skew_outf.close()

#x = np.linspace(0, len(cumulative_st), len(cumulative_st))
##plt.scatter(x,cumulative_st,color="blue")
##plt.scatter(x,cumulative_e2e,color="black")
#plt.plot(x,cumulative_e2e,color="black", linewidth=0.1)
##plt.plot(x,cumulative_st,color="blue", linewidth=0.1)
#plt.plot(x,cumulative_hft,color="green", linewidth=0.1)
#plt.savefig('service_times.png',dpi=720)
