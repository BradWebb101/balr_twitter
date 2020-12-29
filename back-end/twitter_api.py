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
            self.api = tweepy.API(auth)
            
        except tweepy.TweepError as e:
            print(e)
            
    def twitter_hashtags_requests(self) -> object:
        try:
            hashtag_list = []
            current_id = None
            process = True
            while process == True:   
                hashtags = self.api.search(q=self.hashtags_in, result_type='recent', tweet_mode='extended', max_id=current_id)
                for tweet in hashtags:
                    if datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone('UTC')) > (datetime.today() + relativedelta(days=-7)).replace(tzinfo=timezone('UTC')):
                        hashtag_list.append(tweet._json)
                                            
                    else:
                        process = False       
                         
                current_id = hashtag_list[-1]['id']
                
            return hashtag_list
        
        except tweepy.TweepError as e:
            print(e)
            
    def twitter_user_requests(self) -> object:
        user_tweet_list = []
        try: 
            page_number = 1
            user_tweet_date = datetime.today().replace(tzinfo=timezone('UTC'))
            while user_tweet_date > (datetime.today() + relativedelta(years=-1)).replace(tzinfo=timezone('UTC')):
                user_tweets = self.api.user_timeline(id=self.user_name, result_type='recent', tweet_mode='extended', page=page_number)
                for tweet in user_tweets:
                    user_tweet_list.append(tweet._json)
                    user_tweet_date = datetime.strptime(user_tweet_list[-1]['created_at'], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone('UTC'))   
                page_number += 1    

            return user_tweet_list
        
        except tweepy.TweepError as e:
            print(e)
            
 