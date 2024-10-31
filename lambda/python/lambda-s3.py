import boto3
import json
import uuid
import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'mydata-niranjan'

    if 'http' in event['requestContext']:
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
    else:
        method = event['httpMethod']
        path = event['path']

    if "/resource" in path and method == 'GET':
        parts = path.split("/")
        response = s3.get_object(Bucket=bucket_name, Key=parts[-1])
        response = response['Body'].read().decode('utf-8')
        response = json.loads(response)
    elif "/resource" in path and method == 'POST':
        object_key = str(uuid.uuid4())
        body = event['body']
        metadata = {"country":"IND"}
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)
        # s3.put_object(Bucket=bucket_name, StorageClass='STANDARD_IA', Key=object_key, Body=body)
        # s3.put_object(Bucket=bucket_name, Expires=datetime.datetime(2025, 1, 1), Key=object_key, Body=body)
        # s3.put_object(Bucket=bucket_name, Metadata=metadata, Key=object_key, Body=body)
        response = {'id': object_key}
    elif "/metadata" in path and method == 'GET':
        parts = path.split("/")
        response = s3.head_object(Bucket=bucket_name, Key=parts[-1])
        response = response['Metadata']
    else:
        response = {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
        }
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
