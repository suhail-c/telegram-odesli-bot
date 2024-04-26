import json
import httpx
import uuid
import asyncio

from pyrogram import Client, enums
from pyrogram.types import (Message, CallbackQuery, InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery)
from TelegramBot import bot, odesli
from TelegramBot.logging import LOGGER
from TelegramBot.database.sqdb import *
from TelegramBot.helpers.constants import *
from TelegramBot.helpers.shazam import *
from TelegramBot.helpers.spotify import *

from TelegramBot.helpers.odesli.entity.song.SongResult import SongResult
from TelegramBot.helpers.odesli.entity.album.AlbumResult import AlbumResult


async def fetch_links(client: Client, message: Message, song_link):
    
    reply = await message.reply_text("__Fetching links, please wait... (This may take a minute)__",  quote=True)
    await bot.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    try: result = await odesli.getByUrl(song_link)
    except Exception as e:
        LOGGER(__name__).error(e)
        try: r = await songwhip_full(song_link)
        except:
            if message.chat.type == enums.ChatType.PRIVATE:
                await reply.edit_text(URL_ERROR)
                await bot.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
                return
            else: 
                await reply.delete()
                await bot.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
                return
        else:
            await reply.edit_text(r, disable_web_page_preview=True) 
            if message.chat.type == enums.ChatType.PRIVATE:
                await message.reply_text(RATE_TXT, disable_web_page_preview=True)
            return

    if isinstance(result, SongResult):
        entity = result.song
        providers = result.songsByProvider
        try: 
            spotify= providers['spotify'].linksByPlatform['spotify']
            preview= await get_spotify_preview(spotify)
        except: preview= None
        r = '**' + entity.title + "** by **" + entity.artistName + '** \n\n[Odesli](' + result.songLink + ')'
        if preview: r = f"[\u2061]({preview})" + r
    elif isinstance(result, AlbumResult):
        preview= None
        entity = result.album
        providers = result.albumsByProvider
        r = '**' + entity.title + "** by **" + entity.artistName + '** \n\n[Odesli](' + result.albumLink + ')'	
    else:
        await reply.edit_text(URL_ERROR)
        return

    op = []
    for provider in providers:
        if provider == 'youtube':
            r += (" | [YouTube](" + providers['youtube'].linksByPlatform['youtube'] + ') | [YT Music](' +
            providers['youtube'].linksByPlatform['youtubeMusic'] + ')')
            op.append("youtube")
            continue
        elif provider == 'itunes':
            r += (" | [Apple Music](" + providers['itunes'].linksByPlatform['appleMusic'] + ')')
            op.append("itunes")
            continue
        elif provider == 'amazon':
            r += (' | [Amazon Music](' +
            providers['amazon'].linksByPlatform['amazonMusic'] + ')')
            op.append("amazon")
            continue
        else:
            r += ' | [' + (provider.title() + '](' + providers[provider].linksByPlatform[provider] + ')')
            op.append(provider)

    t = r
    t += "\n\n__Checking songwhip.com for additional links, please wait...__"

    reply = await reply.edit_text(t, disable_web_page_preview=True)
    await bot.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)

    try: r = await songwhip(song_link, r, op)
    finally: 
        if preview: await reply.edit_text(f"{r}\n\n<pre>♪ Preview</pre>") 
        else: await reply.edit_text(r, disable_web_page_preview=True)

    #if message.chat.type == enums.ChatType.PRIVATE:
    #await message.reply_text(RATE_TXT, disable_web_page_preview=True)

