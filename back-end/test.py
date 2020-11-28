import os
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class get_data_dict():

    def __init__(self):
        self.db = None
        self.relative_days = 0
        self.dynamo_connect()
        self.get_most_recent_data()
        

    def dynamo_connect(self):
        self.db = boto3.client(
            'dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
            )
        
    def get_most_recent_data(self):
        todays_date = datetime.today() + timedelta(days=-self.relative_days)
        self.relative_days += 1
        try:
            if self.relative_days <= 7 :
                response = self.db.get_item(
                        TableName='balr_twitter', 
                        Key={
                            'date':{'S':todays_date.strftime('%d-%m-%Y')}
                            },
                        )['Items']
                return response
            else:
                return {}
        
        except KeyError as e:
            self.get_most_recent_data()
               







# import tweepy
# from dotenv import load_dotenv
# import os
# from datetime import datetime
# from dateutil.relativedelta import relativedelta

# load_dotenv()

# auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
# auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
# api = tweepy.API(auth)

# def tweet_test():
#     try:
#         tweet_list = []
#         for i in range(10):
#             tweets = api.search(q='balr', result_type='recent', tweet_mode='extended', page=i)
#             if tweets:
#                 for tweet in tweets:
#                     tweet_list.append(tweet)       
#         return tweet_list  
        
#     except tweepy.TweepError as e:
#         print(e)
#         return []
       
    
# tweets = tweet_test()    
# if tweets:
#     print('List has values')
    
# else:
#     print('List has no values')



