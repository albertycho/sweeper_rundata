#!/usr/bin/env python

import os
import sys
import argparse

#args: 1 outdir 2 zsim_exec 3 base cfg file 4 num_server 5 phaseLength 
#      6 packet_injection_rate 7 packet_count 8 update fraction
#this script assumes process 2 will have herd and its params in the base cfg file

# this is your base zsim directory
home = '/nethome/acho44/zsim/zSim'
#home = '/nethome/acho44/zsim/1027_zSim'
herd_1024_path = '/nethome/acho44/zsim/herd-sonuma-zsim/build/herd'
herd_512_path = '/nethome/acho44/zsim/herd-sonuma-zsim/build_512/herd'
xmem_path = '/nethome/acho44/zsim/X-Mem/bin/xmem-linux-x64'

# parse cmd args
parser = argparse.ArgumentParser()
parser.add_argument('--out_dir', type=str, default='out_dir')
parser.add_argument('--exec_file', type=str, default='build/opt/zsim')
#parser.add_argument('--base_cfg', type=str, default='ddio_base.cfg')
parser.add_argument('--base_cfg', type=str, required=True)


parser.add_argument('--IR', type=str, default='10')

#parser.add_argument('--send_in_loop', type=str, default='false')
#parser.add_argument('--num_server', type=str, default='16')
#parser.add_argument('--num_keys', type=str, default='1024')
#parser.add_argument('--phaseLength', type=str, default='1000')
#parser.add_argument('--packet_injection_rate', type=str, default='10')
#parser.add_argument('--packet_count', type=str, default='200000')
#parser.add_argument('--update_fraction', type=str, default='20')
#parser.add_argument('--ingress', type=str, default='llc')
#parser.add_argument('--egress', type=str, default='llc_non_inval')
parser.add_argument('--mem_controllers', type=str, default='6')
parser.add_argument('--forced_packet_size', type=str, default='0')
parser.add_argument('--recv_buf_pool_size', type=str, default='524288')
#parser.add_argument('--ddio_ways', type=str, default='2')
##parser.add_argument('--xmem_dsize', type=str, default='1024')
args = parser.parse_args()



# 1st input: the output directory you want the run to take place + store results
#outdir = sys.argv[1] 
outdir = args.out_dir
os.system('rm -rf '+outdir)
os.system('mkdir '+outdir)
os.chdir(outdir)


# 2nd input: the zsim executable to use
#zsim_exec = sys.argv[2]
zsim_exec = args.exec_file
os.system ('cp '+home+'/'+zsim_exec+' .')

# 3rd input: the base config file (assuming it's in the tests folder)
#confile = sys.argv[3]
confile = args.base_cfg
os.system('cp '+home+'/tests/'+confile+' .')

#### copy executables known to be needed
os.system('cp '+home+'/tests/nic_proxy_app .')
os.system('cp '+home+'/tests/nic_egress_proxy_app .')
#os.system('cp '+herd_path+' .')
os.system('cp '+xmem_path+' .')


# configurable param input:
#num_server = args.num_server
#phaseLength = args.phaseLength
#IR = args.IR
#packet_count = args.packet_count
#update_fraction = args.update_fraction
#ingr = args.ingress
#egr = args.egress
#send_in_loop = args.send_in_loop
#num_keys=args.num_keys
#mem_controllers=args.mem_controllers
#forced_packet_size=args.forced_packet_size
#recv_buf_pool_size=args.recv_buf_pool_size
#ddio_ways=args.ddio_ways
##xmem_dsize = args.xmem_dsize

# create params.txt in outdir to record input params to this run/dir
#fpar = open('params.txt', 'w')
#fpar.write('num_server ='+num_server+'\n')
#fpar.write('phaseLength ='+phaseLength+'\n')
#fpar.write('packet_injection_rate ='+packet_injection_rate+'\n')
#fpar.write('packet_count ='+packet_count+'\n')
#fpar.close()


herd_path = herd_512_path

# create the new config file
f1 = open(confile)
f2 = open('conf.cfg','w')
line = f1.readline()
while line:
	##if 'num_server' in line:
	##	tmp = line.split('=')[0]
	##	f2.write(tmp+'= '+num_server+';\n')
	##elif 'phaseLength' in line:
	##	tmp = line.split('=')[0]
	##	f2.write(tmp+'= '+phaseLength+';\n')
        #if 'packet_injection_rate' in line:
	#	tmp = line.split('=')[0]
	#	f2.write(tmp+'= '+IR+';\n')
        #elif 'controllers =' in line:
	#	tmp = line.split('=')[0]
	#	f2.write(tmp+'= '+mem_controllers+';\n')
        #elif 'networkFile' in line:
	#	tmp = line.split('network.conf')
	#	f2.write(tmp[0]+'network_'+mem_controllers+'.conf'+tmp[1])
        if 'forced_packet_size' in line:
		tmp = line.split('=')[0]
                if '1024' in line:
                    herd_path=herd_1024_path
        #elif 'recv_buf_pool_size' in line:
	#	tmp = line.split('=')[0]
	#	f2.write(tmp+'= '+recv_buf_pool_size+';\n')
        #elif 'num_keys' in line:
        #        tmp=line.split('=')[0]
        #        f2.write(tmp+'= '+num_keys+';\n')
        #elif '--num-keys' in line:
        #        tmp=line.split(' ')[0]
        #        f2.write(tmp+' '+num_keys+' \\\n')

	#else:
	f2.write(line)
	line = f1.readline()
f1.close()
f2.close()


os.system('cp '+herd_path+' .')

# launch the run, redirectung stdin and stderr to log files 
os.system('./zsim conf.cfg')
#os.system('./zsim conf.cfg 1> res.txt 2>app.txt &')
#os.system('./zsim conf.cfg 1> res.txt 2>app.txt')
os.system('ipcrm -a')
#os.system('./zsim conf.cfg 1> res.txt 2>app.txt')
#os.system('python3 ../process_zsim_out.py')
#os.system('python3 ../process_timestamps.py')
#os.system('../process_skew.py')
os.system('cd ..')
