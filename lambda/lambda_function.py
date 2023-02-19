import os
import boto3

DEFAULT_REGION = 'us-west-2'
DEFAULT_CLUSTER = 'minecraft'
DEFAULT_SERVICE = 'minecraft-server'

REGION = os.environ.get('REGION', DEFAULT_REGION)
CLUSTER = os.environ.get('CLUSTER', DEFAULT_CLUSTER)
SERVICE = os.environ.get('SERVICE', DEFAULT_SERVICE)
ENABLED_STR = os.environ.get('ENABLED')
ENABLED = True if ENABLED_STR.upper() == "TRUE" else False

if REGION is None or CLUSTER is None or SERVICE is None:
    raise ValueError("Missing environment variables")


def lambda_handler(event, context):
    """Updates the desired count for a service."""

    if not ENABLED:
        print("server disabled. not updating desired count.")
        return

    ecs = boto3.client('ecs', region_name=REGION)
    response = ecs.describe_services(
        cluster=CLUSTER,
        services=[SERVICE],
    )

    desired = response["services"][0]["desiredCount"]

    if desired == 0:
        ecs.update_service(
            cluster=CLUSTER,
            service=SERVICE,
            desiredCount=1,
        )
        print("Updated desiredCount to 1")
    else:
        print("desiredCount already at 1")