async def songwhip(song_link, r, op):
    async with httpx.AsyncClient() as client:
        data = {'country': 'IN', 'url': song_link}
        response = await client.post('https://songwhip.com/api/songwhip/create', json=data, timeout=60)
        response.raise_for_status()
        if response.status_code == httpx.codes.OK:
            try:
                x = response.json()
                tmp = "https://songwhip.com/" + x.get("data").get("item").get("url")
                r += f" | [Songwhip]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("qobuz")[0].get("link")
                r += f" | [Qobuz]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("jioSaavn")[0].get("link")
                r += f" | [JioSaavn]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("gaana")[0].get("link")
                r += f" | [Gaana]({tmp})"
            except: pass

            if 'spotify' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("spotify")[0].get("link")
                    r += f" | [Spotify]({tmp})"
                except: pass
            if 'deezer' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("deezer")[0].get("link")
                    r += f" | [Deezer]({tmp})"
                except: pass
            if 'tidal' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("tidal")[0].get("link")
                    r += f" | [Tidal]({tmp})"
                except: pass
            if 'amazon' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("amazonMusic")[0].get("link")
                    r += f" | [Amazon Music]({tmp})"
                except: pass
            if 'itunes' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("itunes")[0].get("link")
                    tmp = tmp.replace("{country}", "gb", 1)
                    r += f" | [Apple Music]({tmp})"
                except: pass
            if 'napster' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("napster")[0].get("link")
                    r += f" | [Napster]({tmp})"
                except: pass
            if 'linemusic' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("lineMusic")[0].get("link")
                    r += f" | [Line Music]({tmp})"
                except: pass
            if 'youtube' not in op:
                try:
                    tmp = x.get("data").get("item").get("links").get("youtube")[0].get("link")
                    tmp1 = x.get("data").get("item").get("links").get("youtubeMusic")[0].get("link")
                    r += f" | [Youtube]({tmp}) | [Youtube Music]({tmp1})"
                except: pass
            return r
        else: return r
    
async def get_inline_result_link(client: Client, inline_query: InlineQuery, song_link):
    
    try: result = await odesli.getByUrl(song_link)
    except Exception as e:
        LOGGER(__name__).error(e)
        await inline_query.answer(
        switch_pm_text="Odesli - On demand smart links",
        switch_pm_parameter="help",
        results=[
            InlineQueryResultArticle(
                title="Error",
                description="There's a problem with that URL. Try one from a different music service.",
                thumb_url="https://telegra.ph/file/bd6b2365a405a8b73b033.png",
                thumb_height=512,
                thumb_width=512,
                input_message_content=InputTextMessageContent(INFO),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Open Bot", url="https://t.me/tgodeslibot")
                        ]
                    ]
                )
            )      
        ]
    )
        return 
   
    if isinstance(result, SongResult):
        entity = result.song
        title = entity.title
        artist = entity.artistName
        thumb = entity.thumbnailUrl
        
    elif isinstance(result, AlbumResult):
        entity = result.album
        title = entity.title
        artist = entity.artistName
        thumb = entity.thumbnailUrl
        	

    r = '**' + title + '** by **' + artist + '**'
    await inline_query.answer(
        switch_pm_text="Odesli - On demand smart links",
        switch_pm_parameter="help",
        results=[
            InlineQueryResultPhoto(
                title=title,
                description=artist,
                thumb_url=thumb,
                photo_url=thumb,
                caption=r,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🌐 Fetching links...", callback_data="LOADING_BUTTON")]
                    ]
                )
            )      
        ]
    )

