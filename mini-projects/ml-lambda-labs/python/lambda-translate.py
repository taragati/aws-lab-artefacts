import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('translate')

    if 'http' in event['requestContext']:
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
    else:
        method = event['httpMethod']
        path = event['path']

    if "/translate" in path and method == 'POST':
        body = json.loads(event['body'])
        result = client.translate_text(Text=body['text'],SourceLanguageCode='en', TargetLanguageCode='de')
        response = {'result': result['TranslatedText']}
    else:
        response = {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }