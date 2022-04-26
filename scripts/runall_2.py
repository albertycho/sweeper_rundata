#!/usr/bin/env python

import os
import sys


##############  1KB PACKETS  ##################


os.system('./runall_master_mp.py')

os.system('killall -9 herd')                                                
os.system('killall -9 l3fwd')                                               
os.system('killall -9 simpNF')                                              
os.system('killall -9 zsim')                                                
os.system('killall -9 nic_egress_proxy_app')                                
os.system('killall -9 nic_proxy_app')                                       
os.system('killall -9 memhog_mt')                                           
os.system('ipcrm -a')      

os.system('./runall_master_mp_0329_SPLIT3_REMOVETHIS.py')

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
