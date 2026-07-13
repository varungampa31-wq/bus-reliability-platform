from flask import Flask, jsonify, render_template
from gtfs_helper import get_route_source_destination
import json
import os

app = Flask(__name__)

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Batch Layer Output
FILE_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "processed_trip_updates.json"
)

# Speed Layer Output
LIVE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "speed-layer",
    "speed_output.json"
)

# ----------------------------------------------------
# Load Batch Data Once
# ----------------------------------------------------

print("=" * 60)
print("Loading Batch Layer Data...")
print("=" * 60)

if os.path.exists(FILE_PATH):

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        TRIPS = json.load(f)

    print(f"Loaded {len(TRIPS)} trips.")

else:

    print("processed_trip_updates.json not found.")
    TRIPS = []

print("=" * 60)


# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------------------------------
# Batch Layer Summary
# ----------------------------------------------------

@app.route("/api/summary")
def summary():

    if len(TRIPS) == 0:
        return jsonify({
            "error": "No trip data found."
        })

    total = len(TRIPS)

    excellent = sum(
        1 for t in TRIPS
        if t["status"] == "Excellent"
    )

    good = sum(
        1 for t in TRIPS
        if t["status"] == "Good"
    )

    average = sum(
        1 for t in TRIPS
        if t["status"] == "Average"
    )

    poor = sum(
        1 for t in TRIPS
        if t["status"] == "Poor"
    )

    critical = sum(
        1 for t in TRIPS
        if t["status"] == "Critical"
    )

    avg_score = round(
        sum(
            t["reliability_score"]
            for t in TRIPS
        ) / total,
        2
    )

    return jsonify({

        "total_trips": total,
        "average_score": avg_score,
        "excellent": excellent,
        "good": good,
        "average": average,
        "poor": poor,
        "critical": critical

    })


# ----------------------------------------------------
# Speed Layer Summary
# ----------------------------------------------------

@app.route("/api/live-summary")
def live_summary():

    if not os.path.exists(LIVE_FILE):

        return jsonify({

            "total_trips": 0,
            "average_score": 0,
            "excellent": 0,
            "good": 0,
            "average": 0,
            "poor": 0,
            "critical": 0

        })

    with open(LIVE_FILE, "r", encoding="utf-8") as f:

        data = json.load(f)

    return jsonify(data)


# ----------------------------------------------------
# Live Trips Table
# ----------------------------------------------------

@app.route("/api/live")
def live():

    return jsonify(TRIPS[:50])


# ----------------------------------------------------
# Route Search
# ----------------------------------------------------

@app.route("/api/search/<route_id>")
def search_route(route_id):

    filtered = [

        trip

        for trip in TRIPS

        if route_id.lower() in trip["route_id"].lower()

    ]

    if len(filtered) == 0:

        return jsonify({

            "message": "Route not found"

        })

    total = len(filtered)

    avg_score = round(

        sum(
            t["reliability_score"]
            for t in filtered
        ) / total,

        2

    )

    excellent = sum(
        1 for t in filtered
        if t["status"] == "Excellent"
    )

    good = sum(
        1 for t in filtered
        if t["status"] == "Good"
    )

    average = sum(
        1 for t in filtered
        if t["status"] == "Average"
    )

    poor = sum(
        1 for t in filtered
        if t["status"] == "Poor"
    )

    critical = sum(
        1 for t in filtered
        if t["status"] == "Critical"
    )

    try:

        parts = filtered[0]["route_id"].split()

        if len(parts) > 1:
            route_short = parts[1]
        else:
            route_short = filtered[0]["route_id"]

    except Exception:

        route_short = route_id

    source, destination = get_route_source_destination(route_short)

    return jsonify({

        "route": route_short,
        "source": source,
        "destination": destination,
        "total_trips": total,
        "average_score": avg_score,
        "excellent": excellent,
        "good": good,
        "average": average,
        "poor": poor,
        "critical": critical

    })


# ----------------------------------------------------
# Run Flask
# ----------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)