"""
Configuration file
"""

config = {
    # URL of REST API for video manifest
    'videos_manifest_url': 'https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json',

    # Name of SQLight database file
    'database_name': 'video.db',

    # How often to sync data from video manifest REST API to local database (in seconds)
    'video_manifest_refresh_interval': 10*60
}
