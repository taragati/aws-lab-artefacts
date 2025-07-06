import json
import boto3
import os
import uuid
from datetime import datetime
import csv
from io import StringIO

s3 = boto3.client('s3')

BUCKET_NAME = "niranjan-post-data"

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        reader = csv.DictReader(StringIO(content))

        output = StringIO()
        fieldnames = ['id', 'full_name'] + [f for f in reader.fieldnames if f not in ['first_name', 'middle_name', 'last_name']]
        print(fieldnames)
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            full_name = f"{row.get('first_name', '')} {row.get('middle_name', '')} {row.get('last_name', '')}".strip()
            new_row = {
                'id': str(uuid.uuid4()),
                'full_name': full_name
            }
            for f in fieldnames:
                if f not in ['id', 'full_name']:
                    new_row[f] = row.get(f, '')
            writer.writerow(new_row)

        output.seek(0)
        processed_key = key.replace("uploads/", "processed/")

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=processed_key,
            Body=output.getvalue(),
            ContentType='text/csv'
        )