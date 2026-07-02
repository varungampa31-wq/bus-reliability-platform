"""
Test script for extracting Trip Updates.
"""

from gtfs_reader import download_feed
from feed_parser import parse_feed
from feed_parser import extract_trip_updates


def main():

    print("Downloading GTFS Feed...\n")

    feed_data = download_feed()

    if feed_data is None:
        print("Download Failed")
        return

    print("Parsing Feed...\n")

    feed = parse_feed(feed_data)

    print("Extracting Trip Updates...\n")

    trips = extract_trip_updates(feed)

    print("=" * 70)
    print(f"Total Trip Updates : {len(trips)}")
    print("=" * 70)

    print("\nFirst 10 Trip Updates\n")

    for index, trip in enumerate(trips[:10], start=1):

        print(f"Trip {index}")

        print(f"Trip ID                : {trip['trip_id']}")
        print(f"Route ID               : {trip['route_id']}")
        print(f"Start Date             : {trip['start_date']}")
        print(f"Schedule Relationship  : {trip['schedule_relationship']}")
        print(f"Stop Updates           : {trip['number_of_stop_updates']}")

        print("-" * 70)


if __name__ == "__main__":
    main()