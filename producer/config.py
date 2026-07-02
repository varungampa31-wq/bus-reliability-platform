"""
Configuration file for the Dublin Bus Reliability Platform
"""

# ------------------------------------------------------------------
# GTFS Feed Configuration
# ------------------------------------------------------------------

# We will add the actual TFI GTFS feed URL later.
GTFS_FEED_URL = ""

# Time (in seconds) between feed downloads
FETCH_INTERVAL = 30

# ------------------------------------------------------------------
# Local Storage Configuration
# ------------------------------------------------------------------

RAW_DATA_FOLDER = "data/raw"

RAW_DATA_FILE = "vehicle_data.json"

# ------------------------------------------------------------------
# Project Information
# ------------------------------------------------------------------

PROJECT_NAME = "Bus Reliability Platform"

DATA_SOURCE = "Transport for Ireland (GTFS-Realtime)"