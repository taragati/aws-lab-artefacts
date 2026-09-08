import boto3
import uuid

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = "niranjan_table"
table = dynamodb.Table(TABLE_NAME)

# ~2 KB payload
MESSAGE = "%TRAINING%" * 2000


def lambda_handler(event, context):

    item_id = str(uuid.uuid4())

    # 2 writes
    # Each item is > 1 KB, so each write consumes ~2 WCU
    for i in range(2):
        table.put_item(
            Item={
                "id": f"{item_id}-{i}",
                "message": MESSAGE
            }
        )

    # 2 strongly consistent reads
    # Each item is < 4 KB, so each read consumes ~1 RCU
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
