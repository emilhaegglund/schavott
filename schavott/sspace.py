import subprocess
import os
from contig_info import get_N50, get_contigs, get_contig_sizes


# Counter for multifasta file
global reads
reads = 0


def test_sspace(path_to_SSPACE):
    return os.path.isfile(path_to_SSPACE)


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


def parse_sspace_out(output_dir, counter, intensity):
    """Find the number of scaffolds.

    Parse the scaffold_evidence.txt to find the number
    of scaffolds obtained when running SSPACE.

    Args:
        output (str): Path to output directory.

    Returns:
        number_of_scaffolds (int): Number of scaffolds
            obtained when running SSPACE.
    """
    file_path = output_dir + '_' + str(counter[0]) + '/scaffold_evidence.txt'
    with open(file_path, 'r') as result_file:
        content = result_file.readlines()

    scaffolds = {}
    for line in content:
        if line[0] == '>':
            # print(line)
            scaffold = line.split('|')
            # scaffolds[scaffold[0][1:]] = None
            scaffold_length = scaffold[1]
            scaffold_length = int(scaffold_length[4:])
            scaffolds[scaffold[0][1:]] = scaffold_length
            # if scaffold_length > int(genome_size) * 0.2 and scaffold_length < int(genome_size) * 1.05:
            #     print('Set completed to True')
            #     completed = True
            # else:
            #     completed = False

    fasta_file = output_dir + '_' + str(counter[0]) + '/scaffolds.fasta'
    N50 = get_N50(fasta_file)
    counter[4] = get_contig_sizes(fasta_file)
    number_of_scaffolds = get_contigs(fasta_file)
    counter[3].append(number_of_scaffolds)

    # reads = counter[0] * int(intensity)
    counter[1].append(int(N50))
    counter[2].append(counter[5][-1])
    
    with open(output_dir +  '_statistics.csv', 'a') as statistics:
        statistics.write(str(counter[5][-1]) + ',' + str(number_of_scaffolds) + ',' + str(N50) + '\n') 

    counter[0] += 1

    return number_of_scaffolds, counter


def run_sspace(short_reads, long_reads, output_dir, counter,
               path_to_SSPACE, intensity):
    """Run SSPACE scaffolder

    Args:
        short_reads (str): Path to multifasta file
            containing contigs.
        long_reads (list): List of path to nanopore
            fasta file.
        output_dir (str): Path to output directory.

    Returns:
        number_of_scaffolds (int): Number of scaffolds
            obtained when running SSPACE.
    """
    output = output_dir + '_' + str(counter[0])
    os.mkdir(output)
    nanopore_reads = create_multi_fasta(long_reads, output)
    # Command line arguments for SSPACE
    output = output_dir + '_' + str(counter[0])
    args = ['perl', path_to_SSPACE, '-c', short_reads, '-p', nanopore_reads,
            '-i', '70', '-a', '1500', '-g' '-5000', '-b', output]

    #print("Run SSPACE")
    process = subprocess.Popen(args, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()

    number_of_scaffolds, counter = parse_sspace_out(output_dir, counter, intensity)

    # # Test set-up
    # print("Fake run SSPACE...")
    # number_of_scaffolds = 13
    # counter += 1
    # completed = True

    return number_of_scaffolds, counter

# number_of_scaffolds, counter = parse_sspace_out('test/', 0)
