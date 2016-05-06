import subprocess
import gfatofasta
import contig_info

def miniasm(fastafile, paffile):
	"""Run miniasm"""
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


def test_mini_pipeline():
	"""Test minimap function."""
	strain = 'FSC771'
	fasta_file = 'FSC771_pass_1000.fasta'
	paf_file = minimap(fasta_file)
	assembly_file = miniasm(fasta_file, paf_file)
	gfatofasta.gfatofasta(assembly_file, strain)
	print(contig_info.get_N50(strain+'.fasta'))
	print(contig_info.get_contigs(strain+'.fasta'))


test_mini_pipeline()