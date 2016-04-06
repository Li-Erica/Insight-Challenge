import numpy as np
from igraph import Graph, plot
from itertools import combinations
import matplotlib
matplotlib.use('SVG')
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

__author__ = 'Erica-Li'



class hash_tag_graph:
    """
    hash tag graph class
    """


    def __init__(self,window_duration=60,verbose=True):
        """
        Initialize the class

        :return: hash_tag_graph object
        """
        self.t_window = window_duration
        self.latest_time = 0
        self.graph = Graph()
        self.verbose=verbose


    def trim(self):
        """
        remove edges outside time window

        :return:  None
        """

        # identify edges outside window

        min_time = self.latest_time - self.t_window
        edges_to_trim = self.graph.es.select(time_lt=min_time)
        if self.verbose: print("Edges to trim: "+str(edges_to_trim))

        # remove edges outside of t_window
        self.graph.delete_edges(edges_to_trim)

        # identify vertices with 0 degree to delete
        vertices_to_trim = self.graph.vs.select(_degree=0)
        if self.verbose: print("Vertices to trim: "+str(vertices_to_trim._name_index))
        self.graph.delete_vertices(vertices_to_trim)




    def add_tweet(self,hash_tag_tuple,epoch_time):
        """

        Adds tweet to hash tag graph and updates graph such that it only contains tweets
        withing window_duration of the latest in time tweet. If tweet is outside of the window_duration
        than it is not added to the graph and nothing happens


        :return:
        """
        # Check if tweet is in order, inside the window duration, or outside
        t_diff = self.latest_time - epoch_time > self.t_window

        if t_diff <= self.t_window:
            self.latest_time = max(epoch_time,self.latest_time)

            current_vertices = self.graph.vs._name_index
            if self.verbose:
                print('Graph name index: '+str(current_vertices))
                print('Graph name index type: '+str(type(current_vertices)))

            # current vertivces will have none type when it is initilazed empty
            if current_vertices is not None:

                # Add hashtag to graph as vertex, if its already exists, nothing happens
                for hash_tag in hash_tag_tuple:
                    # only add hashtag if it isn't already in the graph
                    if hash_tag not in current_vertices:
                        if self.verbose: print("Adding Vertex: "+str(hash_tag))
                        self.graph.add_vertex(name=hash_tag)
            else:
                # Add hashtag to graph as vertex, if its already exists, nothing happens
                for hash_tag in hash_tag_tuple:
                    if self.verbose: print("Adding Vertex: "+str(hash_tag))
                    self.graph.add_vertex(name=hash_tag)



            # Add edges with associated epoch time
            for edge in combinations(hash_tag_tuple,r=2):
                if self.verbose: print('Adding Edge Pair:'+str(edge)+" Time:"+str(epoch_time))

                self.graph.add_edge(source=edge[0],target=edge[1],time=epoch_time)

            self.trim()

        # if tweet is outside of the time window than toss it
        else:
            return

        return



    def get_mean_degree(self):
        """
        Compute the average degree

        :return: np.float, average graph degree
        """

        return np.mean(self.graph.degree())

    def draw_graph(self,path):
        """
        Utlity for visualizing the graph.

        :return: 0
        """
        print("Drawing HashTag Graph!")

        layout = self.graph.layout("kk")

        self.graph.vs["label"] = self.graph.vs["name"]


        visual_style = {}
        visual_style["bbox"] = (1600,1600)
        visual_style["vertex_size"] = 10
        visual_style["edge_width"] = 1
        visual_style["edge_color"] = 'blue'
        visual_style["layout"] = layout
        visual_style["margin"] = 100

        graph_plot = plot(self.graph, **visual_style)
        graph_plot.save(fname=path)

        return 0
