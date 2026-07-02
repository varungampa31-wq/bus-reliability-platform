"""
Main Producer
Dublin Bus Reliability Intelligence Platform
"""

import json
import os

from gtfs_reader import download_feed
from feed_parser import parse_feed
from feed_parser import extract_trip_updates
from data_cleaner import clean_trip_updates
from reliability import calculate_reliability
from kinesis_producer import send_to_kinesis


OUTPUT_FOLDER = "data/processed"
OUTPUT_FILE = "processed_trip_updates.json"


def save_json(data):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("\n==============================================")
    print("Processed data saved successfully")
    print("==============================================")
    print(f"Location : {output_path}")


def print_summary(data):

    print("\n================ SUMMARY ================")

    print(f"Total Records : {len(data)}")

    excellent = sum(1 for x in data if x["status"] == "Excellent")
    good = sum(1 for x in data if x["status"] == "Good")
    average = sum(1 for x in data if x["status"] == "Average")
    poor = sum(1 for x in data if x["status"] == "Poor")
    critical = sum(1 for x in data if x["status"] == "Critical")

    print(f"Excellent : {excellent}")
    print(f"Good      : {good}")
    print(f"Average   : {average}")
    print(f"Poor      : {poor}")
    print(f"Critical  : {critical}")

    print("=========================================\n")


def main():

    print("=" * 70)
    print("DUBLIN BUS RELIABILITY INTELLIGENCE PLATFORM")
    print("=" * 70)

    print("\nDownloading GTFS Feed...")

    feed_data = download_feed()

    if feed_data is None:
        print("Feed download failed.")
        return

    print("\nParsing Feed...")

    feed = parse_feed(feed_data)

    print("\nExtracting Trip Updates...")

    trips = extract_trip_updates(feed)

    print(f"Trip Updates Extracted : {len(trips)}")

    print("\nCleaning Data...")

    cleaned = clean_trip_updates(trips)

    print(f"Records After Cleaning : {len(cleaned)}")

    print("\nCalculating Reliability Score...")

    processed = calculate_reliability(cleaned)

    save_json(processed)

    print("\nSending records to Amazon Kinesis...")

    send_to_kinesis(processed)

    print_summary(processed)

    print("Producer completed successfully.")


if __name__ == "__main__":
    main()