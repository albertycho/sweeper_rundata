#!/usr/bin/env python

import os
import sys

from multiprocessing import Process
from multiprocessing import Semaphore




batch_script_name = './batch_ddio_run.py '
#output_path_base = '/shared/acho44/0329_l3fwd_llc_resident_memhog_VAR_POLICIES/'
output_path_base = '/shared/acho44/0414_l3fwd_mm_BATCH_500/'
#base_cfg_name = ' l3fwd_ddio.cfg '
base_cfg_name = ' l3fwd_ddio_matmul_ICL.cfg '
#packet_sizes = [512, 1024]
packet_sizes = [1024]
rb_counts = [512,1024,2048]
mcs = ['8','4','ideal']
num_keys = '16384'
#num_keys = '1024'

batchsizes=['32']

#ddio_setups=['2','11','cleans','cleans11']
ddio_setups=['2','11']
#ddio_setups=['cleans','cleans11']



pcmds=[]
for ps in packet_sizes:
    for ds in ddio_setups:
        for rbc in rb_counts:
            for mc in mcs:
                for bs in batchsizes: #just keeping the name convention
                    rb_pool_size=ps*rbc
                    ds_flag = ' --ddio_ways '+ds+' '
                    if 'clean' in ds:
                        ds_flag = ' --ddio_ways 2 --clean_recv 1 '
                    if 'clean11' in ds:
                        ds_flag = ' --ddio_ways 11 --clean_recv 1 '
                    if 'cleans' in ds:
                        ds_flag = ' --ddio_ways 2 --clean_recv 2 '
                    if 'cleans11' in ds:
                        ds_flag = ' --ddio_ways 11 --clean_recv 2 '

                    tmpcmd = batch_script_name+' --base_cfg '+base_cfg_name+\
                            ' --mem_controllers '+mc+' --forced_packet_size '+str(ps)+\
                            ' --recv_buf_pool_size '+str(rb_pool_size)+' --batchsize '+bs+ds_flag+\
                            ' --batch_dir '+output_path_base+str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_batch_'+bs+ds+'ways'+' --num_keys '+num_keys+' --matN 500 '
                    
                    pcmds.append(tmpcmd)
    



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


    print('runall_mp - '+' Done')
    os.system('ipcrm -a')
    
