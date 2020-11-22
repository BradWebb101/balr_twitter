import tweepy
import os
   
class twitter_api():

    @staticmethod
    def connect() -> object:
        try:
            auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
            auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
            return tweepy.API(auth) 

        except tweepy.TweepError as e:
            print(e)
