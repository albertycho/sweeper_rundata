#!/usr/bin/env python3

import os
import sys
import csv
import math
import statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt 



home = '/nethome/acho/zsim/zSim'

ingress = ["ideal"]#,"mem","llc","llc"]
egress = ["ideal"]#,"mem","llc_inval","llc_non_inval"]

cumulative_st = []
cumulative_e2e = []
cumulative_qt = [] #queuetime
cumulative_hft = [] #herd functionality time
idx = 0

for k in range(len(ingress)):
    
    ingr = ingress[k]
    egr = egress[k]

    total = []

    #os.chdir(outdir+'/phase_length_sens/ingr_'+ingr+'_egr_'+egr+'/phase_len_10000')

    for d in os.listdir('.'):
        if 'timestamps_nic' in d:
            arr = []
            core_id = d.split('_')[3].split('.')[0]
            nic_file = open(d,'r')
            core_file = open("timestamps_core_"+core_id+".txt",'r')
            line = nic_file.readline()
            line = nic_file.readline()
            line = nic_file.readline()
            line = nic_file.readline()
            line = nic_file.readline()
            line1 = core_file.readline()
            line1 = core_file.readline()
            line1 = core_file.readline()
            line1 = core_file.readline()
            line1 = core_file.readline() #throw away first few lines
            for xx in range(1000):
                line = nic_file.readline()
                line1 = core_file.readline()
            previous_service_end = 0
            while line:
                ts_nic = []
                ts_core = []
                for i in line.split(':')[1].split(' '):
                    try: 
                        ts_nic.append(int(i))
                    except ValueError: 
                        pass
                for i in line1.split(':')[1].split(' '):
                    try: 
                        ts_core.append(int(i))
                    except ValueError: 
                        pass
                #assert(ts_nic[0] < ts_core[0])
                #assert(ts_core[2] < ts_nic[1])
                if (previous_service_end==0):
                    previous_service_end=ts_core[0]
                ##arr.append([ts_core[1]-ts_nic[0], ts_core[2]-ts_core[1], ts_core[3]-ts_core[2], ts_core[4]-ts_core[3], ts_nic[1]- ts_core[2], ts_nic[1]-ts_nic[0], ts_core[4]-ts_core[1], ts_core[1]-previous_service_end])
                arr.append([ts_core[0]-ts_nic[0], ts_core[1]-ts_core[0], ts_core[2]-ts_core[1], ts_core[3]-ts_core[2], ts_nic[1]- ts_core[1], ts_nic[1]-ts_nic[0], ts_core[3]-ts_core[0], ts_core[0]-previous_service_end])

                line = nic_file.readline()
                line1 = core_file.readline()
                previous_service_end = ts_core[3]
            nic_file.close()
            core_file.close()

            #total.append(['core '+core_id]+arr[0])

            os.system('rm latencies_core_'+core_id+'.csv')
            with open('latencies_core_'+core_id+'.csv','a') as csv_file: 
                write_csv = csv.writer(csv_file,  delimiter=',')  
                write_csv.writerow(['nic injection to server waking up','herd functionality','sending response (memcpy+enqueue)','dealloc buf','server starting send_response to nic finding an entry','nic end-to-end', 'service time','last_service_end to server pikcup'])
                for k in arr:
                    write_csv.writerow(k)

            
            for i in range(len(arr)):
                cumulative_st.append(arr[i][6])
                cumulative_e2e.append(arr[i][5])
                cumulative_qt.append(arr[i][0])
                cumulative_hft.append(arr[i][1])
            idx+=1
    '''
    os.system('rm latencies.csv')
    with open('latencies.csv','a') as csv_file: 
        write_csv = csv.writer(csv_file,  delimiter=',')  
        write_csv.writerow(['','nic injection to server waking up','herd functionality','sending response (memcpy+enqueue)','dealloc buf','server starting send_response to nic finding an entry','nic end-to-end', 'service time'])
        write_csv.writerows(total)
    '''
    '''
    create one .csv file
    '''

f_lat_all_core = open('latencies_all_cores.csv','w')
#f_lat_all_core.write('nic injection to server waking up,herd functionality,sending response (memcpy+enqueue),dealloc buf,server starting send_response to nic finding an entry,nic end-to-end,service time,phases\n')

