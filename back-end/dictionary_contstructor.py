import tweepy
import os 
import datetime
import boto3
import pytz
from collections import Counter
from dynamo_db import dynamo_db
from twitter_api import twitter_api

class dictionary_constructor():

    def __init__(self, user_name='balr'):
        self.api = twitter_api.connect()
        self.dynamo_db = dynamo_db.set_connection()
        self.user_name = user_name
        self.get_1_yr_tweets()
        self.get_user_stats()
        self.get_hashtag_data()

    def get_1_yr_tweets(self):
        try:
            tweets = tweepy.Cursor(self.api.user_timeline, id=self.user_name, since=(datetime.datetime.today() - datetime.timedelta(days=366))).items()
            table='tweets'
            for items in tweets:
                if datetime.datetime.strptime(items._json['created_at'], '%a %b %d %H:%M:%S %z %Y') < (datetime.datetime.today().replace(tzinfo=pytz.UTC) - datetime.timedelta(days=365)):
                    pass
                else:
                    data_dict = {
                                'id': {'S':items._json['id_str']},
                                'date': {'S':datetime.datetime.strptime(items._json['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%d-%m-%Y')},
                                'retweet_count': {'N':str(items._json['retweet_count'])},
                                'favourite_count': {'N':str(items._json['favorite_count'])},
                                'text': {'S':items._json['text']},
                                'TTL': {'N':str((datetime.datetime.strptime(items._json['created_at'], '%a %b %d %H:%M:%S %z %Y')  + datetime.timedelta(days=365)).timestamp())}
                                } 
                    self.dynamo_db.put_item(TableName=table, Item=data_dict)
        except Exception as e:
            print(e)

    def get_user_stats(self):
        try:
            stats = tweepy.Cursor(self.api.user_timeline, id=self.user_name).items(1)
            table='followers'
            for items in stats:
                data_dict={
                            'date': {'S':datetime.datetime.today().strftime('%d-%m-%Y')},
                            'followers': {'N':str(items._json['user']['followers_count'])},
                            'statuses': {'N':str(items._json['user']['statuses_count'])}
                            }
                self.dynamo_db.put_item(TableName=table, Item=data_dict)
 
        except Exception as e:
            print(e)
            
    def get_hashtag_data(self):
        try:
            hashtag_list = []
            hashtag = ['balr','BALR','Balr']
            tweets = tweepy.Cursor(self.api.search, q=hashtag).items(1000)
            table='hashtags'
            tweet_count = 0
            for item in tweets:
                tweet_count +=1
                for i in item._json['entities']['hashtags']:
                    if i['text'] not in hashtag:
                        hashtag_list.append({'value':i['text']})

            hashtag_list = dict(Counter(hashtags['value'] for hashtags in hashtag_list))
            hashtags = dict(sorted(hashtag_list.items(), key=lambda x: x[1], reverse=True)[:5])
            hashtag_dict = {}
            for hashtag, count in hashtags.items():
                hashtag_dict[hashtag] = {'N':str(count)}
            data_dict = {
                        'date':{'S': datetime.datetime.today().strftime('%d-%m-%Y')},
                        'data': {'M':hashtag_dict},
                        'total_tweets': {'N':str(tweet_count)}
                        }
            self.dynamo_db.put_item(TableName=table, Item=data_dict)

        except Exception as e:
            print(e)
        
 