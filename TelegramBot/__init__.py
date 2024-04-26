import sys, os, shutil
import time
from asyncio import get_event_loop, new_event_loop, set_event_loop
import uvloop 
import httpx

from pyrogram import Client
from TelegramBot import config
from TelegramBot.database.MongoDb import check_mongo_uri
from TelegramBot.database.sqdb import delete_old_entries_by_hours
from TelegramBot.logging import LOGGER
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from TelegramBot.helpers.odesli.Odesli import Odesli
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

uvloop.install()
LOGGER(__name__).info("Starting TelegramBot....")
BotStartTime = time.time()


if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGER(__name__).critical("""
=============================================================
You MUST need to be on python 3.7 or above, shutting down the bot...
=============================================================
""")
    sys.exit(1)

    
LOGGER(__name__).info("setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

    
LOGGER(__name__).info(
    r"""
____________________________________________________________________
|  _______   _                                ____        _        |
| |__   __| | |                              |  _ \      | |       |
|    | | ___| | ___  __ _ _ __ __ _ _ __ ___ | |_) | ___ | |_      |
|    | |/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \|  _ < / _ \| __|     |
|    | |  __/ |  __/ (_| | | | (_| | | | | | | |_) | (_) | |_      |
|    |_|\___|_|\___|\__, |_|  \__,_|_| |_| |_|____/ \___/ \__|     |
|                    __/ |                                         |
|__________________________________________________________________|   
""")
# https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20


LOGGER(__name__).info("initiating the client....")
LOGGER(__name__).info("checking MongoDb URI....")
loop.run_until_complete(check_mongo_uri(config.MONGO_URI))

 
if not os.path.exists("resource"):
    os.mkdir("resource")

async def clear():
    await delete_old_entries_by_hours("mytable", 12)
    shutil.rmtree("resource")
    os.mkdir("resource")

scheduler = AsyncIOScheduler()
scheduler.add_job(clear, "interval", minutes=1440)
scheduler.start()

# intitatioing odesli, sporipy
httpx_client= httpx.AsyncClient(follow_redirects=True)
odesli= Odesli()
spotify= spotipy.Spotify(requests_session=True, client_credentials_manager=SpotifyClientCredentials(client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET))
LOGGER(__name__).info("initiated the Odesli & Spotipy client....")

# https://docs.pyrogram.org/topics/smart-plugins
plugins = dict(root="TelegramBot/plugins")
bot = Client(
    "TelegramBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=plugins)
