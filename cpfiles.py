# This is a test program for scaffolding py

# Create a test directory

# Start scaffolding.py script

# Copy fast5 files from specified directory to
# test directory
# If possible copy the files with 5 sec margin

# Move the created files from links

# When script finished tear down test directory

import os
import time
import datetime
import random
import shutil
import subprocess
import pandas as pd
# Start scaffolding.py
# os.makedirs('data')
# args =  ['./scaffolding.py', '--scaffolder', 'sspace', '--watch', '/scratch/emihag/master-thesis/scripts/nanopore_scaffolding/data/', '--short_reads', '/scratch/emihag/data/references/FSC771/FSC771_MP.fna', '--run_mode', 'reads', '--intensity', '100', '--stop', '1', '--output', 'test', '--genome_size', '1800000']
# print('Args')
# print(args)
# subprocess.Popen(args)
df = pd.read_csv('/scratch/emihag/data/raw/K2000295_FSC771_mkI_R73_20160317/downloads/times.csv',
                sep="\t")
df = df.sort_values(by='unix_timestamp_end')
min_time = df['unix_timestamp_end'].min()
df['time'] = df['unix_timestamp_end'] - min_time
print(df['filename'])
time_list = df['time'].tolist()
file_list = df['filename'].tolist()
print(file_list[0:15])
prev_time = 0
for i in range(len(time_list)):
    cur_time = time_list[i]
    time_diff = cur_time - prev_time
    prev_time = time_list[i]
    time_list[i] = time_diff


from_path = '/scratch/emihag/data/raw/K2000295_FSC771_mkI_R73_20160317/downloads/'
to_path = '/scratch/emihag/master-thesis/scripts/nanopore_scaffolding/data/'
files = os.listdir(from_path)
# random.shuffle(files)
counter = 1
for i, fast5 in enumerate(file_list):
    # if not os.path.isfile('/tmp/scaffolding.pid'):
    #     break
    time.sleep(0.1)
    if fast5.endswith("fast5"):
        print('Copy file: ' + str(fast5))
        shutil.copyfile(from_path+fast5, to_path + fast5[4:])
        counter += 1
# shutil.rmtree('data')
# If scaffolding is completed, remove all files from tmp directory and
# start over. Store the number of reads required to geta scaffold in the right
# genome size.