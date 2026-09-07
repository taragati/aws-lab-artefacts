import boto3
import uuid

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "YOUR_TABLE_NAME"
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    item_id = str(uuid.uuid4())

    # 2 writes → approximately 2 WCU
    for i in range(2):
        table.put_item(
            Item={
                "id": f"{item_id}-{i}",
                "message": "CloudWatch RCU/WCU Lab"
            }
        )

    # 2 strongly consistent reads → approximately 2 RCU
    for i in range(2):
        table.get_item(
            Key={
                "id": f"{item_id}-{i}"
            },
            ConsistentRead=True
        )

    return {
        "statusCode": 200,
        "body": "Generated approximately 2 WCU and 2 RCU"
    }