f_lat_all_core.write('nic injection to server waking up,herd functionality,sending response (memcpy+enqueue),dealloc buf,server starting send_response to nic finding an entry,nic end-to-end,service time,last_service_end to server pikcup\n')
for dd in os.listdir('.'):
    if 'latencies_core' in dd:
        core_id = dd.split('_')[2].split('.')[0]
        #os.system('echo "'+core_id+'"')
        #os.system('echo "core_id '+core_id+'" >> latencies_all_cores.csv')
        f_lat_all_core.write("core "+core_id+",\n")
        f_lc = open(dd,'r') 
        line = f_lc.readline()
        line = f_lc.readline()
        line = f_lc.readline()
        line = f_lc.readline()
        line = f_lc.readline() #throw away first few lines
        while(line):
            f_lat_all_core.write(line)
            line = f_lc.readline()
        f_lc.close()

f_lat_all_core.close()

#avg_intervals=[]
#if 'latency_hist.txt' in os.listdir('.'):
#    f_lat_hist = open('latency_hist.txt','r')
#    #avg_interval_line = f_lat_hist.readline()
#    avg_interval_line = f_lat_hist.readline()
#    while avg_interval_line:
#        avg_intervals.append(avg_interval_line)
#        avg_interval_line=f_lat_hist.readline()
#
##y=np.array(cumulative_e2e)
#
f_stat_summary = open('stat_summary.txt','w')
#if 'latency_hist.txt' in os.listdir('.'):
#    #f_stat_summary.write(avg_interval_line)
#    for avg_interval_line_out in avg_intervals:
#        f_stat_summary.write(avg_interval_line_out)
#    f_lat_hist.close()


f_stat_summary.write("service_time: \n")
f_stat_summary.write("median: "+str(statistics.median(cumulative_st)) + "\n")
f_stat_summary.write("avg: "+str(sum(cumulative_st)/len(cumulative_st)) + "\n")
f_stat_summary.write("max: "+str(max(cumulative_st)) + "\n")
f_stat_summary.write("min: "+str(min(cumulative_st)) + "\n")

f_stat_summary.write("\ne2e_latency: \n")
f_stat_summary.write("median: "+str(statistics.median(cumulative_e2e)) + "\n")
f_stat_summary.write("avge2e: "+str(sum(cumulative_e2e)/len(cumulative_e2e)) + "\n")
f_stat_summary.write("max: "+str(max(cumulative_e2e)) + "\n")
f_stat_summary.write("min: "+str(min(cumulative_e2e)) + "\n")
f_stat_summary.write("90%: "+str(np.percentile(cumulative_e2e, 90)) +"\n")
f_stat_summary.write("95%: "+str(np.percentile(cumulative_e2e, 95)) +"\n")
f_stat_summary.write("99%: "+str(np.percentile(cumulative_e2e, 99)) +"\n")


f_stat_summary.write("\nqueueing_time: \n")
f_stat_summary.write("median: "+str(statistics.median(cumulative_qt)) + "\n")
f_stat_summary.write("avg: "+str(sum(cumulative_qt)/len(cumulative_qt)) + "\n")
f_stat_summary.write("max: "+str(max(cumulative_qt)) + "\n")
f_stat_summary.write("min: "+str(min(cumulative_qt)) + "\n")

f_stat_summary.close()

print("median: "+str(statistics.median(cumulative_st)))
print("avg: "+str(sum(cumulative_st)/len(cumulative_st)))
print("max: "+str(max(cumulative_st)))
print("min: "+str(min(cumulative_st)))
print(str(np.percentile(cumulative_e2e, 95)))

#st_hist, bin_edges = np.histogram(cumulative_st, bins=10)

#mybins = [1000,2000,3000,4000,5000,6000]
#plt.hist(cumulative_st, bins=mybins)
#plt.savefig('st_hist.png')

#plt.scatter(x,cumulative_st,color="blue")
#plt.scatter(x,cumulative_e2e,color="black")
#plt.plot(x,cumulative_st,color="blue", linewidth=0.1)

##comment this back in when using plot
#x = np.linspace(0, len(cumulative_st), len(cumulative_st))
#plt.plot(x,cumulative_e2e,color="black", linewidth=0.1)
#plt.plot(x,cumulative_hft,color="green", linewidth=0.1)
#plt.savefig('service_times.png',dpi=720)


