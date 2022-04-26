#!/usr/bin/env python

import os
import sys
import argparse

#args: 1 outdir 2 zsim_exec 3 base cfg file 4 num_server 5 phaseLength 
#      6 packet_injection_rate 7 packet_count 8 update fraction
#this script assumes process 2 will have herd and its params in the base cfg file

# this is your base zsim directory
home = '/nethome/acho44/zsim/zSim'
script_dir = '/shared/acho44/'

parser = argparse.ArgumentParser()
parser.add_argument('--batch_dir', type=str, default='batch_dir')
parser.add_argument('--out_dir_prefix', type=str, default='0')

parser.add_argument('--exec_file', type=str, default='build/opt/zsim')
parser.add_argument('--base_cfg', type=str, default='ddio_DDR4_base.cfg')

##parser.add_argument('--send_in_loop', type=str, default='false')
##parser.add_argument('--num_server', type=str, default='16')
##parser.add_argument('--phaseLength', type=str, default='1000')
##parser.add_argument('--packet_injection_rate', type=str, default='10')
##parser.add_argument('--packet_count', type=str, default='1000000')
##parser.add_argument('--update_fraction', type=str, default='100')
##parser.add_argument('--pp_policy', type=str, default='0')
##parser.add_argument('--ingress', type=str, default='ideal')
##parser.add_argument('--egress', type=str, default='ideal')
parser.add_argument('--num_keys', type=str, default='1024')
parser.add_argument('--mem_controllers', type=str, default='6')
parser.add_argument('--forced_packet_size', type=str, default='1024')
parser.add_argument('--recv_buf_pool_size', type=str, default='524288')
parser.add_argument('--batchsize', type=str, default='0')

parser.add_argument('--ddio_ways', type=str, default='0')
parser.add_argument('--clean_recv', type=str, default='0')
parser.add_argument('--matN', type=str, default='0')
parser.add_argument('--xmem_w', type=str, default='0')

parser.add_argument('--printstd', type=str, default='0')



args = parser.parse_args()

batch_dir = args.batch_dir
out_dir_prefix = args.out_dir_prefix
zsim_exec = args.exec_file
base_cfg = args.base_cfg
num_keys=args.num_keys


mem_controllers=args.mem_controllers
forced_packet_size=args.forced_packet_size
recv_buf_pool_size=args.recv_buf_pool_size
batchsize=args.batchsize

ddio_ways=args.ddio_ways
clean_recv=args.clean_recv
matN = args.matN
xmem_w=args.xmem_w


printstd=args.printstd

if os.path.isdir(batch_dir):
    print "batch_dir "+batch_dir+" already exists!\n"
    quit()

os.system('rm -rf '+batch_dir)
os.system('mkdir '+batch_dir)
os.chdir(batch_dir)
os.system('cp '+script_dir+'process_timestamps.py .')
os.system('cp '+script_dir+'get_tail_latencies_from_batch.py .')
os.system('cp '+script_dir+'process_zsim_out.py .')
os.system('cp '+script_dir+'get_mem_lat.py .')
os.system('cp '+script_dir+'get_avg_mbw.py .')
os.system('cp '+script_dir+'set_IR_and_run.py .')

flag = 50;

#single_run : launch a single run with given IR, with given config
def single_run(ir): 
    out_dir_name = out_dir_prefix+str(ir)
    os.system('./set_IR_and_run.py --out_dir '+out_dir_name+' --base_cfg '+base_cfg+' --IR '+str(ir)+' --mem_controllers '+mem_controllers+' --recv_buf_pool_size '+recv_buf_pool_size+' --num_keys '+num_keys+' --forced_packet_size '+forced_packet_size+' --batchsize '+batchsize+' --ddio_ways '+ddio_ways+' --clean_recv '+clean_recv+' --printstd '+printstd +'  --matN '+matN+' --xmem_w '+xmem_w)


#if os.path.isfile(target_path):  
#if os.path.isdir(target_path):

