import json
import boto3
import os
import uuid
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = "niranjan-pre-data"

def lambda_handler(event, context):
    file_name = event.get("fileName", f"uploads/employee-raw-data.csv")
    file_type = event.get("fileType", "text/csv")

    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_name,
                'ContentType': file_type
            },
            ExpiresIn=60  # 1 Minute
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadUrl": presigned_url,
                "fileKey": file_name
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }