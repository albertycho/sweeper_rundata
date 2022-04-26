#!/usr/bin/env python

import os
import sys

from multiprocessing import Process                                             
from multiprocessing import Semaphore   

rerun_dirs=[]
curdir=os.getcwd()

rrcmd='timeout 30m ./zsim conf.cfg 1> res.txt 2>app.txt '

f1 = open('leakyDMA_stats.csv')
line=f1.readline()
while line:
    if '0,0,0,0' in line:
        fail_dir=line.split(',')[0]
        rerun_dirs.append(fail_dir)
    line=f1.readline()

print(rerun_dirs)

#for rrd in rerun_dirs:
#    os.chdir(rrd)
#    print(os.getcwd())
#    #os.system('./zsim conf.cfg 1> res.txt 2>app.txt &')
#    os.system(rrcmd)
#    os.chdir(curdir)
#

def f(rrdir, sema):
    print(rrd)
    os.chdir(rrd)
    print(os.getcwd())
    os.system(rrcmd)
    os.chdir(curdir)
    sema.release()




if __name__=='__main__':
    concurrency = 6
    sema = Semaphore(concurrency)
    all_processes=[]

    tmp=0
    tmp2=0

    for rrd in rerun_dirs:
        sema.acquire()
        p=Process(target=f, args=(rrd,sema))
        all_processes.append(p)
        p.start()
        print('rerunlaunched task no '+str(tmp))
        tmp=tmp+1

    for p in all_processes:
        p.join()


    print('rerun_mp - '+' Done')
    #os.system('ipcrm -a')
    
