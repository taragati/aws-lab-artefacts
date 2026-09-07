import json
import logging
import random
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    timestamp = datetime.now(timezone.utc).isoformat()

    # Simulate a batch job status for the lab.
    # Occasionally generate a failure so the CloudWatch alarm can be tested.
    # 0.1 is high occurance
    success = random.random() > 0.1

    if success:
        status = "SUCCESS"
        logger.info(
            json.dumps({
                "event": "batch_job_completed",
                "status": status,
                "job_name": "demo-batch-job",
                "timestamp": timestamp,
                "message": "Batch job completed successfully"
            })
        )
    else:
        status = "FAILED"
        logger.error(
            json.dumps({
                "event": "batch_job_completed",
                "status": status,
                "job_name": "demo-batch-job",
                "timestamp": timestamp,
                "message": "Batch job failed"
            })
        )

    return {
        "statusCode": 200,
        "status": status
    }
