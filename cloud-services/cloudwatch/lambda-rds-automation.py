import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds = boto3.client("rds")

DB_INSTANCE_IDENTIFIER = "database-1"

INSTANCE_TYPE_A = "db.t3.micro"
INSTANCE_TYPE_B = "db.t4g.micro"


def get_rds_instance():
    response = rds.describe_db_instances(
        DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER
    )

    return response["DBInstances"][0]


def opposite_instance_type(current_type):
    if current_type == INSTANCE_TYPE_A:
        return INSTANCE_TYPE_B

    if current_type == INSTANCE_TYPE_B:
        return INSTANCE_TYPE_A

    raise ValueError(
        f"Unsupported RDS instance type: {current_type}. "
        f"Expected {INSTANCE_TYPE_A} or {INSTANCE_TYPE_B}."
    )


def change_instance_type(db_instance, new_type):
    current_type = db_instance["DBInstanceClass"]

    if current_type == new_type:
        logger.info(
            "RDS instance type is already %s",
            new_type
        )
        return

    logger.info(
        "Changing RDS instance type from %s to %s",
        current_type,
        new_type
    )

    rds.modify_db_instance(
        DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER,
        DBInstanceClass=new_type,
        ApplyImmediately=True
    )

    logger.info("RDS instance type modification requested")


def start_rds():
    db_instance = get_rds_instance()

    status = db_instance["DBInstanceStatus"]
    current_type = db_instance["DBInstanceClass"]

    logger.info(
        "RDS status=%s, instance_type=%s",
        status,
        current_type
    )

    if status != "stopped":
        logger.info(
            "RDS is not stopped. Current status=%s. Nothing to start.",
            status
        )
        return

    # Determine the new instance type
    new_type = opposite_instance_type(current_type)

    # Change instance class while the DB is stopped.
    #
    # This is important for t3 <-> t4g because this can require
    # a reboot / instance modification.
    change_instance_type(db_instance, new_type)

    # Start RDS
    logger.info("Starting RDS instance")

    rds.start_db_instance(
        DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER
    )

    logger.info(
        "RDS start requested. New instance type=%s",
        new_type
    )


def stop_rds():
    db_instance = get_rds_instance()

    status = db_instance["DBInstanceStatus"]

    logger.info(
        "RDS current status=%s",
        status
    )

    if status == "available":
        logger.info("Stopping RDS instance")

        rds.stop_db_instance(
            DBInstanceIdentifier=DB_INSTANCE_IDENTIFIER
        )

        logger.info("RDS stop requested")

    else:
        logger.info(
            "RDS is not available. Cannot/should not stop it. "
            "Current status=%s",
            status
        )


def handle_scheduler_event(event):
    """
    EventBridge Scheduler:
        available -> stop
        stopped   -> change instance type + start

    Other transitional states are ignored.
    """

    db_instance = get_rds_instance()

    status = db_instance["DBInstanceStatus"]

    logger.info(
        "Scheduler event received. RDS status=%s",
        status
    )

    if status == "available":
        stop_rds()

    elif status == "stopped":
        start_rds()

    else:
        logger.info(
            "RDS is in transitional/non-toggleable state: %s",
            status
        )


def handle_cloudwatch_alarm(event):
    """
    CloudWatch Alarm:
        ALARM -> ensure RDS is running.

    We don't toggle on OK because an OK event immediately after
    an ALARM should not accidentally stop the database.
    """

    alarm_state = event.get("detail", {}).get("state", {}).get("value")

    alarm_name = event.get("detail", {}).get("alarmName")

    logger.info(
        "CloudWatch Alarm event: alarm=%s state=%s",
        alarm_name,
        alarm_state
    )

    if alarm_state != "ALARM":
        logger.info(
            "Alarm state is %s. No RDS action required.",
            alarm_state
        )
        return

    db_instance = get_rds_instance()

    status = db_instance["DBInstanceStatus"]

    logger.info(
        "CloudWatch alarm requires RDS to be running. "
        "Current status=%s",
        status
    )

    if status == "stopped":
        start_rds()

    elif status == "available":
        logger.info("RDS is already running")

    else:
        logger.info(
            "RDS is currently transitioning: %s",
            status
        )


def lambda_handler(event, context):

    logger.info("Received event:")
    logger.info(event)

    source = event.get("source")
    detail_type = event.get("detail-type")

    # ---------------------------------------------------------
    # EventBridge Scheduler
    # ---------------------------------------------------------
    if source == "aws.rds":
        logger.info("Handling RDS Event Change")
        handle_scheduler_event(event)
        return {
            "statusCode": 200,
            "message": "Scheduler event handled"
        }

    # ---------------------------------------------------------
    # EventBridge Scheduler
    # ---------------------------------------------------------
    if source == "aws.scheduler":
        logger.info("Handling EventBridge Scheduler event")
        handle_scheduler_event(event)
        return {
            "statusCode": 200,
            "message": "Scheduler event handled"
        }

    # ---------------------------------------------------------
    # CloudWatch Alarm
    # ---------------------------------------------------------
    if (
        source == "aws.cloudwatch"
        and detail_type == "CloudWatch Alarm State Change"
    ):
        logger.info("Handling CloudWatch Alarm event")
        handle_cloudwatch_alarm(event)

        return {
            "statusCode": 200,
            "message": "CloudWatch alarm event handled"
        }

    # ---------------------------------------------------------
    # Unknown event
    # ---------------------------------------------------------
    logger.info(
        "Unknown event source=%s detail-type=%s",
        source,
        detail_type
    )

    return {
        "statusCode": 200,
        "message": "Event ignored"
    }
