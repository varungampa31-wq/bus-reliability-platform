"""
Main Producer for Dublin Bus Reliability Platform
Downloads GTFS Trip Updates and saves them as JSON.
"""

import json
import os

from gtfs_reader import download_feed
from feed_parser import parse_feed
from feed_parser import extract_trip_updates


OUTPUT_FOLDER = "data/raw"
OUTPUT_FILE = "trip_updates.json"


def save_json(data):

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("\n==========================================")
    print("Data saved successfully")
    print("==========================================")
    print(f"Location : {output_path}")


def main():

    print("=" * 70)
    print("DUBLIN BUS RELIABILITY PLATFORM")
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

    print(f"\nTotal Trip Updates : {len(trips)}")

    save_json(trips)

    print("\nProducer completed successfully.")


if __name__ == "__main__":
    main()