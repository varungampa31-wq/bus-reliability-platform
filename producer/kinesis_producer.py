"""
Kinesis Producer
Replays processed trip updates to Amazon Kinesis
at a controlled rate (1 record per second).
"""

import json
import time
import boto3
from pathlib import Path

# ---------- AWS Configuration ----------

REGION = "us-east-1"
STREAM_NAME = "bus-trip-stream"

# ---------- Kinesis Client ----------

kinesis = boto3.client(
    "kinesis",
    region_name=REGION
)

# ---------- JSON File ----------

BASE_DIR = Path(__file__).resolve().parent.parent

JSON_FILE = BASE_DIR / "data" / "processed" / "processed_trip_updates.json"


def replay_to_kinesis(delay=1):
    """
    Replay processed JSON records into Kinesis
    at a controlled rate.
    """

    if not JSON_FILE.exists():

        print(f"File not found: {JSON_FILE}")

        return

    with open(JSON_FILE, "r", encoding="utf-8") as file:

        records = json.load(file)

    print("=" * 60)
    print(f"Loaded {len(records)} records")
    print("Starting replay...")
    print("=" * 60)

    total = 0

    for record in records:

        kinesis.put_record(

            StreamName=STREAM_NAME,

            Data=json.dumps(record),

            PartitionKey=str(record["route_id"])

        )

        total += 1

        print(
            f"[{total}] Route: {record['route_id']} | "
            f"Trip: {record['trip_id']} | "
            f"Score: {record['reliability_score']}"
        )

        # Replay one record every second
        time.sleep(delay)

    print("=" * 60)
    print("Replay Completed")
    print("=" * 60)


if __name__ == "__main__":

    replay_to_kinesis(delay=1)
