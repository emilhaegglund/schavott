# -*- coding: utf-8 -*-
"""GFA to Fasta converter."""
import argparse


def gfatofasta(gfa_path, out_prefix):
	""""""
	fasta_sequences = read_gfa(gfa_path)
	fasta_path = write_fasta(fasta_sequences, out_prefix)

	return fasta_path

def insert_newlines(string, every=80):
    return '\n'.join(string[i:i+every] for i in xrange(0, len(string), every))

def read_gfa(gfa_path):
	fasta_sequences = {}
	with open(gfa_path, 'r') as gfa_file:
		for line in gfa_file:
			line_list = line.split('\t')
			if line_list[0] == 'S':
				fasta_sequences[line_list[1]] = line_list[2]
	print(len(fasta_sequences))
	return fasta_sequences

def write_fasta(fasta_sequences, out_prefix):
	fasta_path = out_prefix + '/assembly.fasta'
	with open(fasta_path, 'w') as fasta_file:
		for header in fasta_sequences:
			fasta_header = '>' + header + '\n'
			fasta_file.write(fasta_header)
			fasta_sequence = insert_newlines(fasta_sequences[header]) + '\n'
			fasta_file.write(fasta_sequence)

	return fasta_path

def parse_arguments():
	parser = argparse.ArgumentParser(description='Convert GFA to Fasta')
	parser.add_argument("gfa_path", help="Path to GFA-file")
	parser.add_argument("output", help="Output name")
	args = parser.parse_args()
	return args


def main():
	args = parse_arguments()
	gfatofasta(args.gfa_path, args.output)

if __name__ == '__main__':
    main()