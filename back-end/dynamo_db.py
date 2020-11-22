import boto3
import os
from botocore.exceptions import ClientError 

class dynamo_db():
    
    @staticmethod
    def set_connection():
        try:
            return boto3.client('dynamodb',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION'))

        except ClientError as e:
            print(e)