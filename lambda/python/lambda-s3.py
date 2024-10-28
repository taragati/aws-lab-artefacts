import boto3
import json
import uuid

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'myapis-bucket'

    method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if "/apis/resource" in path and method == 'GET':
        parts = path.split("/")
        response = s3.get_object(Bucket=bucket_name, Key=parts[5])
        response = response['Body'].read().decode('utf-8')
    elif "/apis/resource" in path and method == 'POST':
        object_key = str(uuid.uuid4())
        body = event['body']
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=body)
        response = {'id': object_key}
    else:
        response = {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
