"""
Kinesis Producer
Sends processed trip updates to Amazon Kinesis.
"""

import json
import boto3

# ---------- AWS Configuration ----------

REGION = "us-east-1"
STREAM_NAME = "bus-trip-stream"

# Create Kinesis Client
kinesis = boto3.client(
    "kinesis",
    region_name=REGION
)


def send_to_kinesis(records):
    """
    Sends trip updates to Amazon Kinesis.
    """

    total = 0

    for record in records:

        kinesis.put_record(

            StreamName=STREAM_NAME,

            Data=json.dumps(record),

            PartitionKey=record["route_id"]

        )

        total += 1

    print("=" * 60)
    print(f"Successfully sent {total} records to Kinesis")
    print("=" * 60)