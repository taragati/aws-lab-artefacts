import json
import boto3
import time

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cloudwatch-tracing-lab")


def lambda_handler(event, context):

    item_id = str(event.get("id", "1"))

    # Write to DynamoDB
    table.put_item(
        Item={
            "id": item_id,
            "message": "CloudWatch tracing lab",
            "timestamp": int(time.time())
        }
    )

    # Read from DynamoDB
    response = table.get_item(
        Key={
            "id": item_id
        }
    )

    item = response.get("Item", {})

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "status": "SUCCESS",
            "message": "DynamoDB operation completed"
        })
    }
