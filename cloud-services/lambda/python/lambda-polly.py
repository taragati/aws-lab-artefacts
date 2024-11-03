import boto3
import json
import os
from contextlib import closing

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'my-polly-data-niranjan'

    if 'http' in event['requestContext']:
        method = event['requestContext']['http']['method']
        path = event['requestContext']['http']['path']
    else:
        method = event['httpMethod']
        path = event['path']

    if "/speak" in path and method == 'POST':
        body = json.loads(event['body'])
        polly_client = boto3.client('polly')

        response = polly_client.synthesize_speech(
            VoiceId='Joanna',
            LanguageCode='en-US',
            OutputFormat='mp3',
            TextType='text',
            Text = body['text'])

        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = os.path.join('/tmp', body['filename'])
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        s3.upload_file('/tmp/' + body['filename'],bucket_name,body['filename'] + ".mp3")

        response = {'success': 'true'}
    else:
        response = {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
        }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }