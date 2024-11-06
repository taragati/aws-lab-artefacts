import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('comprehend')

    if 'http' in event['requestContext']:
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
    else:
        method = event['httpMethod']
        path = event['path']

    if "/analyze" in path and method == 'POST':
        body = json.loads(event['body'])
        sentiment = client.detect_sentiment(Text=body['feedback'],LanguageCode='en')['Sentiment']
        response = {'sentiment': sentiment}
    else:
        response = {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }