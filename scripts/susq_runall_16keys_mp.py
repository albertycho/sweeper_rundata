#!/usr/bin/env python

import os
import sys
from multiprocessing import Process                                             
from multiprocessing import Semaphore 

##############  1KB PACKETS  ##################

mcs = ['8','4'] 

q_depths = ['50','150','250','350','450']
#q_depths = ['50','150','200','250','300','350','400']
#q_depths = ['50','150','200','250']
#q_depths = ['300','350','400']
#rb_pool_sizes=['2097152','4194304']
rb_pool_sizes=['4194304']
out_dir_prefix='0419_TLD_16_keys_batch/'

#ddio_setups = ['2','11','cleans','cleans11','mem']
ddio_setups = ['2','12','clean','clean12']


home_base='/shared/acho44'


pcmds=[]
for mc in mcs:
    for qd in q_depths:
        for rbps in rb_pool_sizes:
            for ds in ddio_setups:
                #base_cfg = 'l3fwd_ddio_sustain_q_base_matmul_ICL.cfg'
                base_cfg = 'l3fwd_ddio_sustain_q_base_ICL.cfg'
                ds_flag = ' --ddio_ways '+ds+' '                           
                if 'clean' in ds:
                    ds_flag = ' --ddio_ways 2 --clean_recv 1 '
                if 'clean12' in ds:
                    ds_flag = ' --ddio_ways 12 --clean_recv 1 '
                if 'cleans' in ds:
                    ds_flag = ' --ddio_ways 2 --clean_recv 2 '
                if 'cleans12' in ds:
                    ds_flag = ' --ddio_ways 12 --clean_recv 2 '
                if 'mem' in ds:
                    ds_flag = ' --ddio_ways 2' ##doesn't even matter
                    base_cfg = 'l3fwd_mem_sustain_q_base_matmul_ICL.cfg'
                os.chdir(home_base)
                #outpath=out_dir_prefix+'susq_'+qd+'_'+rbps+'_'+ds
                outpath=out_dir_prefix+'susq_'+qd+'_4k_'+ds+'_'+mc
                rcmd= './set_IR_and_run.py  --base_cfg '+base_cfg+'  --mem_controllers '+mc+' --forced_packet_size 1024  --batchsize 32 --packet_count 500000  --num_keys 16  --recv_buf_pool_size '+rbps+' --q_depth '+qd+ds_flag+' --out_dir '+outpath
                #os.system(rcmd)
                pcmds.append(rcmd)
    
def f(fcmd, sema):                                                              
    print(fcmd)                                                                 
    os.system(fcmd)                                                             
    sema.release()                                                              
 


if __name__=='__main__':
    concurrency = 4
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
                                          


#os.system('./set_IR_and_run.py --printstd 1 --base_cfg  l3fwd_ddio_sustain_q_base.cfg --mem_controllers 6 --forced_packet_size 1024  --batchsize 32 --packet_count 500000  --num_keys 65536  --recv_buf_pool_size 2097152  --q_depth 200 --out_dir 0331_sustain_q_noNF1_base_5k_200qd ')
#
#os.system('killall -9 herd')                                                
#os.system('killall -9 l3fwd')                                               
#os.system('killall -9 simpNF')                                              
#os.system('killall -9 zsim')                                                
#os.system('killall -9 nic_egress_proxy_app')                                
#os.system('killall -9 nic_proxy_app')                                       
#os.system('killall -9 memhog_mt')                                           
#os.system('ipcrm -a')      
#
#os.system('./runall_master_mp_0329_SPLIT3_REMOVETHIS.py')

#f1=open('0324_l3fwd_colloc3runs_completed.txt','w')
#f1.write('runs finished\n')
#f1.close()



#####128KB rb###
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 6 --recv_buf_pool_size 131072 --batch_dir /shared/INDIE/512pack_256recv/ddio_var_mem_ctrl/6con/0215 ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 4 --recv_buf_pool_size 131072 --batch_dir 0208_DDR4_4con_124KRB_512BPkt ')
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 2 --recv_buf_pool_size 131072 --batch_dir 0208_DDR4_2con_124KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 1 --recv_buf_pool_size 131072 --batch_dir 0208_DDR4_1con_124KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_simplemem.cfg --mem_controllers 1 --recv_buf_pool_size 131072 --batch_dir 0208_DDR4_simpemem_124KRB_512BPkt ')
##
##
##
#####256KB rb###
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 6 --recv_buf_pool_size 262144 --batch_dir 0208_DDR4_6con_256KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 4 --recv_buf_pool_size 262144 --batch_dir 0208_DDR4_4con_256KRB_512BPkt ')
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 2 --recv_buf_pool_size 262144 --batch_dir 0208_DDR4_2con_256KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 1 --recv_buf_pool_size 262144 --batch_dir 0208_DDR4_1con_256KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_simplemem.cfg --mem_controllers 1 --recv_buf_pool_size 262144 --batch_dir 0208_DDR4_simpemem_256KRB_512BPkt ')
##
##
##
#####512KB rb###
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 6 --recv_buf_pool_size 524288 --batch_dir 0208_DDR4_6con_512KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 4 --recv_buf_pool_size 524288 --batch_dir 0208_DDR4_4con_512KRB_512BPkt ')
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 2 --recv_buf_pool_size 524288 --batch_dir 0208_DDR4_2con_512KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_DDR4_base.cfg --mem_controllers 1 --recv_buf_pool_size 524288 --batch_dir 0208_DDR4_1con_512KRB_512BPkt ')
##
##os.system(' ./batch_ddio_run_512.py --base_cfg ddio_simplemem.cfg --mem_controllers 1 --recv_buf_pool_size 524288 --batch_dir 0208_DDR4_simpemem_512KRB_512BPkt ')
##
##
####home = '/nethome/acho44/zsim/zSim'
####
####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_1119_md --out_dir_prefix 0 --base_cfg herd_base_DDR.cfg --ingress mem --egress mem --num_keys 8196')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
####
####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_1119_LLD --out_dir_prefix 0 --base_cfg herd_base_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_2W_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 2')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
######
######
####os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_4W_san_check --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 4')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
####
####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_6W_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 6')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
######
######
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_8W_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 8')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
####
####
#####os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_10W_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 10')
#####os.system('killall -9 herd')
#####os.system('killall -9 nic_proxy_app')
#####os.system('killall -9 nic_egress_proxy_app')
#####os.system('ipcrm -a')
#####
#####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_12W_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 12')
#####os.system('killall -9 herd')
#####os.system('killall -9 nic_proxy_app')
#####os.system('killall -9 nic_egress_proxy_app')
#####os.system('ipcrm -a')
####
####
#####os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_14W_1129_RERUN --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 14')
#####os.system('killall -9 herd')
#####os.system('killall -9 nic_proxy_app')
#####os.system('killall -9 nic_egress_proxy_app')
#####os.system('ipcrm -a')
####
####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_16W_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 16')
######os.system('killall -9 herd')
######os.system('killall -9 nic_proxy_app')
######os.system('killall -9 nic_egress_proxy_app')
######os.system('ipcrm -a')
####
####
#####os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_l2_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress l2 --egress mem --num_keys 8196 --ddio_ways 16')
#####os.system('killall -9 herd')
#####os.system('killall -9 nic_proxy_app')
#####os.system('killall -9 nic_egress_proxy_app')
#####os.system('ipcrm -a')
#####
#####
#####
######os.system('./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_l1_1129 --out_dir_prefix 0 --base_cfg herd_base_DDIO.cfg --ingress l1 --egress mem --num_keys 8196 --ddio_ways 16')
#####os.system('killall -9 herd')
#####os.system('killall -9 nic_proxy_app')
#####os.system('killall -9 nic_egress_proxy_app')
#####os.system('ipcrm -a')
#####
####
####
####
####
#####./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_8W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_32_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 8
####
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_32_10W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_32_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 10
########
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_32_12W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_32_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 12
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_32_14W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_32_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 14
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_32_16W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_32_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 16
########
########
########
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_128_10W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 10
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_128_12W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 12
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_128_14W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 14
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_128_16W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_DDR.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 16
########
########
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_ideal_10W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_ideal.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 10
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_ideal_12W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_ideal.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 12
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_ideal_14W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_ideal.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 14
########./multi_herd_run_wrapper.py --batch_dir BATCH_DDIO_ideal_16W_1212 --out_dir_prefix 0 --base_cfg herd_base_skew_128_ideal.cfg --ingress llc --egress llc_non_inval --num_keys 8196 --ddio_ways 16
