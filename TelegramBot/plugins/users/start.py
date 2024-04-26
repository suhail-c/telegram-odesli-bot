import re, os
import pyrogram
import aiofiles

from pyrogram import Client, filters, enums, raw
from pyrogram.raw import types
from pyrogram.types import (Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InlineQuery, ChosenInlineResult, BotCommand, BotCommandScope, BotCommandScopeChat)

from TelegramBot import bot
from TelegramBot.helpers.constants import *
from TelegramBot.config import OWNER_USERID, SUDO_USERID
from TelegramBot.database import database
from TelegramBot.helpers.decorators import ratelimiter
from TelegramBot.helpers.songfinder import *
from TelegramBot.helpers.pasting_services import *
from TelegramBot.helpers.shazam import *
from TelegramBot.helpers.jiosaavn import *
from TelegramBot.helpers.spotify import *
from TelegramBot.helpers.applemusic import *
#from TelegramBot.helpers.tidal import *

@Client.on_message(filters.command("start"))
async def start(_, message: Message):
    if len(message.command) == 2 and message.command[1] in ["help"]:
        return await message.reply_text(
        HELP_CAPTION,
        quote=True,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN)
        
    await database.saveUser(message.from_user)
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("...", reply_markup=ReplyKeyboardMarkup(RBUTTON, is_persistent=False, resize_keyboard=True))
        await message.reply_text(
            START_CAPTION,
            reply_markup=InlineKeyboardMarkup(START_BUTTON),
            quote=True,
            disable_web_page_preview=True)
        return 
    await message.reply_text(
        START_CAPTION,
        reply_markup=InlineKeyboardMarkup(START_BUTTON_G),
        quote=True,
        disable_web_page_preview=True)

