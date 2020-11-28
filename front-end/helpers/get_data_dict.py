import os
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class get_data_dict():

    def __init__(self):
        self.db = None
        self.data = None
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
            if self.relative_days < 7:
                self.data =  self.db.get_item(
                        TableName='balr_twitter', 
                        Key={
                            'date':{'S':todays_date.strftime('%d-%m-%Y')}
                            },
                        )['Item']

            else:
                self.data = None
        
        except KeyError as e:
            self.get_most_recent_data()
            
        except Exception as e:
            return None
    
