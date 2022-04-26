#!/usr/bin/env python

import os
import sys

from multiprocessing import Process
from multiprocessing import Semaphore




batch_script_name = './batch_ddio_run.py '
#output_path_base = '/shared/acho44/0329_l3fwd_llc_resident_memhog_VAR_POLICIES/'
output_path_base = '/shared/acho44/0420_l3fwd_ALONE_BATCH/'
#base_cfg_name = ' l3fwd_ddio.cfg '
base_cfg_name = ' l3fwd_ddio_ICL.cfg '
#packet_sizes = [512, 1024]
packet_sizes = [1024]
rb_counts = [512,1024,2048]
mcs = ['4']
#num_keys = '16384'
num_keys = '1024'

batchsizes=['32']

ddio_ways=['2','6','12','ideal']
#clean_setup=['clean','nocl']
clean_setup=['nocl']



pcmds=[]
for ps in packet_sizes:
    for ds in ddio_ways:
        for rbc in rb_counts:
            for mc in mcs:
                for bs in batchsizes: #just keeping the name convention
                    for cs in clean_setup:
                        base_cfg_name = ' l3fwd_ddio_ICL.cfg '
                        rb_pool_size=ps*rbc
                        cs_flag = ' --clean_recv 0 '
                        if 'clean' in cs:
                            cs_flag = ' --clean_recv 1 '

                        ds_flag = ' --ddio_ways '+ds+' '
                        if 'ideal' in ds:
                            ds_flag = ' '
                            base_cfg_name = ' l3fwd_ddio_ICL_IDEAL_DDIO.cfg '  

                        tmpcmd = batch_script_name+' --base_cfg '+base_cfg_name+\
                                ' --mem_controllers '+mc+' --forced_packet_size '+str(ps)+\
                                ' --recv_buf_pool_size '+str(rb_pool_size)+' --batchsize '+bs+ds_flag+cs_flag+\
                                ' --batch_dir '+output_path_base+str(ps)+'pack_'+str(rbc)+'recv_'+mc+'_batch'+bs+'_'+ds+'ways_'+cs+' --num_keys '+num_keys
                        
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
    