@Client.on_message(filters.command("help"))
async def help(_, message: Message):
    await message.reply_text(
        HELP_CAPTION,
        quote=True,
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.command("info"))
async def saavn(_, message: Message):
    if len(message.command) == 2:
        if "jiosaavn" in message.command[1]:
            match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:jiosaavn)\.(?:[a-z.]+)\/[^\s]+)", message.command[1])
            if match:
                rp = await message.reply_text("Fetching Data...", quote=True)
                rt, title = await jiosaavn(message.command[1])
                try:
                    rt = await telegraph_paste(rt, "JioSaavn")
                    await rp.edit_text(f"<a href='{rt}'<a>{title}</a>", parse_mode=enums.ParseMode.HTML)
                except:
                    root_path = os.path.join(os.getcwd(), f"resource/apple")
                    async with aiofiles.open(f"{root_path}/{title}.html", "w") as file:
                        await file.write(rt)
                    await message.reply_document(f"{root_path}/{title}.html")
                    os.remove(f"{root_path}/{title}.html")
        elif "spotify" in message.command[1]:
            rp = await message.reply_text("Fetching Data...", quote=True)
            rt, title= await get_spotify_data(message.command[1])
            try:
                rt = await telegraph_paste(rt, "Spotify")
                await rp.edit_text(f"<a href='{rt}'<a>{title}</a>", parse_mode=enums.ParseMode.HTML)
            except:
                root_path = os.path.join(os.getcwd(), f"resource/apple")
                async with aiofiles.open(f"{root_path}/{title}.html", "w") as file:
                    await file.write(rt)
                await message.reply_document(f"{root_path}/{title}.html")
                os.remove(f"{root_path}/{title}.html")
        elif "music.apple.com" in message.command[1]:
            rp = await message.reply_text("Fetching Data...", quote=True)
            rt, title= await get_applem_info(message.command[1])
            try: 
                rt = await telegraph_paste(rt, "Apple Music")
                await rp.edit_text(f"<a href='{rt}'<a>{title}</a>", parse_mode=enums.ParseMode.HTML)
            except:
                root_path = os.path.join(os.getcwd(), f"resource/apple")
                async with aiofiles.open(f"{root_path}/{title}.html", "w") as file:
                    await file.write(rt)
                await message.reply_document(f"{root_path}/{title}.html")
                os.remove(f"{root_path}/{title}.html")
        
    elif message.reply_to_message is not None:
        link= message.reply_to_message.text
        match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:spotify|apple|jiosaavn)\.(?:[a-z.]+)\/[^\s]+)", link)
        if not match: return await message.reply_text("**--Get track/album info--** \n\n**Usage:** Use the /info command followed by a link to retrieve comprehensive information about a track or album. Presently, this supports Spotify, Apple Music and JioSaavn links.", quote=True, parse_mode=enums.ParseMode.MARKDOWN)
        if "jiosaavn" in match.group():
            match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:jiosaavn)\.(?:[a-z.]+)\/[^\s]+)", link)
            if match:
                rp = await message.reply_text("Fetching Data...", quote=True)
                rt, title = await jiosaavn(link)
                try:
                    rt = await telegraph_paste(rt, "JioSaavn")
                    await rp.edit_text(f"<a href='{rt}'<a>{title}</a>", parse_mode=enums.ParseMode.HTML)
                except:
                    root_path = os.path.join(os.getcwd(), f"resource/apple")
                    async with aiofiles.open(f"{root_path}/{title}.html", "w") as file:
                        await file.write(rt)
                    await message.reply_document(f"{root_path}/{title}.html")
                    os.remove(f"{root_path}/{title}.html")
        elif "spotify" in match.group():
            rp = await message.reply_text("Fetching Data...", quote=True)
            rt, title= await get_spotify_data(link)
            try:
                rt = await telegraph_paste(rt, "Spotify")
                await rp.edit_text(f"<a href='{rt}'<a>{title}</a>", parse_mode=enums.ParseMode.HTML)
            except:
                root_path = os.path.join(os.getcwd(), f"resource/apple")
                async with aiofiles.open(f"{root_path}/{title}.html", "w") as file:
                    await file.write(rt)
                await message.reply_document(f"{root_path}/{title}.html")
                os.remove(f"{root_path}/{title}.html")
        elif "music.apple.com" in match.group():
            rp = await message.reply_text("Fetching Data...", quote=True)
            rt, title= await get_applem_info(link)
            try:
                rt = await telegraph_paste(rt, "Apple Music")
                await rp.edit_text(f"<a href='{rt}'<a>{title}</a>", parse_mode=enums.ParseMode.HTML)
            except:
                root_path = os.path.join(os.getcwd(), f"resource/apple")
                async with aiofiles.open(f"{root_path}/{title}.html", "w") as file:
                    await file.write(rt)
                await message.reply_document(f"{root_path}/{title}.html")
                os.remove(f"{root_path}/{title}.html")
    else:
        await message.reply_text("**--Get track/album info--** \n\n**Usage:** Use the /info command followed by a link to retrieve comprehensive information about a track or album. Presently, this supports Spotify, Apple Music and JioSaavn links.", quote=True, parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.command("odesli"))
async def odesli(client: Client, message: Message):
    if len(message.command) == 2:
        match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:shazam|spotify|deezer|tidal|yandex|apple|youtube|youtu|music\.youtube|pandora|amazon|soundcloud|napster|audius|anghami|boomplay|audiomack|bandcamp|album|artist|song|pods)\.(?:[a-z.]+)\/[^\s]+)", message.command[1])
        if match: 
            song_link = match.group()
            if "shazam.com" in song_link:
                song_link = await slink_to_alink(song_link)
            if song_link is None:
                await client.reply_text(URL_ERROR, quote=True)
                return
        try: await fetch_links(client, message, song_link)
        except Exception as e:
            LOGGER(__name__).error(e)
    elif message.reply_to_message is not None:
        message= message.reply_to_message
        match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:shazam|spotify|deezer|tidal|yandex|apple|youtube|youtu|music\.youtube|pandora|amazon|soundcloud|napster|audius|anghami|boomplay|audiomack|bandcamp|album|artist|song|pods)\.(?:[a-z.]+)\/[^\s]+)", message.text)
        if match: 
            song_link = match.group()
            if "shazam.com" in song_link:
                song_link = await slink_to_alink(song_link)
            if song_link is None:
                await client.reply_text(URL_ERROR, quote=True)
                return
        try: await fetch_links(client, message, song_link)
        except Exception as e:
            LOGGER(__name__).error(e)
    else:
        await message.reply_text("**--Find Music Links--** \n\n**Usage:** You can send a track or album link directly to the bot. Alternatively, reply to a message containing a link with the /odesli command, or send /odesli command followed by the link.", quote=True, parse_mode=enums.ParseMode.MARKDOWN)

