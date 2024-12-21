import asyncio
from typing import List

from pyrogram.types import Message

from config import AUTO_DELETE_TIME
from Database.count import get_count
from templates import POST_DELETE_TEXT


async def Delete_task(m: List[Message]):
    await asyncio.sleep(AUTO_DELETE_TIME)
    z = m[-1]
    for i in m:
        if not i.empty:
            try:
                await i.delete()
            except:
                continue
    cur = await get_count()
    await z.reply_text(POST_DELETE_TEXT.format(cur))
    return

async def task_initiator(m: List[Message]):
    if AUTO_DELETE_TIME:
        asyncio.create_task(Delete_task(m))
    return