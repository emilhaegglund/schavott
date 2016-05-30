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
import pyfasta
# Start scaffolding.py
# os.makedirs('data')
# args =  ['./scaffolding.py', '--scaffolder', 'sspace', '--watch', '/scratch/emihag/master-thesis/scripts/nanopore_scaffolding/data/', '--short_reads', '/scratch/emihag/data/references/FSC771/FSC771_MP.fna', '--run_mode', 'reads', '--intensity', '100', '--stop', '1', '--output', 'test', '--genome_size', '1800000']
# print('Args')
# print(args)
# subprocess.Popen(args)
# df = pd.read_csv('/mnt/walt_scratch_temp/emihag/data/raw/K2000295_FSC771_mkI_R73_20160317/downloads/times.csv',
#                 sep="\t")
# df = df.sort_values(by='unix_timestamp_end')
# min_time = df['unix_timestamp_end'].min()
# df['time'] = df['unix_timestamp_end'] - min_time
# print(df['filename'])
# time_list = df['time'].tolist()
# file_list = df['filename'].tolist()
# print(file_list[0:15])
# prev_time = 0
# for i in range(len(time_list)):
#     cur_time = time_list[i]
#     time_diff = cur_time - prev_time
#     prev_time = time_list[i]
#     time_list[i] = time_diff


from_path = '/mnt/powervault/emihag/2016_schavott/FSC771/'
orig_fasta = 'np_reads.fasta'
to_path = '/scratch/emihag/schavott/data/'
# files = os.listdir(from_path)
reads = pyfasta.Fasta(from_path + orig_fasta)


# random.shuffle(files)
counter = 1
for read in reads:
    # time.sleep(0.1)
#     if header_list[4] == 'twodirections:seq':
        counter += 1
        fasta_path = from_path + read.split(" ")[1] + ".fasta"
#         print(fasta_path)
        with open(fasta_path, 'w') as fasta_file:
            fasta_header = '>' + read + '\n'
            fasta_file.write(fasta_header)
            fasta_file.write(reads[read][:] + '\n')


        print("Copy file: " + str(counter))
        shutil.copyfile(fasta_path, to_path + read.split(" ")[1] + ".fasta")


# shutil.rmtree('data')
# If scaffolding is completed, remove all files from tmp directory and
# start over. Store the number of reads required to geta scaffold in the right
# genome size.

# files = os.listdir(from_path)
# # random.shuffle(files)
# counter = 1
# for fasta in files:
#     # if not os.path.isfile('/tmp/scaffolding.pid'):
#     #     break
#     # time.sleep(0.1)
#     if fasta.endswith("fasta"):
#         print('Copy file: ' + str(fasta))
#         print(to_path + fasta)
#         shutil.copyfile(from_path+fasta, to_path + fasta)
#         counter += 1