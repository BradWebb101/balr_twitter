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
        self.data =  self.db.scan(
                TableName='balr_twitter', 
                )['Items']
        
        print(self.data)    


    
if __name__ == '__main__':
    get_data_dict()