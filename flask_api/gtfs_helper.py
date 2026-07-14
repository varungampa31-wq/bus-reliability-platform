"""
GTFS Helper
Returns Source and Destination for a Route
Memory Optimized Version
"""

import os
import pandas as pd

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GTFS_DIR = os.path.join(BASE_DIR, "data", "gtfs")


# ---------------------------------------------------
# Function
# ---------------------------------------------------

def get_route_source_destination(route_name):

    try:

        route_name = str(route_name).strip().upper()

        # Load only required columns

        routes = pd.read_csv(
            os.path.join(GTFS_DIR, "routes.txt"),
            usecols=["route_id", "route_short_name"]
        )

        trips = pd.read_csv(
            os.path.join(GTFS_DIR, "trips.txt"),
            usecols=["route_id", "trip_id"]
        )

        stop_times = pd.read_csv(
            os.path.join(GTFS_DIR, "stop_times.txt"),
            usecols=["trip_id", "stop_id", "stop_sequence"]
        )

        stops = pd.read_csv(
            os.path.join(GTFS_DIR, "stops.txt"),
            usecols=["stop_id", "stop_name"]
        )

        # ------------------------------------------------

        route = routes[
            routes["route_short_name"]
            .astype(str)
            .str.upper()
            == route_name
        ]

        if route.empty:

            route = routes[
                routes["route_short_name"]
                .astype(str)
                .str.upper()
                .str.contains(route_name, na=False)
            ]

        if route.empty:
            return "Unknown", "Unknown"

        route_id = route.iloc[0]["route_id"]

        # ------------------------------------------------

        trip = trips[
            trips["route_id"] == route_id
        ]

        if trip.empty:
            return "Unknown", "Unknown"

        trip_id = trip.iloc[0]["trip_id"]

        # ------------------------------------------------

        trip_stop_times = stop_times[
            stop_times["trip_id"] == trip_id
        ]

        if trip_stop_times.empty:
            return "Unknown", "Unknown"

        trip_stop_times = trip_stop_times.sort_values(
            "stop_sequence"
        )

        first_stop = trip_stop_times.iloc[0]["stop_id"]

        last_stop = trip_stop_times.iloc[-1]["stop_id"]

        # ------------------------------------------------

        source = stops.loc[
            stops["stop_id"] == first_stop,
            "stop_name"
        ]

        destination = stops.loc[
            stops["stop_id"] == last_stop,
            "stop_name"
        ]

        if source.empty or destination.empty:
            return "Unknown", "Unknown"

        return source.values[0], destination.values[0]

    except Exception as e:

        print("=" * 60)
        print("GTFS ERROR")
        print(e)
        print("=" * 60)

        return "Unknown", "Unknown"
