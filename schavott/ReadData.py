import h5py
import datetime
import numpy as np

class ReadData(object):
    def __init__(self, filePath=False, fasta_seq=False, fastq_quality=False,seqlen=False,start_time=False):
        ### The new basecallers for nanopore has a quality pass/fail test included, hence is not nessesary check read quality in schavott.
        self.passQuality = True
        self.twod = False
        self.oned = False
        #self.type = event.src_path.strip().rsplit(".")[-1]
        if filePath:
            '''Input is in fast5 format, open read with h5py and parse read information'''
            self.type="fast5"
            open_read(filePath)
            self.passQuality = False
            self.set_time(fast5=True)
            self.set_1d()
            self.set_length_1d()
            self.set_quality_1d()
            self.set_fastq_1d()
            self.set_fasta_1d()
            self.set_2d()
            self.set_length()
            self.set_quality()
            self.set_fastq()
            self.set_fasta()
            self.close_read()

            '''The new fasta files do not have single read constraint, which means that multiple reads can come from one file, if this is the case the file will be looped before turned into a read'''
        elif fastq_quality:
            '''Input is in fasta format, add the fasta sequence to the read information'''
            self.type="fastq"
            self.set_fastq(fastq_quality)
            self.set_fasta(fasta_seq)
            self.set_length(length=seqlen)
        elif fasta_seq:
            '''Input is in fastq format, store the fastq quality string and the sequence'''
            self.type="fasta"
            self.set_fasta(fasta_seq)
            self.set_length(length=seqlen)

        ## Set timestamp
        if start_time:
            #self.set_time(time=start_time)
            self.set_time()
        else:
            self.set_time()

    def open_read(self, path):
        try:
            self._fast5 = h5py.File(path)
        except IOError:
            print('{File} was not possible to open'.format(path))

    def close_read(self):
        self._fast5.close()

    def set_2d(self):
        try:
            self._fast5['Analyses']['Basecall_2D_000']['BaseCalled_2D']
            self.twod = True
            #print('Has 2D')
        except:
            print('No 2D sequence')

    def set_1d(self):
        try:
            self._fast5['Analyses']['Basecall_1D_000']['BaseCalled_template']
            self.oned = True
        except:
            print('No template sequence')

    def set_length_1d(self):
        if self.oned:
            self.length_1d = self._fast5['Analyses']['Basecall_1D_000']['Summary']['basecall_1d_template'].attrs['sequence_length']
            #print('Read length (template): ' + str(self.length_1d))

    def set_fastq_1d(self):
        if self.oned:
            self.fastq_1d = str(np.array(self._fast5['Analyses']['Basecall_1D_000']['BaseCalled_template']['Fastq']))

    def set_fasta_1d(self):
        if self.oned:
            raw_fasta = self.fastq_1d.split('\n')[:2]
            header = '>' + raw_fasta[0][3:] + '\n'
            seq = raw_fasta[1] + '\n'
            self.fasta_1d = header + seq

    def set_length(self, length=False):
        if length:
            ## The fasta file is split in case there is a header > \n sequence also any trailing spaces will be stripped before counting bases
            self.length = length
        elif self.twod:
            self.length = self._fast5['Analyses']['Basecall_2D_000']['Summary']['basecall_2d'].attrs['sequence_length']
            #print('Read length (2d): ' + str(self.length))

    def set_fastq(self,fastq=False):
        if fastq:
            self.fastq = fastq
        elif self.twod:
            self.fastq = str(np.array(self._fast5['Analyses']['Basecall_2D_000']['BaseCalled_2D']['Fastq']))

    def set_fasta(self, fasta=False):
        if fasta:
            self.fasta = fasta
        elif self.twod:
            raw_fasta = self.fastq.split('\n')[:2]
            header = '>' + raw_fasta[0][3:] + '\n'
            seq = raw_fasta[1] + '\n'
            self.fasta = header + seq

    def set_time(self,fast5=False,time=False):
        if fast5:
            expStartTime = self._fast5['UniqueGlobalKey']['tracking_id'].attrs['exp_start_time']
            samplingRate = self._fast5['UniqueGlobalKey']['channel_id'].attrs['sampling_rate']
            for key in self._fast5['Raw']['Reads'].keys():
                startSample = self._fast5['Raw']['Reads'][key].attrs['start_time']
                durationSample = self._fast5['Raw']['Reads'][key].attrs['duration']
        #self.startTime = datetime.datetime.fromtimestamp(int(expStartTime) + float(startSample)/samplingRate + float(durationSample)/samplingRate)
        if time:
            self.startTime = time
        else:
            self.startTime = datetime.datetime.now().time()

    def set_quality(self):
        if self.twod:
            self.quality = self._fast5['Analyses']['Basecall_2D_000']['Summary']['basecall_2d'].attrs['mean_qscore']
            #print('Read quality:' + str(self.quality))

    def set_quality_1d(self):
        if self.oned:
            self.quality_1d = self._fast5['Analyses']['Basecall_1D_000']['Summary']['basecall_1d_template'].attrs['mean_qscore']

    def set_pass(self):
        self.passQuality = True

    def get_fastq(self):
        return self.fastq

    def get_fasta(self):
        return self.fasta

    def get_pass(self):
        return self.passQuality

    def get_length(self):
        return self.length

    def get_quality(self):
        return self.quality

    def get_time(self):
        return self.startTime

    def get_twod(self):
        return self.twod

    def get_oned(self):
        return self.oend

    def get_quality_1d(self):
        return self.quality_1d

    def get_length_1d(self):
        return self.length_1d

    def get_fastq_1d(self):
        return self.fastq_1d

    def get_fasta_1d(self):
        return self.fasta_1d