async def get_inline_result_query(client: Client, inline_query: InlineQuery):

    query = inline_query.query.strip()
    try: hits = await shazam_search(query)     
    except Exception as e:
        LOGGER(__name__).error(e)
        await inline_query.answer(
            switch_pm_text="Odesli - On demand smart links",
            switch_pm_parameter="help",
            results=[
                InlineQueryResultArticle(
                    title="No results found",
                    description="No results found for your query. Try different query or paste link of desired song",
                    thumb_url="https://telegra.ph/file/bd6b2365a405a8b73b033.png",
                    input_message_content=InputTextMessageContent(INFO),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Open Bot", url="https://t.me/tgodeslibot")
                            ]
                        ]
                    )
                )      
            ]
        )
        return
    
    results=[]
    await create_database()
    for i in hits:
        id = uuid.uuid4()
        title = i.get("heading").get("title")
        artist = i.get("heading").get("subtitle")
        thumb = i.get("images").get("default")
        if thumb is None: thumb = "https://graph.org/file/a6145bf65a88feefaf6ac.jpg"
        slink = i.get("url")
        try: link = i.get("stores").get("apple").get("actions")[0].get("uri")
        except: link = slink
        caption= '**' + title + '** by **'+ artist+ '**'
        await store_values(str(id), link)
        results.append(
            InlineQueryResultPhoto(
                title=title,
                description=artist,
                thumb_url=thumb,
                photo_url=thumb,
                caption=caption,
                id=id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🌐 Fetching links...", callback_data="LOADING_BUTTON")]
                    ]
                )
            )        
        )
    if results: await inline_query.answer(results, switch_pm_text="Odesli - On demand smart links", switch_pm_parameter="help")

async def get_inline_result_spotify(client: Client, inline_query: InlineQuery, query, type):
    
    try: albums, tracks = await spotify_search(query)     
    except Exception as e:
        LOGGER(__name__).error(e)
        await inline_query.answer(
            switch_pm_text="Odesli - On demand smart links",
            switch_pm_parameter="help",
            results=[
                InlineQueryResultArticle(
                    title="No results found",
                    description="No results found for your query. Try different query or paste link of desired song",
                    thumb_url="https://telegra.ph/file/bd6b2365a405a8b73b033.png",
                    input_message_content=InputTextMessageContent(INFO),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Open Bot", url="https://t.me/tgodeslibot")
                            ]
                        ]
                    )
                )      
            ]
        )
        return
    
    results=[]
    await create_database()
    if type=='a':
        for album in albums:
            id = uuid.uuid4()
            album_name = album.get("name")
            album_artists = album.get("artists")
            if len(album_artists) > 1:
                artist_names = []
                for artist in album_artists:
                    artist_names.append(artist.get("name"))
                album_artists = ", ".join(artist_names)
            else:
                album_artists = album.get("artists")[0].get("name")
            total_tracks = album.get("total_tracks")
            album_thumb = album.get("images")[0].get("url")
            album_url = album.get("external_urls").get("spotify")
            release_date = album.get("release_date")
            caption= f"**{album_name}** by **{album_artists}**"
            description= f"{str(release_date)} • {str(total_tracks)} Songs • {album_artists}"
            await store_values(str(id), album_url)
            results.append(
                InlineQueryResultPhoto(
                    title=album_name,
                    description=description,
                    thumb_url=album_thumb,
                    photo_url=album_thumb,
                    caption=caption,
                    id=id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("🌐 Fetching links...", callback_data="LOADING_BUTTON")]
                        ]
                    )
                )        
            )
        if results: await inline_query.answer(results, switch_pm_text="Odesli - On demand smart links", switch_pm_parameter="help")
    elif type=='t':
        for track in tracks:
            id = uuid.uuid4()
            track_name = track.get("name")
            track_artists = track.get("artists")
            if len(track_artists) > 1:
                artist_names = []
                for artist in track_artists:
                    artist_names.append(artist.get("name"))
                track_artists = ", ".join(artist_names)
            else:
                track_artists = track.get("artists")[0].get("name")
            track_album_name = track.get("album").get("name")
            track_thumb = track.get("album").get("images")[0].get("url")
            track_preview = track.get("preview_url")
            track_url = track.get("external_urls").get("spotify")
            release_date = track.get("album").get("release_date")
            description= f"{track_artists} • {track_album_name} • {release_date}"
            caption= f"**{track_name}** by **{track_artists}**"
            await store_values(str(id), track_url)
            results.append(
                InlineQueryResultPhoto(
                    title=track_name,
                    description=description,
                    thumb_url=track_thumb,
                    photo_url=track_thumb,
                    caption=caption,
                    id=id,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("🌐 Fetching links...", callback_data="LOADING_BUTTON")]
                        ]
                    )
                )        
            )
        if results: await inline_query.answer(results, switch_pm_text="Odesli - On demand smart links", switch_pm_parameter="help")

