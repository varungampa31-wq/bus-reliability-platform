"""
GTFS Realtime Feed Reader
Downloads the GTFS-Realtime feed from the NTA API.
"""

import requests

from config import GTFS_API_KEY, GTFS_FEED_URL


def download_feed():
    """
    Downloads the GTFS-Realtime feed.

    Returns:
        bytes: Raw protobuf data if successful.
        None: If the download fails.
    """

    headers = {
        "Cache-Control": "no-cache",
        "x-api-key": GTFS_API_KEY
    }

    try:

        print("Connecting to GTFS-Realtime API...")

        response = requests.get(
            GTFS_FEED_URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        print("Feed downloaded successfully.")

        return response.content

    except requests.exceptions.RequestException as error:

        print(f"Download failed: {error}")

        return None
