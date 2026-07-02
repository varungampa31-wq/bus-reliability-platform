from gtfs_reader import download_feed
from feed_parser import parse_feed

feed_data = download_feed()

feed = parse_feed(feed_data)

print("=" * 50)
print("GTFS Feed Successfully Parsed")
print("=" * 50)

print(f"Number of entities: {len(feed.entity)}")