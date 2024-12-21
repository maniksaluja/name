import asyncio
from typing import List

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import AUTO_DELETE_TIME
from Database.count import get_count
from templates import POST_DELETE_TEXT


async def Delete_task(m: List[Message], link=None):
    await asyncio.sleep(AUTO_DELETE_TIME)
    z = m[-1]
    for i in m:
        if not i.empty:
            try:
                await i.delete()
            except:
                continue
    cur = await get_count()
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Get again", url=link)]])
    await z.reply_text(POST_DELETE_TEXT.format(cur), reply_markup=kb)
    return

async def task_initiator(m: List[Message], link=None):
    if AUTO_DELETE_TIME:
        asyncio.create_task(Delete_task(m, link))
    return