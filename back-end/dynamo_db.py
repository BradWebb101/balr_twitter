import boto3
import os
from botocore.exceptions import ClientError 

class dynamo_db():
    
    @staticmethod
    def set_connection():
        try:
            return boto3.client('dynamodb',
            region_name='eu-west-2')

        except ClientError as e:
            print(e)