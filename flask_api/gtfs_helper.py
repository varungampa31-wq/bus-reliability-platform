import pandas as pd

GTFS_PATH = "data/gtfs/"


def get_route_source_destination(route_name):

    try:

        routes = pd.read_csv(GTFS_PATH + "routes.txt")
        trips = pd.read_csv(GTFS_PATH + "trips.txt")
        stop_times = pd.read_csv(GTFS_PATH + "stop_times.txt")
        stops = pd.read_csv(GTFS_PATH + "stops.txt")

        route_name = str(route_name).upper()

        # Search using CONTAINS instead of exact match
        route = routes[
            routes["route_short_name"]
            .astype(str)
            .str.upper()
            .str.contains(route_name, na=False)
        ]

        if route.empty:
            return "Unknown", "Unknown"

        route_id = route.iloc[0]["route_id"]

        trip = trips[
            trips["route_id"] == route_id
        ]

        if trip.empty:
            return "Unknown", "Unknown"

        trip_id = trip.iloc[0]["trip_id"]

        trip_stops = stop_times[
            stop_times["trip_id"] == trip_id
        ].sort_values("stop_sequence")

        if trip_stops.empty:
            return "Unknown", "Unknown"

        first_stop = trip_stops.iloc[0]["stop_id"]
        last_stop = trip_stops.iloc[-1]["stop_id"]

        source = stops.loc[
            stops["stop_id"] == first_stop,
            "stop_name"
        ].values[0]

        destination = stops.loc[
            stops["stop_id"] == last_stop,
            "stop_name"
        ].values[0]

        return source, destination

    except Exception as e:
        print("GTFS ERROR:", e)
        return "Unknown", "Unknown"