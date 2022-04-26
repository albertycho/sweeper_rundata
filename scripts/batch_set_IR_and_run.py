#!/usr/bin/env python

import os
import sys
import argparse

#args: 1 outdir 2 zsim_exec 3 base cfg file 4 num_server 5 phaseLength 
#      6 packet_injection_rate 7 packet_count 8 update fraction
#this script assumes process 2 will have herd and its params in the base cfg file

# this is your base zsim directory
home = '/nethome/acho44/zsim/zSim'

parser = argparse.ArgumentParser()
parser.add_argument('--batch_dir', type=str, default='batch_dir')
#parser.add_argument('--batch_dir', type=str, required=True)
parser.add_argument('--out_dir_prefix', type=str, default='0')

parser.add_argument('--exec_file', type=str, default='build/opt/zsim')
parser.add_argument('--base_cfg', type=str, default='ddio_base.cfg')
#parser.add_argument('--IR', type=str, default='10')

##parser.add_argument('--send_in_loop', type=str, default='false')
##parser.add_argument('--num_server', type=str, default='16')
##parser.add_argument('--num_keys', type=str, default='1024')
##parser.add_argument('--phaseLength', type=str, default='1000')
##parser.add_argument('--packet_injection_rate', type=str, default='10')
##parser.add_argument('--packet_count', type=str, default='1000000')
##parser.add_argument('--update_fraction', type=str, default='100')
##parser.add_argument('--pp_policy', type=str, default='0')
##parser.add_argument('--ingress', type=str, default='ideal')
##parser.add_argument('--egress', type=str, default='ideal')
##parser.add_argument('--ddio_ways', type=str, default='2')
args = parser.parse_args()

batch_dir = args.batch_dir
out_dir_prefix = args.out_dir_prefix
zsim_exec = args.exec_file
base_cfg = args.base_cfg
#IR = args.IR

# configurable param input:
##num_server = args.num_server
##phaseLength = args.phaseLength
##packet_injection_rate = args.packet_injection_rate
##packet_count = args.packet_count
##update_fraction = args.update_fraction
##pp_policy = args.pp_policy
##ingress = args.ingress
##egress = args.egress
##send_in_loop = args.send_in_loop
##num_keys=args.num_keys
##ddio_ways=args.ddio_ways

if os.path.isdir(batch_dir):
    print "batch_dir "+batch_dir+" already exists!\n"
    quit()

os.system('rm -rf '+batch_dir)
os.system('mkdir '+batch_dir)
os.chdir(batch_dir)
os.system('cp ../process_timestamps.py .')
os.system('cp ../get_tail_latencies_from_batch.py .')
os.system('cp ../process_zsim_out.py .')

#injection_rates = ["290","295","300","305","310","315","320","325"]


#for ir in injection_rates:
for ir in range(5,20,1):
    out_dir_name = out_dir_prefix+str(ir)
    os.system('../set_IR_and_run.py --out_dir '+out_dir_name+' --base_cfg '+base_cfg+' --IR '+str(ir))
#    os.system('../herd_run.py --out_dir '+out_dir_name+' --exec_file '+zsim_exec+' --base_cfg '+base_cfg+' --num_server '+num_server+' --phaseLength '+phaseLength+' --packet_injection_rate '+str(ir)+' --packet_count '+packet_count+' --update_fraction '+update_fraction+' --pp_policy '+pp_policy+ ' --send_in_loop '+send_in_loop+' --ingress '+ingress+' --egress '+egress+' --num_keys '+num_keys+' --ddio_ways '+ddio_ways)

#os.system('python3 get_tail_latencies_from_batch.py')
#os.chdir(home)
