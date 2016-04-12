from graphviz import Digraph
from xml.dom import minidom
from bokeh.plotting import figure, output_file, show



# parse the scaffold evidence file.
path = './test_112/scaffold_evidence.txt'
with open(path, 'r') as scaffold_evidence:
    scaffolds = {}
    for line in scaffold_evidence:
        if line[0] == '>':
            cur_scaffold = line.split("|")[0][1:]
            scaffolds[cur_scaffold] = []
        elif line[0] != '\n':
            contig = line.split("|")
            scaffolds[cur_scaffold].append(contig)

dot = Digraph(comment="SSPACE assembly", format='svg')
dot.body.extend(['rankdir=LR', 'size="6,6"'])
dot.engine = 'neato'
# dot.node_attr.update(color='lightblue2', style='filled')
dot.attr('node', shape='circle')
edge_list = []
links_list = []
label_list = []
prev_node = None
for contigs in scaffolds['scaffold1']:

    dot.node(contigs[0], label = contigs[0] + '\n' + contigs[1][4:])
    label_list.append(contigs[0])
    cur_node = contigs[0]
    if prev_node is None:
        prev_node = contigs[0]
        links = contigs[2][5:]
        links_list.append(links)
    else:
        dot.edge(prev_node, cur_node, label=links, len='2.00')

        # edge = prev_node + cur_node
        # edge_list.append(edge)
        prev_node = contigs[0]
        if len(contigs) >= 3:
            links = contigs[2][5:]
            links_list.append(links)
# print(edge_list)
# dot.edges(edge_list)
print(dot.source)

dot.render('graph', view=True)
doc = minidom.parse('graph.svg')
print(doc)
x_pos = [float(ellipse.getAttribute("cx")) for ellipse in doc.getElementsByTagName('ellipse')]
y_pos = [float(ellipse.getAttribute("cy")) * -1 for ellipse in doc.getElementsByTagName('ellipse')]
node_strings = [str(text.firstChild.nodeValue) for text in doc.getElementsByTagName('text')]
x_text = [float(text.getAttribute('x')) - 10 for text in doc.getElementsByTagName('text')]
y_text = [(float(text.getAttribute('y')) - 10) * -1 for text in doc.getElementsByTagName('text')]
polygon = [pts.getAttribute('points') for pts in doc.getElementsByTagName('polygon')]

# print(node_str)

output_file('graph.html')
print(polygon)

p = figure(height=1000, width=1000)
p.circle(x_pos, y_pos, fill_color='white', alpha=0.7, size=25, line_color='black')
p.text(x_text, y_text, text=node_strings)
p.patch([-572.904, -562.799, -568.712, -572.904], [-33.2221, -30.0365, -38.8281, -33.2221])
p.line()

show(p)