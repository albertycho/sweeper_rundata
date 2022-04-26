#!/usr/bin/env python3

import os
import sys
import csv
import math
import statistics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 





cumulative_bw = []

mbw_stats_file = open("mbw_stats.txt", 'w')

for d in os.listdir('.'):
    if 'memory_controller_' in d:
        mbwraw=open(d,'r')
        line = mbwraw.readline()
        tmpmbw = []
        while line:
            bw = float(line)
            tmpmbw.append(bw)
            cumulative_bw.append(bw)
            line=mbwraw.readline()
        if (len(tmpmbw)>0):
            avgbw = str(sum(tmpmbw)/len(tmpmbw))
            mbw_stats_file.write(d+' avgbw: '+avgbw+'\n')
        mbwraw.close()
##if (len(cumulative_bw) >0):
##    mbw_stats_file.write(d+' avgbw: '+avgbw)

mbw_stats_file.close()

os.system('cat mbw_stats.txt >> stat_summary.txt')

