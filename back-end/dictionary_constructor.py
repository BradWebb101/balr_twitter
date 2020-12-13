import tweepy
import os 
from datetime import datetime, date
import boto3
import pytz
from functools import reduce
from collections import Counter
from pytz import timezone
from dateutil.relativedelta import relativedelta
from dynamo_db import dynamo_db
from twitter_api import twitter_api

class dictionary_constructor():

    def __init__(self, user_name: str, hashtags_in: str):
        self.user_name = user_name
        self.hashtags_in = hashtags_in
        self.db_connect = dynamo_db.set_connection()
        self.twitter_data = twitter_api(user_name=self.user_name, hashtags_in=self.hashtags_in)
        self.date_today = datetime.today().replace(tzinfo=pytz.UTC)
        self.get_1_yr_tweets_counts()
        self.get_user_stats()
        self.tweet_by_month()
        self.get_hashtag_text_data()
        self.get_recent_hashtags_details()
        self.send_dictionary()

    def get_1_yr_tweets_counts(self):
        tweets = self.twitter_data.tweets
        tweet_list = []
        try:
            for items in tweets:
                tweet_list.append({'date':items['created_at'], 'retweets':items['retweet_count'], 'favourites':items['favorite_count'], 'full_text':items['full_text']})
                
            retweet_count = reduce((lambda x, y: x + y), (i['retweets'] for i in tweet_list))
            favourite_count = reduce((lambda x, y: x + y), (i['favourites'] for i in tweet_list))
            
            most_retweeted = max(tweet_list, key=lambda x: x['retweets'])
            most_retweeted = {
                'date_of_tweet':{'S': datetime.strptime(most_retweeted['date'], '%a %b %d %H:%M:%S %z %Y').strftime('%d-%m-%Y')},
                'retweets':{'N':str(most_retweeted['retweets'])},
                'text':{'S':str(most_retweeted['full_text'])}
                }
                    
            most_favourited = max(tweet_list, key=lambda x: x['favourites'])
            most_favourited = {
                'date_of_favourite':{'S': datetime.strptime(most_favourited['date'], '%a %b %d %H:%M:%S %z %Y').strftime('%d-%m-%Y')},
                'favourites':{'N':str(most_favourited['favourites'])},
                'text':{'S':str(most_favourited['full_text'])}
            } 
            
            self.tweet_counts = {
                'retweet_count':{'N':str(retweet_count)}, 
                'favourite_count':{'N':str(favourite_count)}, 
                'most_retweeted':{'M':most_retweeted}, 
                'most_favourited': {'M':most_favourited}
                }
            
        except (TypeError, AttributeError) as e:
            print(e)
            self.tweet_counts = {}

    def tweet_by_month(self):
        tweets = self.twitter_data.tweets
        month_labels = []
        month_retweets = []
        month_favourites = []
        try:
            for i in range(12):
                favourited_by_month = 0
                retweeted_by_month = 0
                month_start_date = (datetime.today() + relativedelta(months=-i)).replace(tzinfo=timezone('UTC'))
                month_end_date = (datetime.today() + relativedelta(months=-i-1)).replace(tzinfo=timezone('UTC'))
                for tweet in tweets:
                    tweet_date = (datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y'))
                    if month_start_date > tweet_date > month_end_date:
                            retweeted_by_month += tweet['retweet_count']
                            favourited_by_month += tweet['favorite_count']
                
                month_labels.append({'S':month_start_date.strftime('%d-%m-%Y')})
                month_retweets.append({'N':str(retweeted_by_month)})
                month_favourites.append({'N':str(favourited_by_month)})
                
                self.tweets_month = {
                        'labels':{'L':month_labels},
                        'retweets':{'L':month_retweets}, 
                        'favourites':{'L':month_favourites}
                }
                
        except (TypeError, AttributeError) as e:
            print(e)
            self.tweets_month = {}
            
    
    def get_user_stats(self):
        tweets = self.twitter_data.tweets
        try:
            for items in tweets:
                self.tweets_user = {
                            'followers': {'N':str(items['user']['followers_count'])},
                            'statuses': {'N':str(items['user']['statuses_count'])}
                            }
                break
            
        except (TypeError, AttributeError) as e:
            print(e)
            self.tweets_user = {}               

    def get_hashtag_text_data(self):
        hashtags = self.twitter_data.hashtags
        tweet_count = 0
        hashtag_list = []
        recent_hashtags = []
        try:
            for item in hashtags:
                tweet_count +=1
                for i in item['entities']['hashtags']:
                    if i['text'] not in self.hashtags_in:
                        hashtag_list.append({'value':i['text']})

            top_5_hashtags_dict = dict(Counter(hashtags['value'] for hashtags in hashtag_list))
            top_5_hashtags_dict = dict(sorted(top_5_hashtags_dict.items(), key=lambda x: x[1], reverse=True)[:5])
            self.top_5_hash = {}
            position = 1
            hastag_highest_count = 0
            for k,v in top_5_hashtags_dict.items():
                if position == 1:
                    hastag_highest_count = v
                self.top_5_hash[str(position)] = {'M':{'hashtag':{'S':str(k)}, 'count':{'N':str(v)}, 'percentage':{'S': f'width: {str(int((v/hastag_highest_count*100)))}%'}}}
                position +=1
            self.top_5_hash['tweet_count'] = {'N':str(tweet_count)}
            self.top_5_hash['recent_hashtags'] = {'L':recent_hashtags}
            
        except (TypeError, AttributeError) as e:
            print(e)
            self.top_5_hash = {}
            
    def get_recent_hashtags_details(self):
        hashtags = self.twitter_data.hashtags
        hashtag_count = 1
        hashtag_list = []
        for tweet in hashtags:
            if hashtag_count <= 5:
                hashtag_dict = {'M':{'created_at': {'S':datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')}, 
                                'screen_name': {'S':str(tweet['user']['screen_name'])},
                                'location':{'S':str(tweet['user']['location'])},
                                'followers_count':{'S':str(tweet['user']['followers_count'])},
                                'friends_count':{'S':str(tweet['user']['friends_count'])}
                                }}            
                hashtag_list.append(hashtag_dict)
            
                hashtag_count +=1
            
        self.recent_hashtags = hashtag_list        
        
    def send_dictionary(self):
        dictionary = {
                    'date': {'S': str(datetime.strftime(self.date_today, '%d-%m-%Y'))}, 
                    'tweet_counts': {'M':self.tweet_counts}, 
                    'tweets_month':{'M':self.tweets_month},
                    'user_stats':{'M':self.tweets_user},
                    'top_5_hashtags': {'M':self.top_5_hash}, 
                    'recent_5_hashtags':{'L':self.recent_hashtags}
                    }
        
        response = self.db_connect.put_item(TableName='balr_twitter',
                                            Item = dictionary
                                            )
       
        