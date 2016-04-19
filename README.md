schavott
========
*Emil Haegglund*  
Appliction for scaffolding bacterial genomes in Real-time with SSPACE-longreads
and MinION sequencing.

Python-requirements
-------------
Bokeh 0.11.0  
Poretools 0.5.1  
Watchdog  
pyfasta  

Applications
-------------
SSPACE-longreads  

Instructions
------------
Download and install SSPACE-longreads from [here](http://www.baseclear.com/genomics/bioinformatics/basetools/SSPACE-longread).  
Download the zip-file or use git to clone the repository. Install using `python setup.py install`.

Example run  
`schavott --scaffolder sspace --space_path path_to_sspace --watch download_dir_for_metrichor`
