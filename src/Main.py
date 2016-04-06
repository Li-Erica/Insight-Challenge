import json
import numpy as np
from time import mktime, strptime
from Hash_Tag_Graph import hash_tag_graph


__author__ = 'erica-li'


def main(verbose=True,draw_freq=50):
    """

    :return:
    """
    draw_counter = 0
    next_draw = draw_counter + draw_freq
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


                    if verbose:
                        print("\n")
                        print("Time: "+str(raw_tweet_dict['created_at']))
                        print("Hash Tags: "+str(hash_tags))


                    htg.add_tweet(hash_tag_tuple=hash_tags,
                                  epoch_time=twitter_time_2_epoch_time(raw_tweet_dict['created_at']))


                    if verbose: print("Mean Degree: "+str(htg.get_mean_degree()))

                    if draw_counter >= next_draw:
                        next_draw += draw_freq
                        htg.draw_graph(path='/home/nate/Twitter_Graph_#'+str(draw_counter)+'.png')
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




if __name__ == "__main__":
    main()
