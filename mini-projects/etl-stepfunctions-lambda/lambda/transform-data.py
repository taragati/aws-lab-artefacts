import json
import boto3
import uuid

dynamodb = boto3.client('dynamodb')
table_name = 'MYAPIS_TABLE'

def lambda_handler(event, context):

    found = 'false'
    for record in event[0]:
        if record["fraud"] == "Y":
            if record["chequenumber"] in [tran["chequenumber"] for tran in event[1]]:
                found = 'true'
                object_key = str(uuid.uuid4())
                # Example: Insert an item into the table
                dynamodb.put_item(
                    TableName=table_name,
                    Item={
                        'id': {'S': object_key},
                        'role': {'S': 'FRAUD'},
                        'chequenumber': {'S': record['chequenumber']},
                        'issuername': {'S': record['issuername']},
                        'issuerbank': {'S': record['issuerbank']}
                    }
                )

    return {
        'fraud': found
    }
