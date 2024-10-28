import boto3
import json
import uuid

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    table_name = 'MYAPIS_TABLE'

    method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    if "/apis/resource" in path and method == 'GET':
        # Example: Get all items from the table
        parts = path.split("/")
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'id': {'S': parts[-1]},
                'role': {'S': 'Admin'}
            }
        )
        response = response['Item']
        response['version'] = 'v1'
    elif "/apis/resource" in path and method == 'POST':
        object_key = str(uuid.uuid4())
        # Example: Insert an item into the table
        body = json.loads(event['body'])
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'id': {'S': object_key},
                'role': {'S': body['role']},
                'title': {'S': body['title']}
            }
        )
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
