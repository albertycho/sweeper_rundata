#!/usr/bin/env python

import os
import sys




##############  512B PACKETS  ##################

####128KB rb###
#os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 6 --recv_buf_pool_size 131072 --batch_dir /shared/acho44/0226_l3fwd/512pack_256recv/ddio_var_mem_ctrl/6mc/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 2 --recv_buf_pool_size 131072 --batch_dir /shared/acho44/0226_l3fwd/512pack_256recv/ddio_var_mem_ctrl/2mc/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 3 --recv_buf_pool_size 131072 --batch_dir /shared/acho44/0226_l3fwd/512pack_256recv/ddio_var_mem_ctrl/3mc/0307_batch_test ')
##
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_simplemem.cfg --mem_controllers 3 --recv_buf_pool_size 131072 --batch_dir /shared/acho44/0226_l3fwd/512pack_256recv/ddio_var_mem_ctrl/simplemem/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ideal.cfg --mem_controllers 6 --recv_buf_pool_size 131072 --batch_dir /shared/acho44/0226_l3fwd/512pack_256recv/ddio_var_mem_ctrl/ideal/0307_batch_test ')
##
##
#####256KB rb###

os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 6 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/512pack_512recv/ddio_var_mem_ctrl/6mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 2 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/512pack_512recv/ddio_var_mem_ctrl/2mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 3 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/512pack_512recv/ddio_var_mem_ctrl/3mc/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_simplemem.cfg --mem_controllers 3 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/512pack_512recv/ddio_var_mem_ctrl/simplemem/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ideal.cfg --mem_controllers 6 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/512pack_512recv/ddio_var_mem_ctrl/ideal/0307_batch_test ')

###512KB rb###

os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 6 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/512pack_1024recv/ddio_var_mem_ctrl/6mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 2 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/512pack_1024recv/ddio_var_mem_ctrl/2mc/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 3 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/512pack_1024recv/ddio_var_mem_ctrl/3mc/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_simplemem.cfg --mem_controllers 2 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/512pack_1024recv/ddio_var_mem_ctrl/simplemem/0307_batch_test ')
os.system(' ./batch_ddio_run.py --forced_packet_size 512  --batchsize 4 --base_cfg l3fwd_ideal.cfg --mem_controllers 6 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/512pack_1024recv/ddio_var_mem_ctrl/ideal/0307_batch_test ')

##############  1KB PACKETS  ##################
#1MB rb###
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 6 --recv_buf_pool_size 1048576 --batch_dir /shared/acho44/0226_l3fwd/1024pack_1024recv/ddio_var_mem_ctrl/6mc/0307_batch_test ')
#/shared/acho44/0226_l3fwd/1024pack_1024recv/ddio_var_mem_ctrl/6mc/0307_batch_test

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 2 --recv_buf_pool_size 1048576 --batch_dir /shared/acho44/0226_l3fwd/1024pack_1024recv/ddio_var_mem_ctrl/2mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 3 --recv_buf_pool_size 1048576 --batch_dir /shared/acho44/0226_l3fwd/1024pack_1024recv/ddio_var_mem_ctrl/3mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_simplemem.cfg --mem_controllers 3 --recv_buf_pool_size 1048576 --batch_dir /shared/acho44/0226_l3fwd/1024pack_1024recv/ddio_var_mem_ctrl/simplemem/0307_batch_test')
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ideal.cfg --mem_controllers 6 --recv_buf_pool_size 1048576 --batch_dir /shared/acho44/0226_l3fwd/1024pack_1024recv/ddio_var_mem_ctrl/ideal/0307_batch_test')
#

###512KB rb###
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 6 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/1024pack_512recv/ddio_var_mem_ctrl/6mc/0307_batch_test ')

#os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 4 --recv_buf_pool_size 524288 --batch_dir 0307_batch_test_4con_512KRB_1KBPkt ')
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 2 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/1024pack_512recv/ddio_var_mem_ctrl/2mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 3 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/1024pack_512recv/ddio_var_mem_ctrl/3mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_simplemem.cfg --mem_controllers 3 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/1024pack_512recv/ddio_var_mem_ctrl/simplemem/0307_batch_test ')
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ideal.cfg --mem_controllers 6 --recv_buf_pool_size 524288 --batch_dir /shared/acho44/0226_l3fwd/1024pack_512recv/ddio_var_mem_ctrl/ideal/0307_batch_test ')


##
##
###
###256KB rb###
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 6 --recv_buf_pool_size 262144 --batch_dir  /shared/acho44/0226_l3fwd/1024pack_256recv/ddio_var_mem_ctrl/6mc/0307_batch_test')

#os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 4 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/1024pack_256recv/ddio_var_mem_ctrl/4con/0307_batch_test ')
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 2 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/1024pack_256recv/ddio_var_mem_ctrl/2mc/0307_batch_test')

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ddio_batch.cfg --mem_controllers 3 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/1024pack_256recv/ddio_var_mem_ctrl/3mc/0307_batch_test ')

os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_simplemem.cfg --mem_controllers 3 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/1024pack_256recv/ddio_var_mem_ctrl/simplemem/0307_batch_test ')
os.system(' ./batch_ddio_run.py --batchsize 4 --base_cfg l3fwd_ideal.cfg --mem_controllers 6 --recv_buf_pool_size 262144 --batch_dir /shared/acho44/0226_l3fwd/1024pack_256recv/ddio_var_mem_ctrl/ideal/0307_batch_test ')
##
