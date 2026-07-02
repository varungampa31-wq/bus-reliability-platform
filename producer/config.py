"""
Configuration file for Bus Reliability Platform
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------------------------------------
# API Configuration
# -------------------------------------------------------

GTFS_API_KEY = os.getenv("GTFS_API_KEY")

GTFS_FEED_URL = os.getenv("GTFS_FEED_URL")

FETCH_INTERVAL = 30

# -------------------------------------------------------
# Local Storage
# -------------------------------------------------------

RAW_DATA_FOLDER = "data/raw"

RAW_DATA_FILE = "vehicle_data.json"

# -------------------------------------------------------
# Project
# -------------------------------------------------------

PROJECT_NAME = "Bus Reliability Platform"