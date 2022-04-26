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
l3fwd_path = '/nethome/acho44/zsim/my_l3fwd/build/l3fwd'
simpNF_path = '/nethome/acho44/zsim/simpleNF/build/simpNF'


# parse cmd args
parser = argparse.ArgumentParser()
parser.add_argument('--out_dir', type=str, default='out_dir')
parser.add_argument('--exec_file', type=str, default='build/opt/zsim')
parser.add_argument('--base_cfg', type=str, default='ddio_base.cfg')
parser.add_argument('--printstd', type=str, default='0')

parser.add_argument('--IR', type=str, default='0')

parser.add_argument('--num_keys', type=str, default='0')
parser.add_argument('--packet_count', type=str, default='0')
parser.add_argument('--mem_controllers', type=str, default='6')
parser.add_argument('--forced_packet_size', type=str, default='1024')
parser.add_argument('--recv_buf_pool_size', type=str, default='524288')
parser.add_argument('--batchsize', type=str, default='0') # if not given, don't change
parser.add_argument('--ddio_ways', type=str, default='0')
parser.add_argument('--clean_recv', type=str, default='0')
parser.add_argument('--q_depth', type=str, default='0')
parser.add_argument('--matN', type=str, default='0')
parser.add_argument('--xmem_w', type=str, default='0')
##parser.add_argument('--xmem_dsize', type=str, default='1024')
args = parser.parse_args()


#parser.add_argument('--send_in_loop', type=str, default='false')
#parser.add_argument('--num_server', type=str, default='16')
#parser.add_argument('--phaseLength', type=str, default='1000')
#parser.add_argument('--update_fraction', type=str, default='20')
#parser.add_argument('--ingress', type=str, default='llc')
#parser.add_argument('--egress', type=str, default='llc_non_inval')

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
os.system('cp '+home+'/tests/memhog .')
os.system('cp '+home+'/tests/memhog_mt .')
os.system('cp '+home+'/tests/matmul .')
os.system('cp '+home+'/tests/mm .')
os.system('cp '+home+'/tests/tiled_matmul .')
os.system('cp '+l3fwd_path+' .')
os.system('cp '+simpNF_path+' .')
os.system('cp '+xmem_path+' .')


# configurable param input:
#num_server = args.num_server
#phaseLength = args.phaseLength
set_IR=True
IR = args.IR
if(IR=='0'):
    set_IR=False

set_packet_count=True
packet_count = args.packet_count
if(packet_count=='0'):
    set_packet_count=False
#update_fraction = args.update_fraction
#ingr = args.ingress
#egr = args.egress
#send_in_loop = args.send_in_loop
set_num_keys=True
num_keys=args.num_keys
if(num_keys=='0'):
    set_num_keys=False

mem_controllers=args.mem_controllers
is_ideal_IO = False
is_simplemem = False
if('ideal' in mem_controllers):
    is_ideal_IO = True
    mem_controllers = '6'
if('simplemem' in mem_controllers):
    is_simplemem = True
    mem_controllers = '6' #doesn't really matter as long as there is some value

forced_packet_size=args.forced_packet_size
recv_buf_pool_size=args.recv_buf_pool_size
setbatchsize=True
batchsize=args.batchsize
if(batchsize=='0'):
    setbatchsize=False

ddio_ways=args.ddio_ways
set_ddio_ways=True
if(ddio_ways=='0'):
    set_ddio_ways=False

clean_recv=args.clean_recv

q_depth=args.q_depth
set_q_depth=True
if(q_depth=='0'):
    set_q_depth=False

matN=args.matN
set_matN=True
if(matN=='0'):
    set_matN=False

xmem_w=args.xmem_w
set_xmem_w=True
if(xmem_w=='0'):
    set_xmem_w=False

printstd=args.printstd


herd_path = herd_1024_path
if '512' in forced_packet_size:
    herd_path = herd_512_path


os.system('cp '+herd_path+' .')

# create params.txt in outdir to record input params to this run/dir
#fpar = open('params.txt', 'w')
#fpar.write('num_server ='+num_server+'\n')
#fpar.write('phaseLength ='+phaseLength+'\n')
#fpar.write('packet_injection_rate ='+packet_injection_rate+'\n')
#fpar.write('packet_count ='+packet_count+'\n')
#fpar.close()


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
        if(is_ideal_IO):
            if 'ingress =' in line:
                tmp = line.split('=')[0]
                f2.write(tmp+'= '+'"ideal"'+';\n')
                line=f1.readline()
                continue
            if 'egress =' in line:
                tmp = line.split('=')[0]
		f2.write(tmp+'= '+'"ideal"'+';\n')
                line=f1.readline()
                continue
        if(is_simplemem):
            if 'type = "DDR"' in line:
                tmp = line.split('=')[0]
		f2.write(tmp+'= '+'"Simple"'+';\n')
                line=f1.readline()
                continue
            if 'tech' in line:
                # don't write anything
                f2.write('//tech=notech for ideal\n')
                line=f1.readline()
                continue
        if 'packet_injection_rate' in line:
            if(set_IR):
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+IR+';\n')
            else:
                f2.write(line)
        elif 'controllers' in line:
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+mem_controllers+';\n')
        elif 'ddio_ways' in line:
            if(set_ddio_ways):
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+ddio_ways+';\n')
            else:
                f2.write(line)
        elif 'clean_recv' in line:
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+clean_recv+';\n')
        elif 'packet_count' in line:
            if(set_packet_count):
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+packet_count+';\n')
            else:
                f2.write(line)
        
        elif 'mat_N' in line:
            if(set_matN):
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+matN+';\n')
            else:
                f2.write(line)

        elif 'mlen' in line:
            if(set_matN):
		tmp = line.split('--mlen')[0]
		f2.write(tmp+' --mlen  '+matN+' \\\n')
            else:
                f2.write(line)
        
        elif '-w' in line:
            if(set_xmem_w):
		tmp = line.split('-w')[0]
		f2.write(tmp+' -w'+xmem_w+' \\\n')
            else:
                f2.write(line)



        elif 'networkFile' in line:
		tmp = line.split('network.conf')
		f2.write(tmp[0]+'network_'+mem_controllers+'.conf'+tmp[1])
        elif 'forced_packet_size' in line:
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+forced_packet_size+';\n')
        elif '--packet-size' in line:
		tmp = line.split(' ')[0]
		f2.write(tmp+' '+forced_packet_size+' \\\n')
        elif '--batchsize' in line:
            if(setbatchsize):
		tmp = line.split(' ')[0]
		f2.write(tmp+' '+batchsize+' \\\n')
            else:
                f2.write(line)
        elif 'recv_buf_pool_size' in line:
		tmp = line.split('=')[0]
		f2.write(tmp+'= '+recv_buf_pool_size+';\n')
        
        elif 'q_depth' in line:
            if(set_q_depth):
                tmp=line.split('=')[0]
                f2.write(tmp+'= '+q_depth+';\n')
            else:
                f2.write(line)

        elif 'num_keys' in line:
            if(set_num_keys):
                tmp=line.split('=')[0]
                f2.write(tmp+'= '+num_keys+';\n')
            else:
                f2.write(line)
        elif '--num-keys' in line:
            if(set_num_keys):
                tmp=line.split(' ')[0]
                f2.write(tmp+' '+num_keys+' \\\n')
            else:
                f2.write(line)
	else:
		f2.write(line)
	line = f1.readline()
f1.close()
f2.close()

# launch the run, redirectung stdin and stderr to log files 

#os.system('./zsim conf.cfg 1> res.txt 2>app.txt &')
if '1' in printstd:
    os.system('timeout 30m ./zsim conf.cfg')
else:
    os.system('timeout 30m ./zsim conf.cfg 1> res.txt 2>app.txt')
#os.system('ipcrm -a')
#os.system('./zsim conf.cfg 1> res.txt 2>app.txt')
#os.system('python3 ../process_zsim_out.py')
#os.system('python3 ../process_timestamps.py')
#os.system('../process_skew.py')
os.system('cd ..')
