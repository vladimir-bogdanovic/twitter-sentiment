import re
import os
from dotenv import load_dotenv
import tweepy
from tweepy import OAuthHandler
from textblob import  TextBlob

class TwitterClient(object):
    tweets = []

    def __init__(self):
        load_dotenv()
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+://\S+)", " ", tweet).split())

    def get_tweet_sentiment(self,tweet):
        cleaned_tweet = self.clean_tweet(tweet)
        analysis = TextBlob(cleaned_tweet)

        if analysis > 0:
            return 'positive'
        elif analysis < 0:
            return 'negative'
        else:
            return "neutral"

    def get_tweets(self,query,count = 10):
        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q = query, count = count)

            parsed_tweet = {}

            for tweet in tweets:
                parsed_tweet["text"] = tweet.text
                parsed_tweet["sentiment"] = self.get_tweet_sentiment(tweet)


                if tweet['retweet_count'] > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepyException as e:
            print(f"error: {e}")


def main():

    api = TwitterClient()

    tweets = api.get_tweets("hunter X hunter", 20)

    pos_tweets = [tweet for tweet in tweets if tweet["sentiment"] == "positive"]
    neg_tweets = [tweet for tweet in tweets if tweet["sentiment"] == "negative"]
    neu_tweets = [tweet for tweet in tweets if tweet["sentiment"] == "neutral"]

    print(
        f'''
        There are {len(pos_tweets)} positive tweets.
        There are {len(neg_tweets)} negative tweets.
        There are {len(neu_tweets)} neutral tweets.
        '''
    )

    for tweet in pos_tweets[:5]:
        print(tweet['text'])
    for tweet in neg_tweets[:5]:
        print(tweet['text'])

if __name__ == "__main__":
    main()