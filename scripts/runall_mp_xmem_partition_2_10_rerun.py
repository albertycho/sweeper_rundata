#!/usr/bin/env python

import os
import sys

from multiprocessing import Process
from multiprocessing import Semaphore




batch_script_name = './batch_ddio_run.py '
#output_path_base = '/shared/acho44/0329_l3fwd_llc_resident_memhog_VAR_POLICIES/'
output_path_base = '/shared/acho44/0417_l3fwd_xmem_6MB_partition_10_2_reruns/'
#base_cfg_name = ' l3fwd_ddio.cfg '
base_cfg_name = ' l3fwd_ddio_xmem_mt_ICL_'
#packet_sizes = [512, 1024]
packet_sizes = [1024]
rb_counts = [512,1024,2048]
mcs = ['4']
num_keys = '16' #minimize NF's WS size 
#num_keys = '1024'

batchsizes=['32']

#ddio_setups=['clean','nocl']
ddio_setups=['clean','nocl']
partition_setups=['2_10']



pcmds=[]
for ps in packet_sizes:
    for ds in ddio_setups:
        for rbc in rb_counts:
            for mc in mcs:
                for bs in batchsizes: #just keeping the name convention
                    for pts in partition_setups:
                        rb_pool_size=ps*rbc
                        ds_flag = ' --clean_recv 0 '
                        if 'clean' in ds:
                            ds_flag = ' --clean_recv 1 '
                        batchdir_name = output_path_base+str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_batch_'+bs+ds+'_pt'+pts
                        tmpcmd = batch_script_name+' --base_cfg '+base_cfg_name+pts+'.cfg'+\
                                ' --mem_controllers '+mc+' --forced_packet_size '+str(ps)+\
                                ' --recv_buf_pool_size '+str(rb_pool_size)+' --batchsize '+bs+ds_flag+\
                                ' --batch_dir '+batchdir_name+' --num_keys '+num_keys+' --matN 10 '
                        
                        pcmds.append(tmpcmd)
                        print(tmpcmd)
    



def f(fcmd, sema):
    print(fcmd)
    os.system(fcmd)
    sema.release()


def clean_runaways():
    os.system('killall -9 herd')
    os.system('killall -9 l3fwd')
    os.system('killall -9 simpNF')
    os.system('killall -9 zsim')
    os.system('killall -9 nic_egress_proxy_app')
    os.system('killall -9 nic_proxy_app')
    os.system('killall -9 memhog_mt')
    os.system('ipcrm -a')




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

    for p in all_processes:
        p.join()


    print('runall_mp - '+' Done')
    os.system('ipcrm -a')
    
