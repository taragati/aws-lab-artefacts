import json

def lambda_handler(event, context):

    path = event.get("path", "")

    if path == "/error":
        raise Exception("Simulated backend failure")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "status": "SUCCESS",
            "message": "Hello from API Gateway CloudWatch Lab"
        })
    }
