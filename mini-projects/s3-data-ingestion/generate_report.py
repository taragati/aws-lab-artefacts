import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    table_name = "Employee_Data"
    bucket_name = "niranjan-post-data"
    output_key = 'processed/salesforce_report.csv'

    table = dynamodb.Table(table_name)

    # Query for sort key = 'Salesforce' under a specific partition key (assuming 'pk')
    response = table.query(
        IndexName="skill-index",
        KeyConditionExpression=Key("skill").eq("Salesforce"),
    )

    items = response.get('Items', [])

    # Generate text content
    report_lines = ["Salesforce Data Export\n======================\n"]
    for item in items:
        line = ', '.join(f"{k}: {v}" for k, v in item.items())
        report_lines.append(line)

    report_content = '\n'.join(report_lines)

    # Upload to S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=report_content.encode('utf-8'),
        ContentType='text/csv'
    )