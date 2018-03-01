#!/usr/bin/env python
""" Simulation script for the creation of fastq files based on nanopore reads."""

import os
import sys
import time
import random
import time
from datetime import datetime
import argparse

"""Parse command line arguments.
"""
parser = argparse.ArgumentParser(description='Simulate reads released from nanopore\
                                              in real time')
parser.add_argument("source_dir", help="Path do directory with nanopore reads")
parser.add_argument("run_dir", help="Path to the schavott run directory")
parser.add_argument("start_time", help="Add the start time of the experiment")
parser.add_argument('-s','--speed', default=False, choices=["real-time", "fast-forward", "super-sonic"])
parser.add_argument('--force', action='store_true',help="Clear working directory if not empty!" )
parser.add_argument('--debug', action='store_true', help="This automatically at 100 reads for debugging")

args = parser.parse_args()

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

unique_sequence = uniqueid()
# Read the time stamps in the header of the fastq files.

###
if os.path.isdir(args.source_dir):
    files = os.listdir(args.source_dir)
    if len(files) == 0:
        exit("No files found in directory")
else:
    exit("Error, the source directory is not a directory!")

if not os.path.isdir(args.run_dir):
    os.mkdir(args.run_dir)
else:
    files = os.listdir(args.run_dir)
    if args.force:
        print(str(len(files))+" files in run directory will be removed.")
        for f in files:
            os.remove(os.path.join(args.run_dir,f))
        #os.system()
    elif len(files) > 0:
        exit("Error, the target directory is not empty!")

def write_fast_file(data,filetype):
    _id = next(unique_sequence)
    _file = str(_id) + "." + filetype
    with open(args.run_dir+"/"+_file,"w") as wf:
        wf.write(data)
    return

def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if len(lines[index]):
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment

def parse_time(header):
    '''The new files have their timestamp in the header of the read, parse the header and return the timestamp'''
    time_str = header.strip().split("start_time=")[-1].split("Z")[0]
    _time = float(time.mktime(time.strptime(time_str, '%Y-%m-%dT%H:%M:%S')))
    return _time

def simulate_reads(_file):
    timeindex = 0
    lines = []
    rvFile = reverse_readline(_file)
    line = next(rvFile)
    while line:
        if line.startswith(">") or line.startswith("@"):
            if line.startswith("@"):
                filetype = "fastq"
                quality = lines.pop(0)+"\n"
                sep = lines.pop(0)+"\n"
                data = sep+quality
            elif line.startswith(">"):
                filetype = "fasta"
            sequence = lines.pop(0)+"\n"
            data = line+"\n"+sequence + data

            _time = parse_time(line)
            if timeindex == 0:
                starttime = _time
            _time -= starttime
            if True:
                _time = abs(_time)
            if args.speed == "fast-forward":
                _time = int(_time*0.1)
            if args.speed == "super-sonic":
                _time = 0.1
            timeindex += 1
            if _time < 0:
                exit("Error time value is less than 0")
            if _time > 3600:
                print("Warning: next timestamp is more than one hour away, you may want to consider speeding up the simulation")
            time.sleep(_time)
            write_fast_file(data,filetype)
            lines = []
             if args.debug and timeindex > 100:
                 exit("Autostopped at 100 reads.")
        else:
            lines.append(line)
        try:
            line = next(rvFile)
        except StopIteration:
            print("All reads were added to simulation folder.")
            break

def get_start_time(_file):
    with open(_file) as f:
        _min = 100000000000000
        for row in f:
            if row.startswith(">") or row.startswith("@"):
                _time = parse_time(row)
                if _min > _time:
                    _min = _time

# Go though files sorted by time created
def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

files = sorted(absoluteFilePaths(args.source_dir), key=os.path.getmtime)

for f in files:
    simulate_reads(f)
