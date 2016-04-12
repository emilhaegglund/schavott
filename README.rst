##Read me##
Scaffolding application running in parallel with MinION-sequencing. Watch a directory for fast5 files and use them to scaffold a genome.
The scaffolding process can be triggered either by number of reads or after a specific time. At the moment, only SSPACE-LongRead is the
supported scaffolder at this moment. N50 value, contig number and contig length is plotted in web browser using bokeh. Also a graph
representation of the assembly is plotted.

##Dependencies##
* Python 2.7
* poretools 0.5.1
* Watchdog 0.8.3
* Bokeh 0.11.1
* Numpy 1.10.4
* SSPACE-LongRead v1.1

##Command line arguments##
`--scaffolder (-s) sspace`  
`--watch (-w) Directory to basecalled fast5-file`  
`--short_reads (-c) Path to fasta-file with contigs`  
`--run_mode (-r) 'time' or 'reads'`  
`--intensity (-i) Number of reads or seconds between scaffolding`  
`--output (-o) Basename for output, each scaffoldprocess is saved in basename_nr` 
