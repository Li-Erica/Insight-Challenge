import json
from time import mktime, strptime
from collections import deque
import numpy as np
from igraph import Graph, plot
from itertools import combinations
import matplotlib.pyplot as plt


__author__ = 'erica-li'

def main(verbose=True,draw_freq=3):
    """

    :return:
    """
    draw_counter = 0
    htg = hash_tag_graph()


    tweets_path = "C://Users//nate//Documents//coding-challenge-master//data-gen//tweets.txt"
    tweets_path = "/home/nate/coding-challenge/data-gen/tweets.txt"
    with open(tweets_path) as tweets_file:
        for raw_tweet_text in tweets_file:
            raw_tweet_dict = json.loads(raw_tweet_text)

            # everything has a time but we only care about tweets that have at lease two hashtags
            # this is why we test for hashtags first

            try:
                verbose_hash_tags = raw_tweet_dict['entities']['hashtags']

                # Get lowercase version of hashtags & remove duplicate hashtags
                hash_tags = np.unique([d['text'].lower() for d in verbose_hash_tags])

                # Only interested in hahtag sets with at least two hashtags
                if len(hash_tags) >= 2:

                    htg.add_tweet(hash_tag_tuple=hash_tags,
                                  epoch_time=twitter_time_2_epoch_time(raw_tweet_dict['created_at']))

                    if verbose:
                        print("\n")
                        print("Time: "+str(raw_tweet_dict['created_at']))
                        print("Hash Tags: "+str(hash_tags))
                        print("Mean Degree: "+str(htg.get_mean_degree()))

                    if draw_counter >= draw_freq:
                        print("Drawing Graph!")
                        draw_counter = 0
                        htg.draw_graph()
                        plt.show()
                    else:
                        draw_counter += 1


            # keyError happens when raw_tweet_dict doesnt have an entities key,
            #  this most likely means it is a rate limit line and should be passed over
            except KeyError:
                pass
                #print("\nFailure:")
                #print(raw_tweet_dict)
                #print('\nFAIL!!!!')
                #print(raw_tweet_dict)
                #print(raw_tweet_dict['entities']['hashtags'])



    return 1


def twitter_time_2_epoch_time(s):
    """
    Convert twitter time stamp string to integer representation of seconds since epoch


    Tue Mar 29 06:04:51 +0000 2016

    :return:
    """
    #twitter_time_list = s.split(' ')
    pattern = '%a %b %d %H:%M:%S +0000 %Y'
    t_epoch = int(mktime(strptime(s, pattern)))

    return  t_epoch




class hash_tag_graph:


    def __init__(self,window_duration=60,verbose=False):
        """

        :return:
        """
        self.t_window = window_duration
        self.hashtag_deque = deque()
        self.latest_time = 0
        self.graph = Graph()
        self.verbose=verbose


    def trim(self):
        """
        remove edges outside


        :return:
        """

        # identify edges outside window
        min_time = self.latest_time - self.t_window
        edges_to_trim = self.graph.es.select(time_gt=min_time)
        if self.verbose: print("Edges to trim: "+str(edges_to_trim))

        # remove edges outside of t_window
        self.graph.__sub__(edges_to_trim)

        # identify veritces with 0 degree to delet
        vertices_to_trim = self.graph.vs(_degree_eq=0)
        if self.verbose: print("Vertices to trim: "+str(vertices_to_trim))
        self.graph.__sub__(vertices_to_trim)




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

            # Add hashtag to graph as vertex, if its already exists, nothing happens
            for hash_tag in hash_tag_tuple:
                self.graph.add_vertex(name=hash_tag)

            # Add edges with associated epoch time
            for edge in combinations(hash_tag_tuple,r=2):
                if self.verbose: print('Adding Edge Pair:'+str(edge))
                self.graph.add_edge(source=edge[0],target=edge[1],time=epoch_time)

            #trim graph
            self.trim()



        # if tweet is outside of the time window than toss it
        else:
            return



    def get_mean_degree(self):
        """

        :return:
        """

        return np.mean(self.graph.degree())

    def draw_graph(self):
        """

        :return:
        """
        layout = self.graph.layout("circle")
        self.graph.vs["label"] = self.graph.vs["Name"]

        visual_style = {}
        visual_style["vertex_size"] = 50
        visual_style["edge_width"] = 10
        visual_style["layout"] = layout
        visual_style["margin"] = 100
        plot(self.graph, **visual_style)
        plt.show()

        return 0


if __name__ == "__main__":
    main()
