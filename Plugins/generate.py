import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from config import (DB_CHANNEL_2_ID, DB_CHANNEL_ID, LINK_GENERATE_IMAGE,
                    SUDO_USERS)
from Database.count import incr_count
from Database.settings import get_settings
from templates import LINK_GEN

from . import get_logs_channel, tryer
from .encode_decode import Int2Char, encrypt
from .watchers import get_me


async def fetch_messages(client, channel_id, msg_ids):
    try:
        return await client.get_messages(channel_id, msg_ids)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await fetch_messages(client, channel_id, msg_ids)  # Retry after delay

@Client.on_message(filters.command('gen') & filters.user(SUDO_USERS))
async def generate(_, m: Message):
    try:
        st = int(m.text.split()[1])
        en = int(m.text.split()[2])
    except:
        return await m.reply('Usage: `/gen [start_id] [end_id]`')
    
    okkie = await m.reply("**Rendering...**")
    mess_ids = []
    while en - st + 1 > 150:  # Reduce batch size to 150
        mess_ids.append(list(range(st, st + 150)))
        st += 150
    if en - st + 1 > 0:
        mess_ids.append(list(range(st, en + 1)))
    
    # Fetching messages with optimized async function
    messes = []
    for x in mess_ids:
        messes += await fetch_messages(_, DB_CHANNEL_ID, x)
    
    await tryer(okkie.edit, "**Generating Links...**")
    settings = await get_settings()
    batches = []
    temp = []
    for x in messes:
        if x and not x.empty:
            temp.append(x)
        if len(temp) == settings['generate']:
            batches.append(temp)
            temp = []
    if temp:
        batches.append(temp)
    
    image = settings['image']
    channels = await get_logs_channel()
    for x in batches:
        init = x[0].id
        final = x[-1].id
        cur = await incr_count()
        encr = encrypt(f'{Int2Char(init)}-{Int2Char(final)}|{Int2Char(cur)}')
        link = f'https://t.me/{(await get_me(_)).username}?start=batchone{encr}'
        txt = LINK_GEN.format(f'{cur}', '', link)
        markup = IKM([[IKB('Share', url=link)]])
        try:
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if not channels:
                continue
            else:
                for channel in channels:
                    if not channel:
                        continue
                    await msg.copy(channel)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if channels:
                for channel in channels:
                    await msg.copy(channel)
    await tryer(okkie.delete)
    await tryer(m.reply, "**Generation Completed.**", quote=True)

@Client.on_message(filters.command('gen2') & filters.user(SUDO_USERS))
async def generate2(_, m: Message):
    try:
        st = int(m.text.split()[1])
        en = int(m.text.split()[2])
    except:
        return await m.reply('Usage: `/gen2 [start_id] [end_id]`')
    
    okkie = await m.reply("**Rendering...**")
    mess_ids = []
    while en - st + 1 > 150:  # Reduce batch size to 150
        mess_ids.append(list(range(st, st + 150)))
        st += 150
    if en - st + 1 > 0:
        mess_ids.append(list(range(st, en + 1)))
    
    # Fetching messages with optimized async function
    messes = []
    for x in mess_ids:
        messes += await fetch_messages(_, DB_CHANNEL_2_ID, x)
    
    await tryer(okkie.edit, "**Generating Links...**")
    settings = await get_settings()
    batches = []
    temp = []
    for x in messes:
        if x and not x.empty:
            temp.append(x)
        if len(temp) == settings['generate']:
            batches.append(temp)
            temp = []
    if temp:
        batches.append(temp)
    
    image = settings['image']
    channels = await get_logs_channel()
    for x in batches:
        init = x[0].id
        final = x[-1].id
        cur = await incr_count()
        encr = encrypt(f'{Int2Char(init)}-{Int2Char(final)}|{Int2Char(cur)}')
        link = f'https://t.me/{(await get_me(_)).username}?start=batchtwo{encr}'
        txt = LINK_GEN.format(f'{cur}', '', link)
        markup = IKM([[IKB('Share', url=link)]])
        try:
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if channels:
                for channel in channels:
                    await msg.copy(channel)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if LINK_GENERATE_IMAGE and image:
                msg = await m.reply_photo(LINK_GENERATE_IMAGE, caption=txt, reply_markup=markup)
            else:
                msg = await m.reply(txt, reply_markup=markup)
            if channels:
                for channel in channels:
                    if not channel:
                        continue
                    await msg.copy(channel)
    await tryer(okkie.delete)
    await tryer(m.reply, "**Generation Completed.**", quote=True)

if DB_CHANNEL_2_ID > 0:
    @Client.on_message(filters.command('id') & filters.user(DB_CHANNEL_2_ID) & filters.private)
    async def idddd(_, m):
        reply = m.reply_to_message
        if not reply:
            return await m.reply('Reply to a message.')
        await m.reply(reply.id)
