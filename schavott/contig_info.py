import pyfasta
import sys
import os


def get_N50(path):
    """Return N50 value."""
    print(path)
    print("In N50")
    contig_sizes = get_contig_size_list(path)
    print("Contig sizes: " + str(len(contig_sizes)))
    if len(contig_sizes) == 0:
        return 0
    total_bases = sum(contig_sizes)
    half_size = total_bases/2
    N50 = 0
    contig_sum = 0
    for contig in contig_sizes:
        N50 = contig
        contig_sum += contig
        if contig_sum > half_size:
            break

    return N50


def get_contigs(path):
    """Return number of contigs."""
        # If assembly fails
    print("In get contigs")
    if os.stat(path).st_size == 0:
        print("Fasta file is empty")
        return 0
    try:
        print("Try open fasta")
        f = pyfasta.Fasta(path)
    except pyfasta.fasta.FastaNotFound:
        print("Error: contig file does not exist")
        sys.exit()
    return len(f)


def get_contig_sizes(path):
    """Return size of each contig."""
    print("In get contig sizes")
    if os.stat(path).st_size == 0:
        print("Fasta file is empty")
        return {}
    try:
        print("Tre open fasta")
        f = pyfasta.Fasta(path)
    except pyfasta.fasta.FastaNotFound:
        print("Error: contig file does not exist")
        sys.exit()
    contig_sizes = {}
    for keys in f.keys():
        contig_sizes[keys] = len(f[keys])

    return(contig_sizes)


def get_contig_size_list(path):
    # If assembly fails
    print("In get contig size list")
    if os.stat(path).st_size == 0:
        print("Fasta file is empty")
        return []
    try:
        print("Try open fasta")
        f = pyfasta.Fasta(path)
    except pyfasta.fasta.FastaNotFound:
        print("Error: contig file does not exist")
        sys.exit()
    contig_sizes = []
    for keys in f.keys():
        contig_sizes.append(len(f[keys]))
    contig_sizes.sort()

    return contig_sizes