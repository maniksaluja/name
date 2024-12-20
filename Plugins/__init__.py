import asyncio
from time import perf_counter, time

from cachetools import TTLCache
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, Message

from config import AUTO_DELETE_TIME, LOG_CHANNEL_ID, LOG_CHANNEL_ID2, OWNER_ID
from Database.settings import get_settings

#Caches
ADMIN_REPLY_BACK = TTLCache(1024, (60 * 5), perf_counter) #{user_id: {"forward": forward_func, "to_user": user_id, "msg_id": message.id}}
USER_LISTENING = TTLCache(1024, (60*5), perf_counter) #{user_id: {"forward": forward_func, "mention": mention, "msg_id": message.id}}

current_listening = []

LISTENING_FOR = None #Will have user id of the user for which owner is replying back to

async def is_listening(_, __, m: Message or CallbackQuery):
    global USER_LISTENING
    if not m.from_user:
        return False
    if m.from_user.id in current_listening:
        return True
    return False

async def reply_owner_listening(_, __, m: Message):
    global LISTENING_FOR
    global ADMIN_REPLY_BACK
    if m.from_user and (m.from_user.id == OWNER_ID):
        if LISTENING_FOR and LISTENING_FOR in ADMIN_REPLY_BACK:
            return True
    return False

my_owner_listner = filters.create(reply_owner_listening)
my_listner = filters.create(is_listening)


# Optimized tryer function to handle FloodWait
async def tryer(func, *args, **kwargs):
    while True:
        try:
            return await func(*args, **kwargs)
        except FloodWait as e:
            wait_time = min(e.value, 10)  # Max delay capped at 10 seconds
            print(f"FloodWait detected: Waiting for {wait_time} seconds...")
            await asyncio.sleep(wait_time)
        except Exception as ex:
            print(f"Unexpected error: {ex}")
            return

# Utility functions for time formatting
def grt(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}S"
    elif seconds < 3600:
        return f"{int(seconds / 60)}M"
    else:
        return f"{int(seconds / 3600)}H"

AUTO_DELETE_STR = grt(AUTO_DELETE_TIME)

def alpha_grt(sec: int) -> str:
    if sec < 60:
        return f"{sec}S"
    elif sec < 3600:
        return f"{int(sec / 60)}M"
    return "60M+"

# Global constants and variables
startTime = time()
markup = None

# Function to build the InlineKeyboardMarkup


# async def build(client: Client):
#     try:
#         markup = await start_markup(client)
#     except Exception as e:
#         markup = None
#         print(f"Error in build funtion in init file of plugin: {e}")
#     return markup


async def get_logs_channel():
    setting = (await get_settings()).get("logs", None)
    if not setting:
        return []
    
    elif setting == "both":
        return [LOG_CHANNEL_ID, LOG_CHANNEL_ID2]
    
    elif setting == "l1":
        return [LOG_CHANNEL_ID]

    else:
        return [LOG_CHANNEL_ID2]