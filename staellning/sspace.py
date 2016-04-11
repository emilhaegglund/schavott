import subprocess
import argparse
import os
import matplotlib.pyplot as plt


path_to_SSPACE = '/scratch/emihag/SSPACE-LongRead_v1-1/SSPACE-LongRead.pl'

# Counter for multifasta file
global reads
reads = 0


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


def parse_sspace_out(output, counter, genome_size):
    """Find the number of scaffolds.

    Parse the scaffold_evidence.txt to find the number
    of scaffolds obtained when running SSPACE.

    Args:
        output (str): Path to output directory.

    Returns:
        number_of_scaffolds (int): Number of scaffolds
            obtained when running SSPACE.
    """
    print('Parse SSPACE output')
    file_path = output + '/scaffold_evidence.txt'
    with open(file_path, 'r') as result_file:
        content = result_file.readlines()

    scaffolds = {}
    for line in content:
        if line[0] == '>':
            print(line)
            scaffold = line.split('|')
            # scaffolds[scaffold[0][1:]] = None
            scaffold_length = scaffold[1]
            scaffold_length = int(scaffold_length[4:])
            scaffolds[scaffold[0][1:]] = scaffold_length
            if scaffold_length > int(genome_size) * 0.5 and scaffold_length < int(genome_size) * 1.5:
                print('Set completed to True')
                completed = True
            else:
                completed = False

    fasta_file = output + '/scaffolds.fasta'
    process = subprocess.Popen(['fastainfo', fasta_file], stdout=subprocess.PIPE)
    out = process.communicate()
    out = out[0].splitlines()
    for line in out:
        if line[0:3] == 'N50':
            N50 = line[5:]

    with open('N50.csv', 'a') as N50_file:
        N50_file.write(N50 + ', ')

    number_of_scaffolds = len(scaffolds)
    counter[3].append(number_of_scaffolds)
    
    reads = counter[0] * 100
    counter[1].append(int(N50))
    counter[2].append(reads + 100)
    counter[4] = scaffolds
    # fig, ax1 = plt.subplots()
    # ax1.plot(counter[2], counter[1], 'b')
    # ax1.set_ylabel('N50', color='b')
    # ax1.set_ylim([0, int(genome_size)])
    # ax1.set_xlim([0, counter[2][-1]+100])
    # for tl in ax1.get_yticklabels():
    #     tl.set_color('b')

    # ax2 = ax1.twinx()
    # ax2.plot(counter[2], counter[3], 'r')
    # ax2.set_ylabel('Scaffolds', color='r')
    # ax2.set_ylim([0, counter[3][0]])
    # ax2.set_xlim([0, counter[2][-1]+100])
    # for tl in ax2.get_yticklabels():
    #     tl.set_color('r')
    
    # plt.savefig('foo' + str(counter[0]) + '.png')

    # print('counter[1]: ' + str(counter[1]))
    # print('counter[2]: ' + str(counter[2]))
    # with open('sspace_result.csv', 'a') as store_result:
    #     result_string = str(reads) + ', '
    #     for key in scaffolds.keys():
    #             result_string = result_string + str(scaffolds[key][-1]) + ', '
    #     result_string = result_string + '\n'
    #     store_result.write(result_string)

    counter[0] += 1
    # Test set-up, following code is only for test purpose.
    # scaffold_length = 1850959
    # if scaffold_length > int(genome_size) * 0.9 and scaffold_length < int(genome_size) * 1.1:
    #     completed = True
    # else:
    #     completed = False

    # counter += 1
    # number_of_scaffolds = 13

    return number_of_scaffolds, counter, completed


def run_sspace(short_reads, long_reads, output_dir, counter, genome_size):
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
    print(nanopore_reads)
    print(genome_size)
    # Command line arguments for SSPACE
    output = output_dir + '_' + str(counter[0])
    args = ['perl', path_to_SSPACE, '-c', short_reads, '-p', nanopore_reads,
            '-i', '70', '-a', '1500', '-g' '-5000', '-b', output]

    print("Run SSPACE")
    process = subprocess.Popen(args, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)
    out, err = process.communicate()

    number_of_scaffolds, counter, completed = parse_sspace_out(output, counter, genome_size)

    # # Test set-up
    # print("Fake run SSPACE...")
    # number_of_scaffolds = 13
    # counter += 1
    # completed = True

    return number_of_scaffolds, counter, completed

# number_of_scaffolds, counter = parse_sspace_out('test/', 0)
