import json
import boto3

client = boto3.client('ses')

def lambda_handler(event, context):

    response = client.send_email(
        Destination={
            'ToAddresses': ['sample@email.com']
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'Your order is submitted.',
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Your Order is Submitted!',
            },
        },
        Source='sample@email.com'
    )
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps("Email Sent Successfully. MessageId is: " + response['MessageId'])
    }