import re
from shazamio import Shazam, Serialize

# fetch apple music link from shazam link
async def slink_to_alink(slink):
    shazam = Shazam()
    match = re.search(r"track\/([0-9]+)", slink)
    if match:
        track_id = match.group(1)
        about_track = await shazam.track_about(track_id=track_id)
        serialized = Serialize.track(data=about_track)
        return serialized.apple_music_url
    else: return None

# search shazam for tracks by providing query
async def shazam_search(search_query):
    try:
        shazam = Shazam()
        result = await shazam.search_track(query=search_query, limit=50)
        hits = result.get("tracks").get("hits")
        return hits
    except Exception as e: raise e
        