from gtfs_reader import download_feed

feed = download_feed()

if feed:
    print(f"Downloaded {len(feed)} bytes successfully.")
else:
    print("Download failed.")