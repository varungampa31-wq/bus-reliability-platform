"""
Parses GTFS-Realtime feed and extracts useful information.
"""

from google.transit import gtfs_realtime_pb2


def parse_feed(feed_data):
    """
    Converts raw protobuf data into a FeedMessage object.
    """

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_data)

    return feed


def extract_trip_updates(feed):
    """
    Extracts Trip Update information from the GTFS feed.
    """

    trips = []

    for entity in feed.entity:

        if entity.HasField("trip_update"):

            trip_update = entity.trip_update

            trip_info = trip_update.trip

            trip = {
                "trip_id": trip_info.trip_id,
                "route_id": trip_info.route_id,
                "start_date": trip_info.start_date,
                "schedule_relationship": str(trip_info.schedule_relationship),
                "number_of_stop_updates": len(trip_update.stop_time_update)
            }

            trips.append(trip)

    return trips