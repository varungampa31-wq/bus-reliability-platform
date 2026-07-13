import boto3
import json
import time
from pathlib import Path

REGION = "us-east-1"
STREAM_NAME = "bus-trip-stream"

kinesis = boto3.client(
    "kinesis",
    region_name=REGION
)

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = BASE_DIR / "data" / "speed-layer" / "speed_output.json"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

response = kinesis.describe_stream(StreamName=STREAM_NAME)

shard_id = response["StreamDescription"]["Shards"][0]["ShardId"]

iterator = kinesis.get_shard_iterator(
    StreamName=STREAM_NAME,
    ShardId=shard_id,
    ShardIteratorType="LATEST"
)["ShardIterator"]

summary = {
    "total_trips": 0,
    "excellent": 0,
    "good": 0,
    "average": 0,
    "poor": 0,
    "critical": 0,
    "average_score": 0
}

scores = []

print("=" * 60)
print("Speed Layer Started...")
print("=" * 60)

while True:

    records = kinesis.get_records(
        ShardIterator=iterator,
        Limit=25
    )

    iterator = records["NextShardIterator"]

    for r in records["Records"]:

        trip = json.loads(
            r["Data"]
        )

        summary["total_trips"] += 1

        status = trip["status"].lower()

        if status in summary:
            summary[status] += 1

        scores.append(
            trip["reliability_score"]
        )

        summary["average_score"] = round(
            sum(scores) / len(scores),
            2
        )

        with open(
            OUTPUT_FILE,
            "w"
        ) as f:

            json.dump(
                summary,
                f,
                indent=4
            )

        print(summary)

    time.sleep(1)