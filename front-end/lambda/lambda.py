import os
import boto3
import botocore.exceptions
from datetime import datetime 

def handler(event, context):
    client = boto3.client('dynamodb',
            region_name='eu-west-2')
    
    data = client.get_item(
        TableName='balr_twitter',
        Key={
            'date': {'S':datetime.today().strftime("%d/%m/%Y")}
        }
        )

    return data['Item']

