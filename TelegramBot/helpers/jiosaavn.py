import httpx, json
from TelegramBot import httpx_client

async def jiosaavn(link):
    null = None
    if "/album/" in link:
        
        params = {'link': f"{link}"}
        response = await httpx_client.get('https://jiosaavn-api-gray.vercel.app/albums', params=params, timeout=60)

        if response.status_code == httpx.codes.OK:
            result = response.json()

        album = result.get("data")

        album_id= album["id"]
        album_link= album["url"]
        album_name= album["name"]
        album_year= album["year"]
        album_releasedate= album["releaseDate"]
        tracks_count= album["songCount"]

        album_artists= album["artists"]
        album_partists= album["primaryArtists"]
        album_fartists= album["featuredArtists"]
        title= f'{album_artists} - {album_name}'
        images= album.get("image")
        for image in images:
            if image['quality'] == '50x50': small= image['link']
            if image['quality'] == '150x150': medium= image['link']
            if image['quality'] == '500x500': large= image['link']
         
        album_tracks=album.get("songs")
        count = 0
        text= ""
        for track in album_tracks:
            count += 1
            track_id= track["id"]
            track_link= track["url"]
            track_name= track["name"]
            track_duration= track["duration"]
            track_lang= track["language"]
            has_explicit= track["explicitContent"]
            has_lyrics= track["hasLyrics"]
            track_playcount= track["playCount"]
            track_label= track["label"]
            copyright= track["copyright"]
        
            track_partists= track["primaryArtists"]
            track_fartists= track["featuredArtists"]
        
            down_links= track["downloadUrl"]
        
            for down_link in down_links:
                if down_link['quality'] == '12kbps': sortahighish= down_link['link']
                if down_link['quality'] == '48kbps': lesshigh= down_link['link']
                if down_link['quality'] == '96kbps': prettyhigh= down_link['link']
                if down_link['quality'] == '160kbps': reallyhigh= down_link['link']
                if down_link['quality'] == '320kbps': superduperhigh= down_link['link']
            text += f"""
<strong>{count}. {track_name}</strong>
<pre>ID               : {track_id}
URL              : <a href="{track_link}">{track_link}</a>
Name             : {track_name}
Duration         : {track_duration} s
Language         : {track_lang}
Explicit         : {has_explicit}
Lyrics           : {has_lyrics}
Play Count       : {track_playcount}
Label            : {track_label}
Copyright        : {copyright}

Primary Artists  : {track_partists}
Featured Artists : {track_fartists}

<u>Streaming URL</u>

12  kbps         : <a href="{sortahighish}"<a>{sortahighish}</a>
48  kbps         : <a href="{lesshigh}"<a>{lesshigh}</a>
96  kbps         : <a href="{prettyhigh}"<a>{prettyhigh}</a>
160 kbps         : <a href="{reallyhigh}"<a>{reallyhigh}</a>
320 kbps         : <a href="{superduperhigh}"<a>{superduperhigh}</a>
</pre>
"""
        message=f"""<figure><img src="{large}"></figure>
<h4>Album</h4>
<pre>ID               : {album_id}
URL              : <a href="{album_link}"<a>{album_link}</a>
Name             : {album_name}
Artists          : {album_artists}
Primary Artists  : {album_partists}
Featured Artists : {album_fartists}
Year             : {album_year}
Release Date     : {album_releasedate}
Tracks Count     : {tracks_count}
</pre>
<h4>Cover</h4>
<pre> 50 x  50        : <a href="{small}"<a>{small}</a>
150 x 150        : <a href="{medium}"<a>{medium}</a>
500 x 500        : <a href="{large}"<a>{large}</a>
</pre>
<h4>Tracks</h4>
{text}
"""
        return message, title
    elif "/song/" in link:
        
        params = {'link': f"{link}"}
        response = await httpx_client.get('https://jiosaavn-api-gray.vercel.app/songs', params=params, timeout=60)

        if response.status_code == httpx.codes.OK:
            result = response.json()

        track = result.get("data")[0]

        track_id= track["id"]
        track_link= track["url"]
        track_name= track["name"]
        track_year= track["year"]
        track_releasedate= track["releaseDate"]
        track_duration= track["duration"]
        track_lang= track["language"]
        has_explicit= track["explicitContent"]
        has_lyrics= track["hasLyrics"]
        track_playcount= track["playCount"]
        track_label= track["label"]
        copyright= track["copyright"]
    
        track_partists= track["primaryArtists"]
        track_fartists= track["featuredArtists"]
        title= f'{track_partists} - {track_name}'
        track_album_name= track["album"]["name"]
        track_album_id = track["album"]["id"]
        track_album_link= track["album"]["url"]
        
        images= track.get("image")
        for image in images:
            if image['quality'] == '50x50': small= image['link']
            if image['quality'] == '150x150': medium= image['link']
            if image['quality'] == '500x500': large= image['link']
    
        down_links= track.get("downloadUrl")
        for down_link in down_links:
            if down_link['quality'] == '12kbps': sortahighish= down_link['link']
            if down_link['quality'] == '48kbps': lesshigh= down_link['link']
            if down_link['quality'] == '96kbps': prettyhigh= down_link['link']
            if down_link['quality'] == '160kbps': reallyhigh= down_link['link']
            if down_link['quality'] == '320kbps': superduperhigh= down_link['link']
        
        message= f"""<figure><img src="{large}"></figure>
<h4>Track</h4>
<pre>ID               : {track_id}
URL              : <a href="{track_link}">{track_link}</a>
Name             : {track_name}
Primary Artists  : {track_partists}
Featured Artists : {track_fartists}
Year             : {track_year}
Release Date     : {track_releasedate}
Duration         : {track_duration} s
Language         : {track_lang}
Explicit         : {has_explicit}
Lyrics           : {has_lyrics}
Play Count       : {track_playcount}
Label            : {track_label}
Copyright        : {copyright}
</pre>
<h4>From Album</h4>
<pre>Name             : {track_album_name}
ID               : {track_album_id}
URL              : <a href="{track_album_link}"<a>{track_album_link}</a>
</pre>
<h4>Cover</h4>
<pre> 50 x  50        : <a href="{small}"<a>{small}</a>
150 x 150        : <a href="{medium}"<a>{medium}</a>
500 x 500        : <a href="{large}"<a>{large}</a>
</pre>
<h4>Streaming URL</h4>
<pre>12  kbps         : <a href="{sortahighish}"<a>{sortahighish}</a>
48  kbps         : <a href="{lesshigh}"<a>{lesshigh}</a>
96  kbps         : <a href="{prettyhigh}"<a>{prettyhigh}</a>
160 kbps         : <a href="{reallyhigh}"<a>{reallyhigh}</a>
320 kbps         : <a href="{superduperhigh}"<a>{superduperhigh}</a>
</pre>
"""
        return message, title
    

