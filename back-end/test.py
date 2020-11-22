# import tweepy
# import os
# from dotenv import load_dotenv
# import datetime

# load_dotenv()

# auth = tweepy.OAuthHandler(os.getenv('API_KEY'), os.getenv('API_KEY_SECRET'))
# auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
# api = tweepy.API(auth) 

# tweets = tweepy.Cursor(api.user_timeline,id='balr').items()

# for items in tweets:
#     print(datetime.datetime.strptime(items._json['created_at'], '%a %b %d %H:%M:%S %z %Y').replace(year=lambda x: x+1))

# import datetime

# print(datetime.datetime.today().strftime('%d-%m-%Y'))



# import botocore.exceptions

# for key, value in sorted(botocore.exceptions.__dict__.items()):
#     if isinstance(value, type):
#         print(key)


from get_data_dict import get_data_dict

data_dict = get_data_dict().data_dict

for k,v in data_dict.items():
    print(k,v)