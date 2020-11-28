import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta
   
class twitter_api():
   
    def __init__(self, user_name:str, hashtags_in:list):
        self.user_name = user_name
        self.hashtags_in = hashtags_in
        self.api = None
        self.tweets = None
        self.hashtags = None
        self.connect()
        self.hashtags = self.twitter_hashtags_requests()
        self.tweets = self.twitter_user_requests()
        
    def connect(self) -> object:
        try:
            auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
            auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
            self.api = tweepy.API(auth, wait_on_rate_limit=True, retry_errors=[429,500, 502,503,504], timeout=60, retry_delay=60, retry_count=10) 

        except tweepy.TweepError as e:
            print(e)
            
    def twitter_hashtags_requests(self) -> object:
        hashtag_list = []
        try: 
            hashtags = tweepy.Cursor(self.api.search, q=self.hashtags_in, result_type='recent', tweet_mode='extended').items(1000)
            for tweet in hashtags:
                if (datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y')) > (datetime.today() + relativedelta(years=-1)).replace(tzinfo=timezone('UTC')):
                    hashtag_list.append(tweet._json)    

            return hashtag_list
        
        except tweepy.TweepError as e:
            print(e)

    def twitter_user_requests(self) -> object:
        user_tweet_list = []
        try: 
            user_tweets = tweepy.Cursor(self.api.user_timeline, id=self.user_name, result_type='recent', tweet_mode='extended').items(1000)
            for tweet in user_tweets:
                if (datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y')) > (datetime.today() + relativedelta(years=-1)).replace(tzinfo=timezone('UTC')):
                    user_tweet_list.append(tweet._json)    

            return user_tweet_list
        
        except tweepy.TweepError as e:
            print(e)
            
