import os
import boto3
import json
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    http_method = event.get("httpMethod", "")
    if http_method == "POST":
        item_id = str(uuid.uuid4())
        body = json.loads(event.get("body", "{}"))
        message = body.get("message", "Hello from Lambda!")

        table.put_item(Item={"id": item_id, "message": message})
        return {
            "statusCode": 200,
            "body": json.dumps({"id": item_id, "message": message})
        }

    elif http_method == "GET":
        resp = table.scan(Limit=10)
        return {
            "statusCode": 200,
            "body": json.dumps(resp.get("Items", []))
        }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported method"})
    }