import timeit
import os
import sys
import glob
import schavott.ReadData
import schavott.UI
import schavott.Scaffold
import schavott.Assembler

class MainApp(object):
    # TODO: Add switch to discard xx number of reads in the beginning
    # to avoid reads from wrong organism in the scaffolding.
    def __init__(self, args):
        self.readQue = []
        self.reads = []
        self.passCounter = 0
        self.failCounter = 0
        self.runMode = args.run_mode
        self.skip = args.skip
        self.skip_counter = 0
        self.output = args.output
        self.plot = args.plot
        self.triggerMode = args.trigger_mode
        # Will be added to argument list
        self.readLengths = []
        self.minQuality = int(args.min_quality)
        self.minLength = int(args.min_read_length)
        self._reset_timer()
        self._set_intensity(args.intensity)
        
        # Create scaffold or assembly object
        if self.runMode == 'scaffold':
            self.scaffoldApp = args.scaffolder
            if self.scaffoldApp == 'sspace':
                self._setup_scaffolder(args.contig_file, args.sspace_path)
            else:
                self._setup_scaffolder(args.contig_file)
        else:
            self._setup_assembler()

        # Create plots
        if self.plot:
            self._setup_plots()
        
        # Create output directories
        if os.path.isdir(self.output):
            if os.listdir(self.output) == ['reads_fasta']:
                pass
            elif os.listdir(self.output) == []:
                os.mkdir(os.path.join(self.output, 'reads_fasta'))
            else:
                sys.exit("Output directory contains something, use an empty dir")
        else:
            os.mkdir(self.output)
            os.mkdir(os.path.join(self.output, 'reads_fasta'))

    def open_read(self, filePath):
        """Open downloaded fast5"""
        # Try to read fast5 file.
        self.skip_counter += 1
        if self.skip_counter > self.skip:
            try:
                head, tail = os.path.split(filePath)
                root, ext = os.path.splitext(tail)
                read = schavott.ReadData.ReadData(filePath)
                self.add_read(read)
                # Change if statement to if read.get_twod(): to use 2D reads, depricated from ONT.
                if False:
                    self.readLengths.append(read.get_length())
                    if read.get_quality() >= self.minQuality and read.get_length() >= self.minLength:
                        read.set_pass()
                        with open(os.path.join(self.output, "reads_fasta", root) + '.fasta', 'w') as f:
                            f.write(str(read.get_fasta()))
                        f.close()
                        self.update_counter(read)
                    else:
                        self.readLengths.append(read.get_length_1d())
                        if read.get_quality_1d() >= self.minQuality and read.get_length_1d() >= self.minLength:
                        read.set_pass()
                        with open(os.path.join(self.output, "reads_fasta", root) + '.fasta', 'w') as f:
                            f.write(str(read.get_fasta_1d()))
                        f.close()
                        self.update_counter(read)
            except AttributeError:
                self.add_to_readQue(filePath)

    def add_read(self, read):
        self.reads.append(read)

    def update_counter(self, read):
        if read.get_pass():
            self.passCounter += 1
            print('Reads: ' + str(self.passCounter))
            self.run_scaffold()
        else:
            self.failCounter += 1
        if self.plot:
            self._update_readPlots(read)

    def add_to_readQue(self, filePath):
        """ Reads failed to open """
        self.readQue.append(filePath)

    def run_scaffold(self):
        if self.passCounter % int(self.intensity) == 0 and \
           self.triggerMode == 'reads':
                if self.runMode== 'scaffold':
                    print("Scaffolding")
                    self.scaffolder.run_scaffold(self.passCounter)
                    self.UI.update_scaffold_plots(self.scaffolder)
                else:
                    print("Assembly")
                    self.assembler.run_mini(self.passCounter)
                    self.UI.update_scaffold_plots(self.assembler)
        elif int(timeit.default_timer()) - self.timer > self.intensity and \
                self.triggerMode == 'time':
                if self.runMode == 'scaffold':
                    print("Scaffolding")
                    self.scaffolder.run_scaffold(self.passCounter)
                    self.UI.update_scaffold_plots(self.scaffolder)
                else:
                    print("Assembly")
                    self.assembler.run_mini(self.passCounter)
                    self.UI.update_scaffold_plots(self.assembler)
                self._reset_timer()

    def _reset_timer(self):
        self.timer = timeit.default_timer()

    def _set_intensity(self, intensity):
        try:
            self.intensity = int(intensity)
        except ValueError:
            print('Error: intensity is not a valid number')

    def _setup_scaffolder(self, contig_file, sspace_path=None):
        self.scaffolder = schavott.Scaffold.Scaffold(contig_file, os.path.join(self.output + 'np_reads.fasta'),  self.scaffoldApp, self.output, sspace_path)

    def _setup_assembler(self):
        self.assembler = schavott.Assembler.Assembly(self.output, os.path.join(self.output + 'np_reads.fasta'))

    def _setup_plots(self):
        if self.runMode == 'scaffold':
            self.UI = schavott.UI.UI(self.scaffolder)
        else:
            self.UI = schavott.UI.UI(self.assembler)

    def _update_readPlots(self, read):
        nrReads = len(self.reads)
        self.UI.update_read_plots(read, nrReads, self.passCounter,
                                  self.failCounter)
        self.UI.update_read_hist_plot(self.readLengths)
