import json
__author__ = 'erica-li'

def main():
    """

    :return:
    """
    tweets_path = "C://Users//nate//Documents//coding-challenge-master//data-gen//tweets.txt"
    tweets_path = "/home/nate/coding-challenge/data-gen/tweets.txt"
    with open(tweets_path) as tweets_file:
        for raw_tweet_text in tweets_file:
            raw_tweet_dict = json.loads(raw_tweet_text)

            # everything has a time but we only care about tweets that have at lease two hashtags
            # this is why we test for hashtags first

            try:
                verbose_hash_tags = raw_tweet_dict['entities']['hashtags']


                hash_tags = [d['text'].lower() for d in verbose_hash_tags]
                if len(hash_tags) >= 2:


                    print("\n")
                    print("Time: "+str(raw_tweet_dict['created_at']))
                    print("Hash Tags: "+str(hash_tags))
                    #print("Hash Tags: "+str([unicode(s,'utf-8') for s in hash_tags]))


            except KeyError:
                pass
                print("\nFailure:")
                print(raw_tweet_dict)
                #print('\nFAIL!!!!')
                #print(raw_tweet_dict)
                #print(raw_tweet_dict['entities']['hashtags'])



    return 1


class hash_tag_graph:

    def __init__(self):
        """

        :return:
        """


    def get_mean_degree(self):
        """

        :return:
        """

    def draw_graph(self):
        """

        :return:
        """


if __name__ == "__main__":
    main()
