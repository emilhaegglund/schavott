from bokeh.io import gridplot
from bokeh.plotting import figure, curdoc
from bokeh.client import push_session
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from math import pi
import numpy as np
import sys

class UI(object):
    """Graphical UI for schavott"""
    def __init__(self, scaffold):
        self._draw_plots(scaffold)

    def update_scaffold_plots(self, scaffold):
        '''Update plot dictionaries for contig plots'''
        circle = self._calculate_circle(scaffold)

        contig_dist_data = dict(
            start=circle[0],
            stop=circle[1],
            colors=circle[2],
            contigs=circle[3])

        contig_read_data = dict(
            reads=[scaffold.nrReads],
            contigs=[scaffold.nrContigs],
            n50=[scaffold.N50])

        # Reset contig dist source
        self.contig_dist_src.remove('start')
        self.contig_dist_src.remove('stop')
        self.contig_dist_src.remove('colors')
        self.contig_dist_src.remove('contigs')
        self.contig_dist_src.add([], name='start')
        self.contig_dist_src.add([], name='stop')
        self.contig_dist_src.add([], name='colors')
        self.contig_dist_src.add([], name='contigs')

        # Stream data to plot
        self.contig_read_src.stream(contig_read_data, 400)
        self.contig_dist_src.stream(contig_dist_data)

    def update_read_plots(self, read, nrReads, passCounter, failCounter):
        '''Update plot dict for read information'''
        
        read_data = dict(
            nrReads=[nrReads],
            nrPassReads=[passCounter],
            nrFailReads=[failCounter],
            readTime=[read.get_time()])

        self.read_src.stream(read_data, 400)

    def update_read_hist_plot(self, readLengths):
        readHist, edges = np.histogram(readLengths, density=False, bins=20)

        read_hist_data = dict(
            readLength=list(readHist),
            left=list(edges[:-1]),
            right=list(edges[1:]))

    #     # self.read_hist_src.remove('readLength')
    #     # self.read_hist_src.remove('left')
    #     # self.read_hist_src.remove('right')
    #     # self.read_hist_src.add([], name='readLength')
    #     # self.read_hist_src.add([], name='left')
    #     # self.read_hist_src.add([], name='right')

        self.read_hist_src.stream(read_hist_data, rollover=400)


    def _draw_plots(self, scaffolder):
        '''Setup all plots.'''
        self.contig_read_src = ColumnDataSource(dict(
            reads=[scaffolder.nrReads],
            contigs=[scaffolder.nrContigs],
            n50=[scaffolder.N50]))

        # Calculate data for contig circle plot
        circle = self._calculate_circle(scaffolder)
        self.contig_dist_src = ColumnDataSource(dict(
            start=circle[0],
            stop=circle[1],
            colors=circle[2],
            contigs=circle[3]))

        self.read_src = ColumnDataSource(dict(
            nrReads=[],
            nrPassReads=[],
            nrFailReads=[],
            readTime=[]))

        self.read_hist_src = ColumnDataSource(dict(
            readLength=[],
            left=[],
            right=[]))

        # Draw plots
        contigNrPlot = self._draw_contigNrPlot(scaffolder)
        n50Plot = self._draw_n50Plot()
        contigCirclePlot = self._draw_contigCirclePlot()
        readPlot = self._draw_readCountPlot()
        #readHist = self._draw_readLenHistPlot()

        # Position plots
        layout = gridplot([[n50Plot, contigNrPlot],
                          [contigCirclePlot, readPlot]])
        try:
            session = push_session(curdoc())
            session.show(layout)
        except IOError:
            sys.exit("No bokeh server is running on this host")

    def _draw_contigNrPlot(self, scaffolder):
        plot = figure(title='Number of contigs')
        plot.circle(x='reads', y='contigs',
                    source=self.contig_read_src, size=10)
        plot.line(x='reads', y='contigs', line_width=4, source=self.contig_read_src)
        plot.xaxis.axis_label = '# Reads'
        plot.yaxis.axis_label = 'Contigs'
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.major_label_text_font_size = '14pt'
        plot.xaxis.major_label_text_font_size = '14pt'
        plot.title.text_font_size = '16pt'

        return plot

    def _draw_n50Plot(self):
        plot = figure(title='N50 Values')
        plot.circle(x='reads', y='n50', source=self.contig_read_src,
                    size=10, color='red')
        plot.line(x='reads', y='n50', line_width=4, source=self.contig_read_src, color='red')
        plot.xaxis.axis_label = '# Reads'
        plot.yaxis.axis_label = 'N50'
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.major_label_text_font_size = '14pt'
        plot.xaxis.major_label_text_font_size = '14pt'
        plot.yaxis[0].formatter = NumeralTickFormatter(format='0.00a')
        plot.title.text_font_size = '16pt'
        
        return plot

    def _draw_contigCirclePlot(self):
        hover = HoverTool(tooltips=[('Length', '@contigs')])
        hover.point_policy = "follow_mouse"
        plot = figure(x_axis_type=None, y_axis_type=None, tools=[hover], title='Contig lengths')
        plot.annular_wedge(x=0, y=0, inner_radius=0.5, outer_radius=0.7,
                           start_angle='start', end_angle='stop',
                           color='colors', alpha=0.9, source=self.contig_dist_src)
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.major_label_text_font_size = '14pt'
        plot.xaxis.major_label_text_font_size = '14pt'
        plot.title.text_font_size = '16pt'

        return plot

    def _draw_readCountPlot(self):
        plot = figure(x_axis_type='datetime', title='Processed Reads')
        plot.circle(x='readTime', y='nrReads', source=self.read_src, size=10, color='firebrick')
        plot.xaxis.axis_label = 'Time (min)'
        plot.yaxis.axis_label = '# Reads'
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.major_label_text_font_size = '14pt'
        plot.xaxis.major_label_text_font_size = '14pt'
        plot.title.text_font_size = '16pt'

        return plot

    def _draw_readLenHistPlot(self):
        plot = figure(title='Read Lenght Histogram')
        plot.quad(top='readLength', bottom=0, left='left', right='right',
                  source=self.read_hist_src, fill_color='#036463', line_color='#033649')
        plot.xaxis.axis_label = 'Read Length'
        plot.yaxis.axis_label = 'Number of Reads'
        return plot

    def _draw_readDistPlot(self):
        plot = figure()
        plot.quad(top='readPass', bottom=0, left=[5], right=[7])
        plot.quad(top='readFail', bottom=0, left=[1], right=[3])
        return plot

    def _calculate_circle(self, scaffold):
        total = 2 * pi
        contigs = []
        for keys in scaffold.contig_size_dict:
            contigs.append(scaffold.contig_size_dict[keys])
        cum_contig_length = sum(contigs)
        contig_fractions = [float(contig)/cum_contig_length for contig in contigs]
        contig_lengths = [contig * total for contig in contig_fractions]
        x = np.random.random(size=scaffold.nrContigs) * 100
        y = np.random.random(size=scaffold.nrContigs) * 100
        colors = ["#%02x%02x%02x" % (int(r), int(g), 100) for r, g in zip(50+2*x, 30+2*y)]

        start = []
        stop = []
        start_pos = 0
        total_length = 0
        for i in range(len(contig_lengths)):
            start.append(start_pos)
            start_pos += contig_lengths[i]
            total_length += contig_lengths[i]
            stop.append(total_length)

        circle = [start, stop, colors, contigs]
        return circle
