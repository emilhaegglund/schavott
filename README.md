Schavott v0.1.0
========
*Emil Haegglund*  
Applictions to monitor scaffolding or assembly of bacterial genomes in Real-time with MinION sequencing.  
SSPACE-longreads is used for scaffolding, and the minimap/miniasm pipeline is used for assembly.  

Python-requirements
-------------
Python (>=2.7, <3.0)  
Bokeh 0.11.0  
Poretools 0.5.1  
Watchdog 0.8.3  
pyfasta  

Applications
-------------
SSPACE-longreads  

Instructions
------------
Download and install SSPACE-longreads from [here](http://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE-longread).  
Download the zip-file or use git to clone the repository. Install using `python setup.py install`.

Example run - Schavott  
`schavott --sspace_path path_to_sspace --watch pass_download_dir_for_metrichor --contig_file path_to_contig_file`  
  
Example run - Schavott Assembly  
`schavott-assembly --watch pass_download_dir_for_metrichor`  

Arguments
---------
  `-h, --help`  
  show this help message and exit

  `--sspace_path SSPACE_PATH, -p SSPACE_PATH `  
Path to SSPACE  
  
  `--watch WATCH, -w WATCH`  
Directory to watch for fast5 files  
  
`--contig_file CONTIG_FILE, -c CONTIG_FILE`  
Path to contig file  
  
`--run_mode {time,reads}, -r {time,reads}`  
Use timer or read count. (Default: reads)  
  
`--intensity INTENSITY, -i INTENSITY`  
How often the scaffolding process should run. If run mode is set to reads, scaffolding will run every i:th read. If run mode is time, scaffolding will run every i:th second. (Defaut: 100)  
    
`--output OUTPUT, -o OUTPUT`  
Set output filename. (Defaut: schavott)  
