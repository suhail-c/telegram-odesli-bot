import re
import json
import m3u8
import httpx
from TelegramBot.logging import LOGGER
from TelegramBot import httpx_client

async def get_token():
    
    response = await httpx_client.get("https://music.apple.com/us/album/positions-deluxe-edition/1553944254")
    jspath = re.search("crossorigin src=\"(/assets/index.+?\.js)\"", response.text).group(1)
    response = await httpx_client.get("https://music.apple.com"+jspath)
    tkn = re.search(r"(eyJhbGc.+?)\"", response.text).group(1)
    return tkn

async def get_applem_info(link): 
    apple_rx= re.compile(r"apple\.com\/(\w\w)\/album\/.+\/(\d+|pl\..+)(?:\?i=(\d+))*")
    match= apple_rx.search(link)
    if not match.group(3):
        region, id_, __ = match.groups()
        tkn = await get_token()
        headers = {'origin': 'https://music.apple.com','Authorization': f'Bearer {tkn}',}
        params = {'extend': 'extendedAssetUrls',}
        response = await httpx_client.get(f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{id_}/', params=params, headers=headers)
        album= response.json()["data"][0]
        
        id=album["id"]
        link=album["attributes"]["url"]
        
        name=album["attributes"]["name"]
        artists=album["attributes"]["artistName"]
        release_date=album["attributes"]["releaseDate"]
        genere=album["attributes"]["genreNames"]
        genere=', '.join(genere)
        total_tracks=album["attributes"]["trackCount"]
        upc=album["attributes"]["upc"]
        rating=album["attributes"].get("contentRating", "Clean")
        label=album["attributes"]["recordLabel"]
        copyright=album["attributes"]["copyright"]
        
        isSingle=album["attributes"]["isSingle"]
        isCompilation=album["attributes"]["isCompilation"]
        isPrerelease=album["attributes"]["isPrerelease"]
        isComplete=album["attributes"]["isComplete"]
        
        audiotraits=album["attributes"]["audioTraits"]
        audiotraits=' • '.join(audiotraits)
        isMasteredForItunes=album["attributes"]["isMasteredForItunes"]
        
        try:
            editorialNotes=album["attributes"]["editorialNotes"]["short"]
            editorialNotes+= '<br><br>' + album["attributes"]["editorialNotes"]["standard"]
        except:
            editorialNotes="Null"

        cover=album["attributes"]["artwork"]["url"].format(w=album["attributes"]["artwork"]["width"], h=album["attributes"]["artwork"]["height"])
        title= f"{artists} - {name}"

        tracks=album["relationships"]["tracks"]["data"]
        text=""
        for track in tracks:
            track_id=track["id"]
            track_url=track["attributes"]["url"]
            
            track_name=track["attributes"]["name"]
            track_artists=track["attributes"]["artistName"]
            track_duration=track["attributes"]["durationInMillis"]
            track_composer=track["attributes"].get("composerName", "")
            track_genere=track["attributes"]["genreNames"]
            track_genere=', '.join(track_genere)
            track_rls_date=track["attributes"].get("releaseDate", "")
            track_disc_no=track["attributes"].get("discNumber", "")
            track_track_no=track["attributes"]["trackNumber"]
            track_rating=track["attributes"].get("contentRating", "Clean")
            track_locale=track["attributes"].get("audioLocale", "")
            track_isrc=track["attributes"]["isrc"]
            
            track_hasLyrics=track["attributes"].get("hasLyrics", "False")
            track_hasTimeSyncedLyrics=track["attributes"].get("hasTimeSyncedLyrics", "False")
            track_hasCredits=track["attributes"].get("hasCredits", "False")
            
            track_isVocalAttenuationAllowed=track["attributes"].get("isVocalAttenuationAllowed", "False")
            track_isAppleDigitalMaster=track["attributes"].get("isAppleDigitalMaster", "False")
            track_isMasteredForItunes=track["attributes"].get("isMasteredForItunes", "False")
            try:
                track_audiitraits=track["attributes"]["audioTraits"]
                track_audiitraits=' • '.join(track_audiitraits)
            except: track_audiitraits=""
            try: track_preview=track["attributes"]["previews"][0]["url"]
            except: track_preview=""
            try: track_cover=track["attributes"]["artwork"]["url"].format(w=track["attributes"]["artwork"]["width"], h=track["attributes"]["artwork"]["height"])
            except: track_cover=""

            try:
                hls=track["attributes"]["extendedAssetUrls"]["enhancedHls"]
                playlist = m3u8.parse(m3u8.load(hls).dumps())
                streams=""
                for stream in playlist['playlists']:
                    codec= stream['stream_info']['codecs']
                    audio= stream['stream_info']['audio']
                    streams+=f"• {codec} | {audio}<br>"
            except: streams=""

            text+=f"""<strong>{track_track_no}. {track_name}</strong>
<pre>ID             : {track_id}
URL            : <a href="{track_url}">{track_url}</a>

Name           : {track_name}
Artist         : {track_artists}
Composer       : {track_composer}
Duration       : {track_duration} ms
Genre          : {track_genere}
Release Date   : {track_rls_date}
Disc No        : {track_disc_no}
Track No       : {track_track_no}
Content Rating : {track_rating}
Locale         : {track_locale}
ISRC           : {track_isrc}
Quality        : {track_audiitraits}
Cover          : <a href="{track_cover}">{track_cover}</a>
Preview        : <a href="{track_preview}">{track_preview}</a>

Has Credits              : {track_hasCredits}
Has Lyrics               : {track_hasLyrics}
Has Time synced Lyrics   : {track_hasTimeSyncedLyrics}

Is Apple Digital Master      : {track_isAppleDigitalMaster}
Is Mastered For Itunes       : {track_isMasteredForItunes}
Is Vocal Attenuation Allowed : {track_isVocalAttenuationAllowed}

<u>Available Streams</u>
{streams}</pre>
"""        
                    
        message=f"""<figure><img src="{cover}"></figure>
<h4>Album</h4>
<pre>ID             : {id}
URL            : <a href="{link}">{link}</a>
 
Name           : {name}
Artist         : {artists}
Genre          : {genere}
Release Date   : {release_date}
Total Tracks   : {total_tracks}
UPC            : {upc}
Content Rating : {rating}
Label          : {label}
Copyright      : {copyright}
Quality        : {audiotraits}
Cover          : <a href="{cover}">{cover}</a>

Is Single      : {isSingle}
Is Compilation : {isCompilation}
Is Pre-release : {isPrerelease}
Is Complete    : {isComplete}
is Mastered For Itunes : {isMasteredForItunes}
</pre>
<h4>Tracks</h4>
{text}
<h4>Editorial Notes</h4>
{editorialNotes}
"""
        return message, title

    elif match.group(3):
        region, __, id_ = match.groups()
        tkn = await get_token()
        headers = {'origin': 'https://music.apple.com','Authorization': f'Bearer {tkn}',}
        params = {'extend': 'extendedAssetUrls',}
        response = await httpx_client.get(f'https://amp-api.music.apple.com/v1/catalog/{region}/songs/{id_}/', params=params, headers=headers)
        track= response.json()["data"][0]

        track_id=track["id"]
        track_url=track["attributes"]["url"]
        
        track_name=track["attributes"]["name"]
        track_artists=track["attributes"]["artistName"]
        track_album= track["attributes"]["albumName"]
        track_duration=track["attributes"]["durationInMillis"]
        track_composer=track["attributes"].get("composerName", "")
        track_genere=track["attributes"]["genreNames"]
        track_genere=', '.join(track_genere)
        track_rls_date=track["attributes"].get("releaseDate", "")
        track_disc_no=track["attributes"].get("discNumber", "")
        track_track_no=track["attributes"]["trackNumber"]
        track_rating=track["attributes"].get("contentRating", "Clean")
        track_locale=track["attributes"].get("audioLocale", "")
        track_isrc=track["attributes"]["isrc"]
        
        track_hasLyrics=track["attributes"].get("hasLyrics", "False")
        track_hasTimeSyncedLyrics=track["attributes"].get("hasTimeSyncedLyrics", "False")
        track_hasCredits=track["attributes"].get("hasCredits", "False")
        
        track_isVocalAttenuationAllowed=track["attributes"].get("isVocalAttenuationAllowed", "False")
        track_isAppleDigitalMaster=track["attributes"].get("isAppleDigitalMaster", "False")
        track_isMasteredForItunes=track["attributes"].get("isMasteredForItunes", "False")
        try:
            track_audiitraits=track["attributes"]["audioTraits"]
            track_audiitraits=' • '.join(track_audiitraits)
        except: track_audiitraits=""
        try: track_preview=track["attributes"]["previews"][0]["url"]
        except: track_preview=""
        try: track_cover=track["attributes"]["artwork"]["url"].format(w=track["attributes"]["artwork"]["width"], h=track["attributes"]["artwork"]["height"])
        except: track_cover=""
        
        title= f"{track_artists} - {track_name}"
        try:
            hls=track["attributes"]["extendedAssetUrls"]["enhancedHls"]
            playlist = m3u8.parse(m3u8.load(hls).dumps())
            streams=""
            for stream in playlist['playlists']:
                codec= stream['stream_info']['codecs']
                audio= stream['stream_info']['audio']
                streams+=f"• {codec} | {audio}<br>"
        except: streams=""

        message=f"""<figure><img src="{track_cover}"></figure>
<h4>Track</h4>
<pre>ID             : {track_id}
URL            : <a href="{track_url}">{track_url}</a>

Name           : {track_name}
Album          : {track_album}
Artist         : {track_artists}
Composer       : {track_composer}
Duration       : {track_duration} ms
Genre          : {track_genere}
Release Date   : {track_rls_date}
Disc No        : {track_disc_no}
Track No       : {track_track_no}
Content Rating : {track_rating}
Locale         : {track_locale}
ISRC           : {track_isrc}
Quality        : {track_audiitraits}
Cover          : <a href="{track_cover}">{track_cover}</a>
Preview        : <a href="{track_preview}">{track_preview}</a>

Has Credits              : {track_hasCredits}
Has Lyrics               : {track_hasLyrics}
Has Time synced Lyrics   : {track_hasTimeSyncedLyrics}

Is Apple Digital Master      : {track_isAppleDigitalMaster}
Is Mastered For Itunes       : {track_isMasteredForItunes}
Is Vocal Attenuation Allowed : {track_isVocalAttenuationAllowed}

<u>Available Streams</u>
{streams}</pre>
"""
        return message, title 