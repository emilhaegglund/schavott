Schavott v0.5.0
========
[![bioconda-badge](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](http://bioconda.github.io) [![PyPI release](https://img.shields.io/pypi/v/schavott.svg)](https://pypi.python.org/pypi/schavott/)

Applictions to monitor scaffolding or assembly of bacterial genomes in Real-time with MinION sequencing.  
SSPACE-longreads or links can be used for scaffolding, and the minimap/miniasm pipeline can be used for assembly.  
![Schavott GUI](https://github.com/emilhaegglund/schavott/blob/master/gui.png)

Python-requirements
-------------
Python (>=2.7, <3.0)  
Bokeh  
h5py 2.2.0  
Watchdog 0.8.3  
pyfasta  

Using Conda
-------------
A conda environment installation settingsfile was added in config/schavott_conda_env.yaml
The path to your local conda installation needs to be modified. Then run:
conda env create -f config/schavott_conda_env.yaml

Applications
-------------
SSPACE-longreads, [links](https://github.com/warrenlr/LINKS) and/or [minimap](https://github.com/lh3/minimap)/[miniasm](https://github.com/lh3/miniasm)

Instructions
------------
Download and install SSPACE-longreads from [here](http://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE-longread).  
Download the zip-file or use git to clone the repository. Install using `python setup.py install`.  
A [bokeh server](http://bokeh.pydata.org/en/latest/) must be running on the computer for the application to start, this is used to plot the result in a web browser.  

To start a bokeh server, run the following command in the terminal:  
`bokeh serve`   


Example run  
SSPACE-longreads  
`schavott --scaffolder sspace_path path_to_sspace --watch pass_download_dir_for_metrichor --contig_file path_to_contig_file`  

links  
`schavott --scaffolder links --watch pass_download_dir_for_metrichor --contig_file path_to_contig_file`  

minimap/miniasm   
`schavott --run_mode assembly --min_read_length 5000 --min_quality 8 --watch pass_download_dir_for_metrichor`  


Arguments
---------
`-h, --help`  
show this help message and exit  
  
`--run_mode {scaffold, assembly}`  
Assemble or scaffold genome using MinION reads.  
  
`--scaffolder {SSPACE, links}`  
If scaffold, which scaffolder to use.  
  
`--sspace_path SSPACE_PATH, -p SSPACE_PATH `  
In case SSPACE is used, give the path to SSPACE.  
  
`--watch WATCH, -w WATCH`  
Directory to watch for fast5 files, usually metrichor downloads/pass folder.  
  
`--min_read_length`  
Minimum read length to use. (Default: 5000)  
  
`--min_quality`  
Minimum read quality. (Default: 9)

`--skip SKIP, -j SKIP`
Skip the first reads of the sequencing run. (Default: 0)
  
`--contig_file CONTIG_FILE, -c CONTIG_FILE`  
Path to contig file if scaffolding, fasta-format.  
  
`--run_mode {time,reads}, -r {time,reads}`  
Use timer or read count. (Default: reads)  
  
`--intensity INTENSITY, -i INTENSITY`  
How often the scaffolding process should run. If run mode is set to reads, scaffolding will run every i:th read. If run mode is time, scaffolding will run every i:th second. (Defaut: 100)  
  
`--output OUTPUT, -o OUTPUT`  
Set output filename. (Defaut: schavott)  
  
`--plot`  
Show bokeh GUI in web-browser, this require a bokeh server to run.

Test run using existing MinION data
------------------------------

### Modern data (>=9.4)

You may use the simulation script to test the application using already sequenced data that is basecalled using albacore (>2.0). 

```
python read_simulation [path/to/source_folder/] [path/to/watchdir] [start time] --speed super-sonic --force 
```

The force parameter is used to clean your watchdir from previous files to avoid duplication and manual cleaning of folder during tests. If you want to speed things up when testing, you could always change `real-time` to `fast-forward` or `super-sonic`.

### Ancient data (<=7.3)

It is possible to test the application using already sequenced data by older generation of the technology. To do this, the time-information and the path to the fast5-files must be extracted. To do this, run [poretools](https://github.com/arq5x/poretools) times on the folder containing the fast5-files.

```poretools times path/to/fast5-dir > times.csv```  

In a second terminal start the Schavott application using the previously described commands, and set the watch directory to target_dir. Next the move_fast5.py script is run to simulate the creation of new fast5-files in the target directory, files are copied from the fast5-files source directory to the target directory using the time information in the fast5-files.

```
python move_fast5.py times.csv target_dir/ real-time
```
