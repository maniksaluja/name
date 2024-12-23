import asyncio
import random
from typing import List  # Import random module

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from config import (DB_CHANNEL_2_ID, DB_CHANNEL_ID, LINK_GENERATE_IMAGE,
                    SUDO_USERS)
from Database.count import incr_count
from Database.count_2 import incr_count_2
from Database.encr import update
from Database.settings import get_settings
from templates import CUSTOM_CAPTION, LINK_GEN

from . import alpha_grt, get_logs_channel, tryer
from .encode_decode import Int2Char, encrypt

dic = {}
me = None

class bkl:
    def done():
        return True

TASK = bkl

def get_TASK():
    return TASK.done()

async def get_me(client):
    global me
    if not me:
        me = await client.get_me()
    return me

def in_batch(user_id):
    return user_id in dic or not get_TASK()

async def send_delayed_message(delay=None):
    """Delay function to avoid flood limits."""
    if delay is None:
        delay = random.uniform(0.5, 2)  # Random delay between 0.5-2 seconds
    await asyncio.sleep(delay)

@Client.on_message(filters.command('b') & filters.user(SUDO_USERS) & filters.private)
async def batch(client, message):
    if message.from_user.id in dic:
        return await message.reply('**Batch Under Process Use /cancel For Stop!!**')
    if TASK and not TASK.done():
        return await message.reply('Wait Until The Batch Gets Done.')
    dic[message.from_user.id] = []
    await message.reply('**OKAY Now I Can Make Batch Link When You Are Done Use /end **', quote=True)

async def batch_cwf(client, message):
    if message.text:
        if message.text.startswith('/'):
            return
    if message.from_user.id in dic:
        dic[message.from_user.id].append(message)

@Client.on_message(filters.command('cancel') & filters.user(SUDO_USERS) & filters.private)
async def cancel(client, message):
    if not message.from_user.id in dic:
        return await message.reply('Nothing to cancel.')
    dic.pop(message.from_user.id)
    await message.reply('Batch Cancelled.')

async def end(client: Client, message: Message):
    if not message.from_user.id in dic:
        return
    messages: List[Message] = dic[message.from_user.id]
    dic.pop(message.from_user.id)
    if not messages:
        return
    progress_message = await message.reply("**It Takes Few Minutes...**")
    dest_ids = []
    dest_ids_2 = []
    all_vid = True
    for msg in messages:
        if not msg.video:
            all_vid = False
         
        new = await tryer(msg.copy, DB_CHANNEL_ID, caption=CUSTOM_CAPTION)
        dest_ids.append(new.id)
        new = await tryer(msg.copy, DB_CHANNEL_2_ID, caption=CUSTOM_CAPTION)
        dest_ids_2.append(new.id)
        
        # Add only delay, no messages to user
        await send_delayed_message()
    
    if all_vid:
        duration = sum([msg.video.duration for msg in messages])
        duration = "⋞⋮⋟ " + alpha_grt(duration)
    else:
        duration = ''
    
    cur = await incr_count()
    encr = encrypt(f'{Int2Char(dest_ids[0])}-{Int2Char(dest_ids[-1])}|{Int2Char(cur)}')
    encr_2 = encrypt(f'{Int2Char(dest_ids[0])}-{Int2Char(dest_ids[-1])}|{Int2Char(cur)}')
    await update(encr, encr_2)
    
    link = f'https://t.me/{(await get_me(client)).username}?start=batchone{encr}'
    txt = LINK_GEN.format(f'{cur}', duration, link)
    markup = IKM([[IKB('Share', url=link)]])
    settings = await get_settings()
    await progress_message.delete()
    
    channels = await get_logs_channel()
    if LINK_GENERATE_IMAGE and settings['image']:
        await message.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup, quote=True)
        if not  channels:
            return
        else:
            for channel in channels:
                if not channel:
                    continue
                await client.send_photo(channel, LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
    else:
        await message.reply(txt, reply_markup=markup, quote=True)
        if not  channels:
            return
        else:
            for channel in channels:
                await client.send_photo(channel, LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)


@Client.on_message(filters.command('end') & filters.user(SUDO_USERS) & filters.private)
async def endddd(client, message):
    global TASK
    TASK = asyncio.create_task(end(client, message))
    await TASK
