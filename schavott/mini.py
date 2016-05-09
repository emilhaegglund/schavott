import subprocess
import gfatofasta
import contig_info
import os

def create_multi_fasta(long_reads, output):
    """Create a multifasta sequence file.

    SSPACE requires that all long reads are in
    a single multifasta file. This function append
    new reads to the multifasta file.

    Args:
        long_reads (list): Path to nanopore fasta files.
        output_dir (str): Output directory for program

    Returns:
        path (str): Path to multifasta file.
    """
    global reads

    path = output + '/np_reads.fasta'
    with open(path, 'a') as outfile:
        for fasta in long_reads:
            with open(fasta, 'r') as infile:
                for line in infile:
                    if line[0] == '>':
                        outfile.write(line)
                    else:
                        outfile.write(line + '\n')

    reads = len(long_reads)
    return path


def miniasm(fastafile, paffile):
    """Run miniasm."""
    print('Run miniasm')
    args = ['miniasm', '-f', fastafile, paffile]
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate()
    print('Write assembly to file')
    assembly_path = 'assembly.gfa'
    with open(assembly_path, 'w') as assembly_file:
        assembly_file.write(out)
    print('Return assembly')
    return assembly_path

def minimap(fastafile):
    """Run minimap"""
    print('Run minimap')
    args = ['minimap', '-x', 'ava10k', '-t', '12', fastafile, fastafile]
    process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate()
    print(err)
    print('Write paf-file')
    paf_path = 'out.paf'
    with open(paf_path, 'w') as paf_file:
        paf_file.write(out)
    print('Return paf-file')
    return paf_path


def run_mini(long_reads, output_dir, counter, intensity):
    """Run minimap and miniasm."""
    output = output_dir + '_' + str(counter[0])
    
    print("Maked dir")
    os.mkdir(output)
    fasta_file = create_multi_fasta(long_reads, output)
    paf_file = minimap(fasta_file)
    assembly_file = miniasm(fasta_file, paf_file)
    gfatofasta.gfatofasta(assembly_file, output)
    print(contig_info.get_N50(output+'.fasta'))
    print(contig_info.get_contigs(output+'.fasta'))
