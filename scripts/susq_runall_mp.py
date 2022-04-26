#!/usr/bin/env python

import os
import sys
from multiprocessing import Process                                             
from multiprocessing import Semaphore 

##############  1KB PACKETS  ##################

mcs = ['4'] 

q_depths = ['50','250','450']
#rb_pool_sizes=['2097152','4194304']
#rb_pool_sizes=['4194304']
rb_pool_sizes=['2097152']

#out_dir_prefix='0420_TLD_many_keys_batch/'
out_dir_prefix='0421_TLD_2KBUFFERS_ISOL/'

#ddio_setups = ['2','11','cleans','cleans11','mem']
ddio_setups = ['2','6','12','clean','clean6','clean12']


home_base='/shared/acho44'


pcmds=[]
for mc in mcs:
    for qd in q_depths:
        for rbps in rb_pool_sizes:
            for ds in ddio_setups:
                #base_cfg = 'l3fwd_ddio_sustain_q_base_matmul_ICL.cfg'
                base_cfg = 'l3fwd_ddio_sustain_q_base_ICL_ISOL.cfg'
                ds_flag = ' --ddio_ways '+ds+' '                           
                if 'clean' in ds:
                    ds_flag = ' --ddio_ways 2 --clean_recv 1 '
                if 'clean12' in ds:
                    ds_flag = ' --ddio_ways 12 --clean_recv 1 '
                #if 'cleans' in ds:
                #    ds_flag = ' --ddio_ways 2 --clean_recv 2 '
                #if 'cleans12' in ds:
                #    ds_flag = ' --ddio_ways 12 --clean_recv 2 '
                if 'clean6' in ds:
                    ds_flag = ' --ddio_ways 6 --clean_recv 1 '
                #if 'mem' in ds:
                #    ds_flag = ' --ddio_ways 2' ##doesn't even matter
                #    base_cfg = 'l3fwd_mem_sustain_q_base_matmul_ICL.cfg'
                os.chdir(home_base)
                #outpath=out_dir_prefix+'susq_'+qd+'_'+rbps+'_'+ds
                outpath=out_dir_prefix+'susq_'+qd+'_4k_'+ds+'_'+mc
                rcmd= './set_IR_and_run.py  --base_cfg '+base_cfg+'  --mem_controllers '+mc+' --forced_packet_size 1024  --batchsize 32 --packet_count 500000  --num_keys 16384  --recv_buf_pool_size '+rbps+' --q_depth '+qd+ds_flag+' --out_dir '+outpath
                #os.system(rcmd)
                pcmds.append(rcmd)
    
def f(fcmd, sema):                                                              
    print(fcmd)                                                                 
    os.system(fcmd)                                                             
    sema.release()                                                              
 


if __name__=='__main__':
    concurrency = 6
    sema = Semaphore(concurrency)
    all_processes=[]

    tmp=0
    tmp2=0

    for pcmd in pcmds:
        sema.acquire()
        p=Process(target=f, args=(pcmd,sema))
        all_processes.append(p)
        p.start()
        print('runall launched task no '+str(tmp))
        tmp=tmp+1
        ### clean up periodically. making sure to not send kill while things run
        #if(tmp==concurrency*2):
        #    for p in all_processes:
        #        p.join()
        #    tmp2=tmp2+1
        #    tmp=0
        #    #print('preiodic cleanup')
        #    #clean_runaways()
        #    #print(str(tmp2)+'th '+str(concurrency*2)+' tasks done')

    for p in all_processes:
        p.join()


    print('susq_runall_mp - done')
    os.system('ipcrm -a')
                                          