@Client.on_message(filters.new_chat_members, group=1)
async def newChat(_, message: Message):
    """
    Get notified when someone add bot in the group, then saves that group chat_id
    in the database.
    """

    chatid = message.chat.id
    chattitle = message.chat.title
    if message.chat.username is not None: chatusername = message.chat.username
    else: chatusername= "none"
    t = f"#newgroup \n\n{chattitle} | {str(chatid)} | @{chatusername}"
    for new_user in message.new_chat_members:
        if new_user.id == bot.me.id:
            await database.saveChat(chatid)
            #await bot.send_message(chat_id=, text=t)

@Client.on_callback_query()
async def botCallbacks(_, CallbackQuery: CallbackQuery):

    if CallbackQuery.data == "LOADING_BUTTON": 
        return await CallbackQuery.answer("Please wait... This may take a minute.", show_alert=True)

    clicker_user_id = CallbackQuery.from_user.id
    user_id = CallbackQuery.message.reply_to_message.from_user.id

    if clicker_user_id != user_id:
        return await CallbackQuery.answer("This command is not initiated by you.")

    if CallbackQuery.data == "HELP_BUTTON":             
        await CallbackQuery.edit_message_text(HELP_CAPTION, reply_markup=InlineKeyboardMarkup(GOBACK_BUTTON), disable_web_page_preview=True, parse_mode=enums.ParseMode.MARKDOWN)

    elif CallbackQuery.data == "START_BUTTON":
        await CallbackQuery.edit_message_text(START_CAPTION, reply_markup=InlineKeyboardMarkup(START_BUTTON))

    await CallbackQuery.answer()
    
@Client.on_message(filters.text)
async def main(client: Client, message: Message):
    if message.text.startswith("/") or message.via_bot:
        return 
    if message.chat.type == enums.ChatType.PRIVATE:
        match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:shazam|spotify|deezer|tidal|yandex|apple|youtube|youtu|music\.youtube|pandora|amazon|soundcloud|napster|audius|anghami|boomplay|audiomack|bandcamp|album|artist|song|pods)\.(?:[a-z.]+)\/[^\s]+)", message.text)
    else: match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:shazam|spotify|deezer|tidal|yandex|apple|music\.youtube|pandora|amazon|soundcloud|napster|audius|anghami|boomplay|audiomack|bandcamp|album|artist|song|pods)\.(?:[a-z.]+)\/[^\s]+)", message.text)
    if match: 
        song_link = match.group()
        if "shazam.com" in song_link:
            song_link = await slink_to_alink(song_link)
            if song_link is None:
                await client.reply_text(URL_ERROR, quote=True)
                return
    
        try: await fetch_links(client, message, song_link)
        except Exception as e:
            print(e)
            return 
    elif message.chat.type == enums.ChatType.PRIVATE and not message.via_bot:
        match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:[a-zA-Z0-9-.]+)\.(?:[a-z.]+)\/[^\s]+)", message.text)
        length= len(message.text)
        if not match:
            if length>60: return 
            await message.reply_text("Search Track/Album?", quote=True, reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton('Track Search', switch_inline_query_current_chat=f".st {message.text}")
                        ],
                        [
                            InlineKeyboardButton('Album Search', switch_inline_query_current_chat=f".sa {message.text}")
                        ]
                    ]))
        else:
            await message.reply_text("Unsupported Link", quote=True)

