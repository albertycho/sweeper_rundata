#!/usr/bin/env python3

import os
import sys 
import csv 
import math
import statistics
import numpy as np
from os.path import exists

#for dd in os.listdir('.'):
for jj in range(10,38,1):
    dd = '0'+str(jj)
    if exists(dd):
        os.chdir(dd)
        os.system('python3 ../get_mem_lat.py')
        os.chdir('..')


