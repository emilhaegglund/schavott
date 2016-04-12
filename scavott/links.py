import os
import subprocess
import timeit


def long_read_src(long_reads, output_dir):
    """
    Create a txt file containing path to all
    long read fasta files.
    """
    path = output_dir + 'long_reads.txt'
    with open(path, 'w') as long_read_file:
        for line in long_reads:
            long_read_file.write(line + '\n')

    return path


def run_links(short_reads, long_reads, output_dir):
    """Run LINKS scaffolder

    Args:
        short_reads (str): Path to sequences to scaffold
        long_reads (list): List of long read files

    Returns:
        scaffolds (int): Number of scaffolds in the resulting file
    """
    print("In run links function")
    # Merge fasta file to multifasta
    path = long_read_src(long_reads, output_dir)

    # print("Completed long read src function")
    print("Run LINKS")
    # Command line arguments for LINKS

    args = ['LINKS', '-f', short_reads, '-s', path, '-d', '400',
            '-l', '1', '-b', output_dir]

    # Run links
    tic = timeit.default_timer()

    # Run LINKS quiet
    process = subprocess.Popen(args, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    toc = timeit.default_timer()
    timer = toc - tic
    print('Runtime for LINKS: ' + str(timer))
    return parse_results(output_dir)


def parse_results(output_dir):
    """Parse output from LINKS
    """
    # print('In parse result')
    scaffold_files = []
    files = os.listdir(output_dir)
    for scaffold_file in files:
        if scaffold_file.endswith("scaffolds"):
            scaffold_files.append(scaffold_file)
    for scaffold_file in scaffold_files:
        # print(path+scaffold_file)
        with open(output_dir+scaffold_file, 'r') as f:
            content = f.readlines()
        number_of_scaffolds = len(content)

    return number_of_scaffolds