__author__ = 'erica-li'

__author__ = 'nate'
from igraph import *
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("/home/nate/Desktop/Workbook1.csv")
df.set_index('Name',inplace=True)

cdf = df.T.corr()
print(cdf)



def mat_2_graph(df,threshold=.5):
    """

    :return:
    """

    X = df.values
    g = Graph()
    n,m  = df.shape
    g.add_vertices(n)

    edge_pairs = []

    for i in range(n):
        for j in range(i):
            if i != j:
                if X[i,j] >= threshold:
                    edge_pairs.append((i,j))


    g.add_edges(edge_pairs)

    g.vs["Name"] = df.columns.values
    g.vs["node_type"] = [s[0] for s in df.columns.values]

    color_dict = {"T": "orange", "G": "grey"}
    g.vs["color"] = [color_dict[t] for t in g.vs["node_type"]]

    print("Displaying")
    layout = g.layout("circle")
    g.vs["label"] = g.vs["Name"]

    visual_style = {}
    visual_style["vertex_size"] = 50
    visual_style["edge_width"] = 10
    visual_style["layout"] = layout
    visual_style["margin"] = 100
    graph_plot = plot(g, **visual_style)
    graph_plot.show()
    graph_plot.save(fname='/home/nate/pic.png')


mat_2_graph(cdf)


#sns.heatmap(cdf)
#plt.show()
