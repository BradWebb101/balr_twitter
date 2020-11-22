import os
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

class get_data_dict():

    def __init__(self):
        self.db = None
        self.dynamo_connect()
        self.data_dict = {}
        self.get_today_followers()
        self.get_today_hashtags()
        self.get_total_tweets()

    def dynamo_connect(self):
        self.db = boto3.client(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
            )

    def get_today_followers(self):
        try:
            self.data_dict['followers'] =  self.db.get_item(
                TableName='followers', 
                Key={
                    'date':{'S':datetime.today().strftime('%d-%m-%Y')}
                    },
                AttributesToGet = ['date','followers', 'statuses']
                )['Item']
        
            
        except ClientError as e:
            print(e)
            return {}

    def get_today_hashtags(self):
        try:
            self.data_dict['hashtags'] = self.db.get_item(
                TableName='hashtags', 
                Key={
                    'date':{'S':datetime.today().strftime('%d-%m-%Y')}
                    },
                AttributesToGet = ['data', 'total_tweets']
                )['Item']

        except ClientError as e:
            print(e)
            return {}

    def get_total_tweets(self):
        try:
            total_favourites = 0
            total_retweets = 0
            total_tweet_counts = self.db.scan(
                TableName='tweets', 
                AttributesToGet = ['favourite_count', 'retweet_count']
                )['Items']
            for item in total_tweet_counts:
                for k, v in item.items():
                    if k == 'favourite_count':
                        total_favourites += int(v['N'])
                    elif k == 'retweet_count':
                        total_retweets += int(v['N'])
            self.data_dict['total_counts'] = {'total_retweets':total_retweets, 'total_favourites':total_favourites}
                    
        except ClientError as e:
            print(e)
            return {}