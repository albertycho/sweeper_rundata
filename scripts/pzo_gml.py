#!/usr/bin/env python3

import os
import sys
import csv
import math
#import statistics
#import numpy as np
#import matplotlib



os.system('../process_zsim_out.py');
os.system('../get_mem_lat.py');
os.system('../get_avg_mbw.py');
os.system('../get_memhog_perf.py');
os.system('cat stat_summary.txt');

