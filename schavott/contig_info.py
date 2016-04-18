import pyfasta

def get_N50(path):
    """Return N50 value."""
    f = pyfasta.Fasta(path)
    contig_sizes = get_contig_size_list(path)
    total_bases = sum(contig_sizes)
    half_size = total_bases/2
    N50 = 0
    contig_sum = 0
    for contig in contig_sizes:
        N50 = contig
        contig_sum += contig
        if  contig_sum > half_size:
            break

    return N50


def get_contigs(path):
    """Return number of contigs."""
    f = pyfasta.Fasta(path)
    return len(f)


def get_contig_sizes(path):
    """Return size of each contig."""
    f = pyfasta.Fasta(path)
    contig_sizes = {}
    for keys in f.keys():
        contig_sizes[keys] = len(f[keys])

    return(contig_sizes)


def get_contig_size_list(path):
    f = pyfasta.Fasta(path)
    contig_sizes = []
    for keys in f.keys():
        contig_sizes.append(len(f[keys]))
    contig_sizes.sort()

    return(contig_sizes)