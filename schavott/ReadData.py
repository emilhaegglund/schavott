import h5py
import datetime
import numpy as np


class ReadData(object):
    def __init__(self, filePath):
        self.open_read(filePath)
        self.passQuality = False
        self.twod = False
        self.set_2d()
        self.set_length()
        self.set_quality()
        self.set_time()
        self.set_fastq()
        self.set_fasta()
        self.close_read()

    def open_read(self, path):
        try:
            self._fast5 = h5py.File(path)
        except IOError:
            print('File was not possible to open')
        
    def close_read(self):
        """Always remember to close your open files... """
        self._fast5.close()

    def set_2d(self):
    
        try:
            self._fast5['Analyses']['Basecall_2D_000']['BaseCalled_2D']
            self.twod = True
        except:
            print('1D')

    def set_length(self):
        if self.twod:
            self.length = self._fast5['Analyses']['Basecall_2D_000']['Summary']['basecall_2d'].attrs['sequence_length']
            #print('Read length: ' + str(self.length))

    def set_fastq(self):
        if self.twod:
            self.fastq = str(np.array(self._fast5['Analyses']['Basecall_2D_000']['BaseCalled_2D']['Fastq']))
            
    def set_fasta(self):
        if self.twod:
            raw_fasta = self.fastq.split('\n')[:2]
            header = '>' + raw_fasta[0][3:] + '\n'
            seq = raw_fasta[1] + '\n'
            self.fasta = header + seq

    def set_time(self):
        expStartTime = self._fast5['UniqueGlobalKey']['tracking_id'].attrs['exp_start_time']
        samplingRate = self._fast5['UniqueGlobalKey']['channel_id'].attrs['sampling_rate']
        for key in self._fast5['Raw']['Reads'].keys():
            startSample = self._fast5['Raw']['Reads'][key].attrs['start_time']
            durationSample = self._fast5['Raw']['Reads'][key].attrs['duration']
        self.startTime = datetime.datetime.fromtimestamp(int(expStartTime) + float(startSample)/samplingRate + float(durationSample)/samplingRate)
        #self.startTime = datetime.datetime.now().time()

    def set_quality(self):
        if self.twod:
            self.quality = self._fast5['Analyses']['Basecall_2D_000']['Summary']['basecall_2d'].attrs['mean_qscore']
            #print('Read quality:' + str(self.quality))

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