async def chosen_result_handler(client, query, message_id):
    
    try: result = await odesli.getByUrl(query)
    except Exception as e:
        LOGGER(__name__).error(e)
        try: r = await songwhip_full(query)
        except: 
            await client.edit_inline_text(message_id, URL_ERROR)
            return
        else:
            await client.edit_inline_text(message_id, r)
            return 

    if isinstance(result, SongResult):
        entity = result.song
        title = entity.title
        artist = entity.artistName
        thumb = entity.thumbnailUrl
        providers = result.songsByProvider
        r = '**' + entity.title + "** by **" + entity.artistName + '** \n\n[Odesli](' + result.songLink + ')'
		
    elif isinstance(result, AlbumResult):
        entity = result.album
        title = entity.title
        artist = entity.artistName
        thumb = entity.thumbnailUrl
        providers = result.albumsByProvider
        r = '**' + entity.title + "** by **" + entity.artistName + '** \n\n[Odesli](' + result.albumLink + ')'
        
    op = []
    for provider in providers:
        if provider == 'youtube':
            r += (" | [YouTube](" + providers['youtube'].linksByPlatform['youtube'] + ') | [YT Music](' +
            providers['youtube'].linksByPlatform['youtubeMusic'] + ')')
            op.append("youtube")
            continue
        if provider == 'itunes':
            r += (" | [Apple Music](" + providers['itunes'].linksByPlatform['appleMusic'] + ')')
            op.append("itunes")
            continue
        if provider == 'amazon':
            r += (' | [Amazon Music](' +
            providers['amazon'].linksByPlatform['amazonMusic'] + ')')
            op.append("amazon")
            continue	
        else:
            r += ' | [' + (provider.title() + '](' + providers[provider].linksByPlatform[provider] + ')')
            op.append(provider)
    
    await client.edit_inline_text(message_id, r)
    try: 
        r = await songwhip(query, r, op)
        await client.edit_inline_text(message_id, r)
    except:
        return

async def songwhip_full(song_link):
    async with httpx.AsyncClient() as client:
        data = {'country': 'IN', 'url': song_link}
        response = await client.post('https://songwhip.com/api/songwhip/create', json=data, timeout=60)
        response.raise_for_status()

        if response.status_code == httpx.codes.OK:
            try:
                x = response.json()
                name = x.get("data").get("item").get("name")
                artist = x.get("data").get("item").get("artists")[0].get("name")
                r = f"**{name}** by **{artist}** \n\n"
            except: pass
            try:
                tmp = "https://songwhip.com/" + x.get("data").get("item").get("url")
                r += f"[Songwhip]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("qobuz")[0].get("link")
                r += f" | [Qobuz]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("spotify")[0].get("link")
                r += f" | [Spotify]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("deezer")[0].get("link")
                r += f" | [Deezer]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("tidal")[0].get("link")
                r += f" | [Tidal]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("amazonMusic")[0].get("link")
                r += f" | [Amazon Music]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("itunes")[0].get("link")
                tmp = tmp.replace("{country}", "gb", 1)
                r += f" | [Apple Music]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("napster")[0].get("link")
                r += f" | [Napster]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("lineMusic")[0].get("link")
                r += f" | [Line Music]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("youtube")[0].get("link")
                tmp1 = x.get("data").get("item").get("links").get("youtubeMusic")[0].get("link")
                r += f" | [Youtube]({tmp}) | [Youtube Music]({tmp1})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("jioSaavn")[0].get("link")
                r += f" | [JioSaavn]({tmp})"
            except: pass
            try:
                tmp = x.get("data").get("item").get("links").get("gaana")[0].get("link")
                r += f" | [Gaana]({tmp})"
            except: pass
 
            return r