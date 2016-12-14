#!/usr/bin/env python
""" Script to simulate creation of fast5 fie in the output path."""
import os
import sys
import pandas as pd
import time
import shutil


if len(sys.argv) != 3:
    print("Usage: move_fast5.py times.csv target_dir")
    sys.exit()

time_file = sys.argv[1]
output_path = sys.argv[2]

# Read the time file generated with poretools time.
times = pd.read_csv(time_file, sep='\t')
#times = pd.read_csv(time_file, sep='\t', names=["channel", "filename", "readLength", "expStartTime", "readStartTime", "duration", "readEndTime", "isoTime", "day", "hour", "minute"], header = None)

# Calculate when the read is completed in seconds after the experiment started.
times["moveTimes"] = times["unix_timestamp_end"] - min(times["exp_starttime"])

# Sort the data frame, beginning with the smallest moveTime
times = times.sort_values(["moveTimes"])
# Create a list with all filenames in the dataframe
path = list(times['filename'])

# Wait until each read is completed, then move it to the output_path
prev_time = 0
print("Start copying files to " + output_path)
for i, next_time in enumerate(list(times['moveTimes'])):
    move_time = next_time - prev_time
    time.sleep(move_time)
    print('Copy ' + str(path[i]))
    shutil.copy(path[i], output_path)
    prev_time = move_time
