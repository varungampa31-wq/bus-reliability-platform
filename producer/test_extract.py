from gtfs_reader import download_feed
from feed_parser import parse_feed

feed_data = download_feed()
feed = parse_feed(feed_data)

print(f"Total entities: {len(feed.entity)}")

for i, entity in enumerate(feed.entity[:5]):
    print(f"\nEntity {i+1}")

    print("Has Vehicle :", entity.HasField("vehicle"))
    print("Has Trip    :", entity.HasField("trip_update"))
    print("Has Alert   :", entity.HasField("alert"))