import subprocess
import schavott.gfatofasta
import os
import pyfasta

class Assembly():
    def __init__(self):
        self.nrReads = 0
        self.assemblyCounter = 1
        self.nrContigs = 0
        self.N50 = 0
        self.contig_size_dict = {}

    def miniasm(self, path_to_np_reads):
        """Run miniasm."""
        print('Run miniasm')
        args = ['miniasm', '-f', path_to_np_reads, self.paf_path]
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate()
        print('Write assembly to file')
        self.assembly_path = 'assembly.gfa'
        with open(self.assembly_path, 'w') as assembly_file:
            assembly_file.write(str(out))
        print('Return assembly')

    def minimap(self, path_to_np_reads):
        """Run minimap"""
        print('Run minimap')
        args = ['minimap', '-x', 'ava10k', '-t', '12', path_to_np_reads, path_to_np_reads]
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate()
        print(out)
        print(err)
        print('Write paf-file')
        self.paf_path = 'out.paf'
        with open(self.paf_path, 'w') as paf_file:
            paf_file.write(str(out))
        print('Return paf-file')

    def run_mini(self, path_to_np_reads, output, passCounter):
        """Run minimap and miniasm."""
        new_folder  =  output + '_' + str(self.assemblyCounter)
        os.mkdir(new_folder)
        self.minimap(path_to_np_reads)
        self.miniasm(path_to_np_reads)
        fasta_output = schavott.gfatofasta.gfatofasta(self.assembly_path, new_folder)
        self.assemblyCounter += 1
        self.nrReads = passCounter
        self.parse_fasta(fasta_output)

    def parse_fasta(self, fasta):
        """Parse resulting fasta file from SSPACE"""
        self._get_N50(fasta)
        self._get_NrContigs(fasta)
        self._contig_size_list(fasta)
        self._contig_size_dict(fasta)

    def _get_N50(self, path):
        """Calculate N50 value for fasta file."""
        self._contig_size_list(path)

        if len(self.contig_sizes) == 0:
            self.N50 = 0
        total_bases = sum(self.contig_sizes)
        half_size = total_bases/2
        N50 = 0
        contig_sum = 0
        for contig in self.contig_sizes:
            N50 = contig
            contig_sum += contig
            if contig_sum > half_size:
                break

        self.N50 = N50


    def _get_NrContigs(self, path):
        """Find the number of contigs in the fasta file."""
        try:
          f = pyfasta.Fasta(path)
          counter = 0
          for header in f:
            counter += 1
          self.nrContigs = counter
        except ValueError:
          self.nrContigs = 0

    def _contig_size_dict(self, path):
        """Find the distribution of contig sizes."""
        try:
          f = pyfasta.Fasta(path)
          self.contig_size_dict = {}
          for keys in f.keys():
            self.contig_size_dict[keys] = len(f[keys])
          self.contig_size_dict
        except ValueError:
          self.contig_size_dict = {}


    def _contig_size_list(self, path):
        """Insert all contig sizes in a list."""
        try:
          f = pyfasta.Fasta(path)
          self.contig_sizes = []
          for keys in f.keys():
            self.contig_sizes.append(len(f[keys]))
          self.contig_sizes.sort()
        except ValueError:
          self.contig_sizes = []
