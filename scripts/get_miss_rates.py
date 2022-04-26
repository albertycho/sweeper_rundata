#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

f_miss_rate = open('miss_rates.csv','w')
net_total=0
app_total=0
net_miss=0
app_miss=0

if exists('zsim.out'):
    zsimout = open('zsim.out','r')
    line = zsimout.readline()
    found_l3_stat=False
    while line:
        if 'l3' in line:
            found_l3_stat=True
        if found_l3_stat:
            if 'netMiss:' in line:
                tmp = line.split('netMiss: ')[1]
                tmp2 = tmp.split(' ')[0]
                tmp3=int(tmp2)
                net_miss+=tmp3
                net_total+=tmp3
            if 'netHit:' in line:
                tmp = line.split('netHit: ')[1]
                tmp2 = tmp.split(' ')[0]
                tmp3=int(tmp2)
                net_total+=tmp3
            if 'appMiss:' in line:
                tmp = line.split('appMiss: ')[1]
                tmp2 = tmp.split(' ')[0]
                tmp3=int(tmp2)
                app_total+=tmp3
                app_miss+=tmp3
            if 'appHit:' in line:
                tmp = line.split('appHit: ')[1]
                tmp2 = tmp.split(' ')[0]
                tmp3=int(tmp2)
                app_total+=tmp3
        line=zsimout.readline()

    zsimout.close()
    net_miss_rate = net_miss/net_total
    app_miss_rate = app_miss/app_total
    f_miss_rate.write('net_miss_rate, '+str(net_miss_rate)+',\n')
    f_miss_rate.write('app_miss_rate, '+str(app_miss_rate)+',\n')
    f_miss_rate.close()

else:
    print('zsim.out not found\n')

