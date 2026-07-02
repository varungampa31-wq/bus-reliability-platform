"""
Parses GTFS-Realtime Protocol Buffer data.
"""

from google.transit import gtfs_realtime_pb2


def parse_feed(feed_data):
    """
    Converts raw protobuf data into a FeedMessage object.
    """

    feed = gtfs_realtime_pb2.FeedMessage()

    feed.ParseFromString(feed_data)

    return feed