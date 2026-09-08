import boto3
import uuid

s3 = boto3.client("s3")

BUCKET_NAME = "YOUR_BUCKET_NAME"


def lambda_handler(event, context):

    run_id = str(uuid.uuid4())

    objects = []

    # --------------------------------------------------
    # 1. PUT requests
    # Generate 10 PUT requests
    # --------------------------------------------------
    for i in range(10):
        key = f"cloudwatch-lab/{run_id}/file-{i}.txt"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=f"CloudWatch S3 Lab test object {i}".encode()
        )

        objects.append(key)

    # --------------------------------------------------
    # 2. GET requests
    # Generate 10 GET requests
    # --------------------------------------------------
    for key in objects:
        s3.get_object(
            Bucket=BUCKET_NAME,
            Key=key
        )

    # --------------------------------------------------
    # 3. HEAD requests
    # Generate 10 HEAD requests
    # --------------------------------------------------
    for key in objects:
        s3.head_object(
            Bucket=BUCKET_NAME,
            Key=key
        )

    # --------------------------------------------------
    # 4. DELETE requests
    # Generate 5 DELETE requests
    # --------------------------------------------------
    for key in objects[:5]:
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=key
        )

    # --------------------------------------------------
    # 5. Generate 4xx errors
    # Request objects that don't exist
    # --------------------------------------------------
    for i in range(10):
        try:
            s3.get_object(
                Bucket=BUCKET_NAME,
                Key=f"cloudwatch-lab/{run_id}/does-not-exist-{i}.txt"
            )
        except s3.exceptions.NoSuchKey:
            pass
        except Exception:
            pass

    return {
        "statusCode": 200,
        "body": {
            "put_requests": 10,
            "get_requests": 20,
            "delete_requests": 5,
            "expected_4xx_requests": 10
        }
    }
