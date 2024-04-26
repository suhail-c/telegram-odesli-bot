from pyrogram.types import (InlineKeyboardButton, KeyboardButton, WebAppInfo)


START_CAPTION = """
Hi there, I'm an unofficial Odesli Bot! With support for all major streaming platforms, simply share a link to your favorite tune and I'll provide you with links to that same song on all your other preferred platforms. 

Powered by odesli.co & songwhip.com
"""


HELP_CAPTION = """
🔗 **--Find Music Links--**

You can send a track or album link directly to the bot. Alternatively, reply to a message containing a link with the /odesli command. or send /odesli command followed by the link.

🔍 **--Inline Search Mode--**

In any chat, type "@tgodeslibot <link>" to retrieve music links using inline mode.

To search for an album by query and get music links, use "@tgodeslibot .sa <album_name>" (replace <album_name> with the actual album name).

For track searches, employ the command "@tgodeslibot .st <track_name>" (replace <track_name> with the actual track name).

ℹ  **--Get track/album Info--**

Utilize the /info command with a link to retrieve comprehensive information about a track or album. Presently, this supports Spotify, Apple Music and JioSaavn links.
"""


URL_ERROR = "__There's a problem with that URL. Either we don't support this music service or the URL is malformed. Try one from a different music service.__"


RATE_TXT = "__If you like this bot, you can rate me [HERE](https://t.me/botsarchive/2726) ❤️__"


INFO = "**Odesli Bot** \n\nAutomated, on-demand smart links for songs, albums, podcasts and more. For artists, for fans, for free."
INFO_M = "**Find Music Links** \n\n**Usage:** `@tgodeslibot [Type a track name, or paste any music link]`"
INFO_ST = "**Find Music Links - Track Search** \n\n**Usage:** `@tgodeslibot .st [Type a track name]`"
INFO_SA = "**Find Music Links - Album Search** \n\n**Usage:** `@tgodeslibot .sa [Type an album name]`"

START_BUTTON = [
                   [
                        InlineKeyboardButton('Help', callback_data='HELP_BUTTON')
                   ],
                   [
                       InlineKeyboardButton('Add me to Group', url='https://t.me/tgodeslibot?startgroup=true')
                   ],
                   [
                        InlineKeyboardButton('Inline Search', switch_inline_query_current_chat=""),
                        InlineKeyboardButton('Give Feedback', url='https://t.me/dmviabot')
                   ]
               ]

START_BUTTON_G = [
                   [
                        InlineKeyboardButton('Help', url='https://t.me/tgodeslibot?start=help')
                   ],
                   [
                        InlineKeyboardButton('Inline Search', switch_inline_query_current_chat=""),
                        InlineKeyboardButton('Give Feedback', url='https://t.me/dmviabot')
                   ]
                 ]

SEARCH_BUTTON = [
                    [
                        InlineKeyboardButton('Track Search', switch_inline_query_current_chat=".st ")
                    ],
                    [
                        InlineKeyboardButton('Album Search', switch_inline_query_current_chat=".sa ")
                    ]
                ]

GOBACK_BUTTON = [[InlineKeyboardButton("🔙 Go Back", callback_data="START_BUTTON")]]

RBUTTON = [
              [
                KeyboardButton('Odesli', web_app=WebAppInfo(url="https://odesli.co")),
                KeyboardButton('Songwhip', web_app=WebAppInfo(url="https://songwhip.com/create"))
              ]
           ]