def get_run_res(ir):
    runres = 2 #0: fail, 1: success, 2: crash/bad_run
    out_dir_name = out_dir_prefix+str(ir)
    if os.path.isdir(out_dir_name): #if exists out_dir_name path:
        if os.path.isfile(out_dir_name +'/run_success' ):  #if exists file run_success:
            return 1
        else:
            if os.path.isfile(out_dir_name +'/res.txt' ): #if exists res.txt
                #readline, while line, if 'OUT OF RECV BUFFER' in line: runres=1
                fres=open(out_dir_name+'/res.txt', 'r')
                line=fres.readline()
                while line:
                    if 'OUT OF RECV BUFFER' in line:
                        runres=0
                    if 'THIS RUN HAD SPILLOVER' in line:
                        runres=0
                    line=fres.readline()
            else:
                print(batch_dir+' at IR '+ir+': res.txt does not exist!')
    else:
        print(batch_dir+' at IR '+ir+': test dir does not exist!')

    return runres


print('batch_dir path: '+batch_dir)

#power of 2 makes things smoother. Assuming we won't go over 64 IR
ir=32
hop=ir
flag =0
last_runres=0
runres=2
crash_count=0
do_second_loop = False


while (hop>0):
    hop=hop/2
    last_runres=runres
    print((str(ir)))    
    out_dir_name = out_dir_prefix+str(ir)
    single_run(ir)
    runres = get_run_res(ir)
    print('runres returned '+str(runres))
    if runres==0:
        print('fail, '+batch_dir+out_dir_name)
        if(ir==16):
            do_second_loop = True
            break;
        ir=ir-hop
        crash_count=0
    elif runres==1:
        print('success, '+batch_dir+out_dir_name)
        ir=ir+hop
        crash_count=0
    elif runres==2: #simulation died. rerun
        print('crash, '+batch_dir+out_dir_name)
        #os.system('killall -9 herd')
        #os.system('killall -9 l3fwd')
        #os.system('killall -9 zsim')
        #os.system('killall -9 nic_egress_proxy_app')
        #os.system('killall -9 nic_proxy_app')
        #os.system('ipcrm -a')
        os.system('mv '+out_dir_name+' '+out_dir_name+'_crash'+str(crash_count))
        #os.system('rm -r '+out_dir_name)
        #### ipcrm and killalls
        crash_count=crash_count+1
        if(crash_count<5):
            hop=hop*2
            if(hop==0): #corner case where last run crashes
                hop=1
        else: #crashed 5 times, treat as failure
            print('crashed 5 times')
            if(ir==16):
                do_second_loop = True
                break;
            ir=ir-hop
            crash_count=0

if(do_second_loop):
    ir=16
    hop=1
    flag =0
    last_runres=0
    runres=2
    crash_count=0
    
    while (ir>0):
        last_runres=runres
        print((str(ir)))    
        out_dir_name = out_dir_prefix+str(ir)
        single_run(ir)
        runres = get_run_res(ir)
        print('runres returned '+str(runres))
        if runres==0:
            print('fail, '+batch_dir+out_dir_name)
            ir=ir-hop
            crash_count=0
        elif runres==1:
            print('success, '+batch_dir+out_dir_name)
            break;
        elif runres==2: #simulation died. rerun
            print('crash, '+batch_dir+out_dir_name)
            os.system('mv '+out_dir_name+' '+out_dir_name+'_crash'+str(crash_count))
            crash_count=crash_count+1
            if(crash_count<5):
                if(hop==0): #corner case where last run crashes
                    hop=1
            else: #crashed 5 times, treat as failure
                print('crashed 5 times')
                ir=ir-hop
                crash_count=0
    


print('batch_run done at: '+batch_dir)
fdone=open('batch_run_done.txt', 'w')
fdone.write('batch_run_done')
fdone.close()


###for ir in range(15,30,1):
##for ir in range(10,9,-1):
##    print((str(ir)))
##    out_dir_name = out_dir_prefix+str(ir)
##    single_run(ir)
##    runres = get_run_res(ir)
##    print('runres returned '+str(runres))
##
##    flag = flag -1
##    if flag==0 :
##        break;
##    if 'run_success' in os.listdir(out_dir_name):
##        if(flag>2):
##            flag=2 #do 2 more runs after success




#os.system('python3 get_tail_latencies_from_batch.py')
#os.chdir(home)
