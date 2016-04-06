__author__ = 'Erica Li'

import sys
import json
import numpy as np
from time import mktime, strptime
from Hash_Tag_Graph import hash_tag_graph




def main():
    """

    :return:
    """
    htg = hash_tag_graph(window_duration=60,verbose=False)

    # Get paths from user input
    input_tweet_path = sys.argv[1]
    output_tweet_path = sys.argv[2]

    # Check if paths are valid



    with open(output_tweet_path,mode='w') as output_file:

        with open(input_tweet_path,mode='r') as tweets_file:
            for raw_tweet_text in tweets_file:
                raw_tweet_dict = json.loads(raw_tweet_text)

                # everything has a time but we only care about tweets that have at lease two hashtags
                # this is why we test for hashtags first
                try:
                    verbose_hash_tags = raw_tweet_dict['entities']['hashtags']

                    # Get lowercase version of hashtags & remove duplicate hashtags
                    hash_tags = np.unique([d['text'].lower() for d in verbose_hash_tags])

                    # Only interested in hashtag sets with at least two hashtags
                    if len(hash_tags) >= 2:

                        htg.add_tweet(hash_tag_tuple=hash_tags,
                                      epoch_time=twitter_time_2_epoch_time(raw_tweet_dict['created_at']))

                        # Write output to new line of outputfile
                        output_file.write("{0:.2f}\n".format(htg.get_mean_degree()))


                # keyError happens when raw_tweet_dict doesnt have an entities key,
                #  this most likely means it is a rate limit line and should be passed over
                except KeyError:
                    pass


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



if __name__ == "__main__":
    main()