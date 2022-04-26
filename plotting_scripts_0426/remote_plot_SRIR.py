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

parser = argparse.ArgumentParser()                                              
parser.add_argument('--range', type=int, default=0)  
parser.add_argument('--start', type=int, default=0)  
args = parser.parse_args()

x_range = args.range
x_start = args.start


IRS = []
SRS = []
cq_sizes = []
ceq_sizes = []

if 'IRSR_dump.csv' in os.listdir('.'):
    f=open('IRSR_dump.csv','r')
    line=f.readline();
    line=f.readline();
    while line:
        tmp=line.split(',')
        IRS.append(int(tmp[0]))
        SRS.append(int(tmp[1]))
        cq_sizes.append(int(tmp[2]))
        ceq_sizes.append(int(tmp[3]))
        line=f.readline()
                        
    f.close()


    #comment this back in when using plot
    #x = np.linspace(0, len(SRS), len(SRS))

    if(x_range==0):
        x = np.arange(0, len(SRS))

        plt.plot(x,IRS,color="black", linewidth=0.1)
        plt.plot(x,SRS,color="green", linewidth=0.1)
        plt.plot(x,cq_sizes,color="red", linewidth=0.1)
        plt.plot(x,ceq_sizes,color="blue", linewidth=0.1)
        plt.savefig('IRSR_dump.png',dpi=720)
    else: 
        x2 = np.arange(x_start, x_range)
        IRS2=IRS[x_start:x_range]
        SRS2=SRS[x_start:x_range]
        cqs2=cq_sizes[x_start:x_range]
        ceqs2=ceq_sizes[x_start:x_range]

        plt.plot(x2,IRS2,color="black", linewidth=1)
        plt.plot(x2,SRS2,color="green", linewidth=1)
        plt.plot(x2,cqs2,color="red", linewidth=1)
        plt.plot(x2,ceqs2,color="blue", linewidth=1)
        plt.savefig('IRSR_dump_'+str(x_range)+'phases.png',dpi=720)


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


