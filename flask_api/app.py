from flask import Flask, jsonify, render_template
from gtfs_helper import get_route_source_destination
import json
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/summary")
def summary():

    file_path = "data/processed/processed_trip_updates.json"

    if not os.path.exists(file_path):
        return jsonify({
            "error": "processed_trip_updates.json not found"
        })

    with open(file_path, "r") as f:
        trips = json.load(f)

    total = len(trips)

    excellent = sum(1 for t in trips if t["status"] == "Excellent")
    good = sum(1 for t in trips if t["status"] == "Good")
    average = sum(1 for t in trips if t["status"] == "Average")
    poor = sum(1 for t in trips if t["status"] == "Poor")
    critical = sum(1 for t in trips if t["status"] == "Critical")

    avg_score = round(
        sum(t["reliability_score"] for t in trips) / total,
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
    
@app.route("/api/live")
def live():

    file_path = "data/processed/processed_trip_updates.json"

    if not os.path.exists(file_path):
        return jsonify([])

    with open(file_path, "r") as f:
        trips = json.load(f)

    return jsonify(trips[:50])

@app.route("/api/search/<route_id>")
def search_route(route_id):

    file_path = "data/processed/processed_trip_updates.json"

    if not os.path.exists(file_path):
        return jsonify({"error": "Data not found"})

    with open(file_path, "r") as f:
        trips = json.load(f)

    filtered = [
        t for t in trips
        if route_id.lower() in t["route_id"].lower()
    ]

    if len(filtered) == 0:
        return jsonify({
            "message": "Route not found"
        })

    total = len(filtered)

    avg_score = round(
        sum(t["reliability_score"] for t in filtered) / total,
        2
    )

    excellent = sum(1 for t in filtered if t["status"] == "Excellent")
    good = sum(1 for t in filtered if t["status"] == "Good")
    average = sum(1 for t in filtered if t["status"] == "Average")
    poor = sum(1 for t in filtered if t["status"] == "Poor")
    critical = sum(1 for t in filtered if t["status"] == "Critical")

    # NEW
    route_short = filtered[0]["route_id"].split()[1]

    source, destination = get_route_source_destination(route_short)

    return jsonify({
        "route": route_id,
        "source": source if source else "Not Available",
        "destination": destination if destination else "Not Available",
        "total_trips": total,
        "average_score": avg_score,
        "excellent": excellent,
        "good": good,
        "average": average,
        "poor": poor,
        "critical": critical
    })


if __name__ == "__main__":
    app.run(debug=True)