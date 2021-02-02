import tweepy
import os 
from datetime import datetime, date
import boto3
import pytz
from functools import reduce
from collections import Counter
from pytz import timezone
from dateutil.relativedelta import relativedelta
import random

from dynamo_db import dynamo_db
from twitter_api import twitter_api

class dictionary_constructor():

    def __init__(self, user_name: str, hashtags_in: str):
        self.user_name = user_name
        self.hashtags_in = hashtags_in
        self.dict = {}
        self.hashtag_counts = {}
        self.lang_counts = {}
        self.hashtags_totals = {}
        self.db_connect = dynamo_db.set_connection()
        self.twitter_data = twitter_api(user_name=self.user_name, hashtags_in=self.hashtags_in)
        self.dict['date'] = {'S': datetime.today().replace(tzinfo=pytz.UTC).strftime("%d/%m/%Y")}
        self.get_1_yr_tweets_counts()
        self.get_user_stats()
        self.tweet_by_month()
        self.language_of_tweet()
        self.get_hashtag_text_data()
        self.get_random_tweet()
        self.send_dictionary()

    def get_1_yr_tweets_counts(self):
        retweet_count = reduce((lambda x, y: x + y), (i['retweet_count'] for i in self.twitter_data.tweets))
        favourite_count = reduce((lambda x, y: x + y), (i['favorite_count'] for i in self.twitter_data.tweets))
        
        most_retweeted = max(self.twitter_data.tweets, key=lambda x: x['retweet_count'])                
        most_favourited = max(self.twitter_data.tweets, key=lambda x: x['favorite_count'])
        
        self.dict['retweet_count'] = {'N':str(retweet_count)}
        self.dict['favourite_count'] = {'N':str(favourite_count)}
        
        self.dict['most_retweeted_id'] = {'S': str(most_retweeted['id'])}
        # self.dict['most_retweeted_count'] = {'N':str(most_retweeted['retweet_count'])}
        
        self.dict['most_favourited_id'] = {'S': str(most_favourited['id'])}
        # self.dict['most_favourited_count'] = {'N':str(most_favourited['favorite_count'])}
        
    def tweet_by_month(self):
        month_labels = []
        month_retweets = []
        month_favourites = []
        
        for i in range(12):
            favourited_by_month = 0
            retweeted_by_month = 0
            month_start_date = (datetime.today() + relativedelta(months=-i)).replace(tzinfo=timezone('UTC'))
            month_end_date = (datetime.today() + relativedelta(months=-i-1)).replace(tzinfo=timezone('UTC'))
            for tweet in self.twitter_data.tweets:
                tweet_date = (datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y'))
                if month_start_date > tweet_date > month_end_date:
                        retweeted_by_month += tweet['retweet_count']
                        favourited_by_month += tweet['favorite_count']
            
            
            month_labels.append({'S': month_start_date.strftime('%d-%m-%Y')})
            month_retweets.append({'N':str(retweeted_by_month)})
            month_favourites.append({'N':str(favourited_by_month)})

        self.dict['labels'] = {'L':month_labels[::-1]}
        self.dict['retweets'] = {'L':month_retweets[::-1]}
        self.dict['favourites'] = {'L':month_favourites[::-1]}
    
    def get_user_stats(self):
        for items in self.twitter_data.tweets:
            self.dict['followers'] = {'N':str(items['user']['followers_count'])}
            self.dict['statuses'] = {'N':str(len(self.twitter_data.tweets))}
            break
            
    def language_of_tweet(self):
        language_list = []
        for tweet in self.twitter_data.hashtags:
            language_list.append(tweet['lang'])
   
        language_counts = {}
        for n in list(set(language_list)):
            language_counts[n] = language_list.count(n)
        
        language_counts = dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True))

        count = 0
        others = 0
        lang_labels = []
        lang_data = []
        for k,v in language_counts.items():
            if count < 5:
                if k != 'und':
                    lang_labels.append({'S':str(k)})
                    lang_data.append({'N':str(v)})
                    count += 1
                else:
                    count += 1
                    others += v
            else:
                 others += v
        lang_labels.append({'S':'Other'})
        lang_data.append({'N':str(others)})
        
        self.dict['lang_labels'] = {'L':lang_labels}
        self.dict['lang_data'] = {'L':lang_data}
                              
    def get_hashtag_text_data(self):
        hashtags = self.twitter_data.hashtags
        self.dict['total_tweets'] = {'N': str(len(hashtags))}
        tweet_count = 0
        hashtag_list = []
        
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
            self.dict[f'hashtag_{str(position)}_hashtag'] = {'S':str(k)}
            self.dict[f'hashtag_{str(position)}_count'] = {'N':str(v)}
            self.dict[f'hashtag_{str(position)}_percentage'] = {'S': f'{str(int((v/hastag_highest_count*100)))}%'}                
            position +=1
                       
    def get_random_tweet(self):
        hashtags = self.twitter_data.hashtags
        print(hashtags[0])
        random_number = random.randint(0, (len(hashtags)-1))
        self.dict['random_tweet_id'] = {'N': str(hashtags[random_number]['id'])}
        self.dict['random_user_name'] = {'S': str(hashtags[random_number]['user']['screen_name'])}
        self.dict['random_tweet_friends'] = {'N':str(hashtags[random_number]['user']['friends_count'])}
        self.dict['random_tweet_followers'] = {'N': str(hashtags[random_number]['user']['followers_count'])}

    def send_dictionary(self):
        response = self.db_connect.put_item(TableName='balr_twitter',
                                            Item = self.dict
                                            )
        
        
        