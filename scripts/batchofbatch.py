#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists


for dd in os.listdir('.'):
#for jj in range(10,38,1):
    if not '.py' in dd:
        print(dd)
        os.chdir(dd)
        os.system('rm get_tail_latencies_from_batch.py')
        os.system('rm process_timestamps.py')
        os.system('cp /shared/acho44/get_tail_latencies_from_batch.py .')
        os.system('cp /shared/acho44/process_timestamps.py .')
        os.system('cp /shared/acho44/get_mem_lat.py .')
        os.system('cp /shared/acho44/get_avg_mbw.py .')
        os.system('python3 get_tail_latencies_from_batch.py')
        os.chdir('..')


