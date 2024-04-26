import httpx
import json
import asyncio
import math
import aiofiles
import os
import re
from TelegramBot import spotify, httpx_client


# search spotify for tracks, albums
async def spotify_search(query):
    try:
        results = spotify.search(q=query, limit=50, offset=0, type="track,album", market="IN")
        albums = results.get("albums").get("items")
        tracks = results.get("tracks").get("items")
        return albums, tracks
    except Exception as e: raise e

async def get_spotify_data(url):
    
    if "spotify.link" in url:
        async with httpx.AsyncClient() as client:
            url =  await client.get(url)
            url = url.headers['Location']
  
    if "/track/" in url:
        result = spotify.track(url)
        track = result
        track_album= result["album"]
        
        id= track["id"]
        uri= track["uri"]
        url=track["external_urls"]["spotify"]
        name=track["name"]
        artists = track["artists"]
        artist = []
        for i in artists:
            artist.append(i["name"])
        artists = ', '.join(artist)
        title= f'{artists} - {name}'
        duration= track["duration_ms"]
        explicit = track["explicit"]
        disc_number = track["disc_number"]
        track_number=track["track_number"]
        isrc = track["external_ids"]["isrc"]
        preview_url=track["preview_url"]
        markets=track["available_markets"]
        markets = ', '.join(markets)
        album_id=track_album["id"]
        album_uri=track_album["uri"]
        album_url=track_album["external_urls"]["spotify"]
        album_name= track_album["name"]
        album_type = track_album["album_type"]
        album_artists = track_album["artists"]
        album_artist = []
        for i in album_artists:
            album_artist.append(i["name"])
        album_artists = ','.join(album_artist)
        album_release_date = track_album["release_date"]
        total_tracks= track_album["total_tracks"]
        images = track_album["images"]
        for image in images:
            if image["height"] == 640: large = image["url"]
            if image["height"] == 300: medium= image["url"]
            if image["height"] == 64: small = image["url"]
        
        
        text=f"""<figure><img src="{large}"></figure>
<h4>Track</h4><pre>ID            : {id}
URI           : {uri}
URL           : <a href="{url}"<a>{url}</a>

Name          : {name}
Artists       : {artists}
Duration      : {duration} ms
Explicit      : {explicit}
Disc No       : {disc_number}
Track No      : {track_number}
ISRC          : {isrc}
Preview       : <a href="{preview_url}"<a>{preview_url}</a>
</pre>
<h4>From Album</h4>
<pre>ID            : {album_id}
URI           : {album_uri}
URL           : <a href="{album_url}"<a>{album_url}</a>

Name          : {album_name}
Type          : {album_type}
Artists       : {album_artists}
Release Date  : {album_release_date}
Total Tracks  : {total_tracks}
</pre>
<h4>Cover</h4><pre> 64 x  64     : <a href="{small}"<a>{small}</a>
300 x 300     : <a href="{medium}"<a>{medium}</a>
600 x 600     : <a href="{large}"<a>{large}</a>
</pre>
<h4>Available Markets</h4>
{markets}
"""
        return text, title
    elif "/album/" in url:
        result = spotify.album(url)
        album= result
        album_tracks=result["tracks"]["items"]
        
        album_id=album["id"]
        album_uri=album["uri"]
        album_url=album["external_urls"]["spotify"]
        album_name= album["name"]
        album_type = album["album_type"]
        album_artists = album["artists"]
        artist = []
        for i in album_artists:
            artist.append(i["name"])
        album_artists= ', '.join(artist)
        title= f'{album_artists} - {album_name}'
        markets = album["available_markets"]
        markets = ', '.join(markets)
        album_release_date = album["release_date"]
        label = album["label"]
        upc = album["external_ids"]["upc"]
        total_tracks= album["total_tracks"]
        images = album["images"]
        for image in images:
            if image["height"] == 640: large = image["url"]
            if image["height"] == 300: medium= image["url"]
            if image["height"] == 64: small = image["url"]
        count=0
        t=""
        for track in album_tracks:
            count+=1
            track_id= track["id"]
            track_uri= track["uri"]
            track_url=track["external_urls"]["spotify"]
            track_name=track["name"]
            track_artists = track["artists"]
            track_artist = []
            for i in track_artists:
                track_artist.append(i["name"])
            track_artists = ','.join(track_artist)
            track_duration= track["duration_ms"]
            explicit = track["explicit"]
            disc_number = track["disc_number"]
            track_number=track["track_number"]
            preview_url=track["preview_url"]
            t+=f"""
<strong>{count}. {track_name}</strong>
<pre>ID            : {track_id}
URI           : {track_uri}
URL           : <a href="{track_url}"<a>{track_url}</a>

Name          : {track_name}
Artists       : {track_artists}
Duration      : {track_duration} ms
Explicit      : {explicit}
Disc No       : {disc_number}
Track No      : {track_number}
Preview       : <a href="{preview_url}"<a>{preview_url}</a>
</pre>
"""
        
        text=f"""<figure><img src="{large}"></figure>
<h4>Album</h4><pre>ID            : {album_id}
URI           : {album_uri}
URL           : <a href="{album_url}"<a>{album_url}</a>

Name          : {album_name}
Type          : {album_type}
Artists       : {album_artists}
Release Date  : {album_release_date}
Label         : {label}
Total Tracks  : {total_tracks}
UPC           : {upc}
</pre>
<h4>Cover</h4><pre> 64 x  64     : <a href="{small}"<a>{small}</a>
300 x 300     : <a href="{medium}"<a>{medium}</a>
600 x 600     : <a href="{large}"<a>{large}</a>
</pre>
<h4>Tracks</h4>
{t}
<h4>Available Markets</h4>
{markets}
"""
        return text, title

async def get_spotify_preview(url):

    try:
        result = spotify.track(url)
        preview=result["preview_url"]
    except:
        preview=None
    return preview