@Client.on_inline_query()
async def answer(client: Client, inline_query: InlineQuery):
    query = inline_query.query.strip()
    match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:shazam|spotify|deezer|tidal|yandex|apple|youtube|youtu|music\.youtube|pandora|amazon|soundcloud|napster|audius|anghami|boomplay|audiomack|bandcamp|album|artist|song|pods)\.(?:[a-z.]+)\/[^\s]+)", query)
    
    if not query:
        await inline_query.answer(
        switch_pm_text="Odesli - On demand smart links",
        switch_pm_parameter="help",
        results=[
            InlineQueryResultArticle(
                title="Find Music Links",
                description="Type a track name, or paste any music link.",
                thumb_url="https://telegra.ph/file/d364144102981e32d35c1.png",
                input_message_content=InputTextMessageContent(INFO_M),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Try Now", switch_inline_query_current_chat="")]
                    ]
                )
            )      
         ]
     )
    elif match:
        song_link = match.group()
        if "shazam.com" in song_link:
            song_link = await slink_to_alink(song_link)
        try: await get_inline_result_link(client, inline_query, song_link)
        except Exception as e:
            LOGGER(__name__).error(e)

    elif query.startswith(".st"):
        query = " ".join(query.split(" ")[1:])
        if query == "":
             await inline_query.answer(
        switch_pm_text="Odesli - On demand smart links",
        switch_pm_parameter="help",
        results=[
            InlineQueryResultArticle(
                title="Search for a track",
                description="Type a track name to search.",
                thumb_url="https://telegra.ph/file/94b52a8d5e4db3cbd80bc.png",
                input_message_content=InputTextMessageContent(INFO_ST),
                reply_markup=InlineKeyboardMarkup(
                        [
                        [InlineKeyboardButton("Try Now", switch_inline_query_current_chat=".st ")]
                        ]
                    )
                    )      
                 ]
             )
             return
        await get_inline_result_spotify(client, inline_query, query, 't')
    elif query.startswith(".sa"):
        query = " ".join(query.split(" ")[1:])
        if query == "":
            await inline_query.answer(
        switch_pm_text="Odesli - On demand smart links",
        switch_pm_parameter="help",
        results=[
            InlineQueryResultArticle(
                title="Search for an album",
                description="Type an album name to search.",
                thumb_url="https://telegra.ph/file/0247cd08f135c5eb2bfec.png",
                input_message_content=InputTextMessageContent(INFO_SA),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Try Now", switch_inline_query_current_chat=".sa ")]
                    ]
                )
            )      
         ]
     )
            return
        await get_inline_result_spotify(client, inline_query, query, 'a')
    else:
        await get_inline_result_query(client, inline_query)

@Client.on_raw_update()
async def chosen_inline_result(client, update, _, __):
    if not isinstance(update, raw.types.UpdateBotInlineSend): return 
    inline_message_id = pyrogram.utils.pack_inline_message_id(update.msg_id)
    query = update.query.strip()
    match = re.search(r"((?:https?:\/\/)?(?:(?:[a-zA-Z0-9-.]+)\.)?(?:shazam|spotify|deezer|tidal|yandex|apple|youtube|youtu|music\.youtube|pandora|amazon|soundcloud|napster|audius|anghami|boomplay|audiomack|bandcamp|album|artist|song|pods)\.(?:[a-z.]+)\/[^\s]+)", query)
    if match:
        if "shazam.com" in query:
            query = await slink_to_alink(query)
        try: 
            await chosen_result_handler(client, query, inline_message_id)
            return
        except: return 
    else:
        id_to_retrieve = update.id
        result = await retrieve_values_by_id(id_to_retrieve)
        if result is None: return
        link = result[0]
        if "www.shazam.com" in link:
            m = link + "\n\n__Couldn't find any streaming links for this track.__"
            await client.edit_inline_text(inline_message_id, m)
        else:
            await chosen_result_handler(client, link, inline_message_id)
